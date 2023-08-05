import json
import pycrfsuite
import uuid
import os
import re
from collections import Counter
from sklearn.model_selection import train_test_split
from typing import List

from .config import CRFConfig
from .feature_extraction import (
    FeatureExtractor,
    FEATURE_LAYER_POS,
    FEATURE_LAYER_GRAMMAR,
    FEATURE_LAYER_WORD,
    KNOWN_LAYERS
)
from .tagging_report import TaggingReport
from . import exceptions


def check_model_loaded(func):
    """
    Wrapper function for checking if Tagger model is loaded.
    """
    def func_wrapper(*args, **kwargs):
        if not args[0].model:
            raise exceptions.ModelNotLoadedError()
        return func(*args, **kwargs)
    return func_wrapper



class CRFExtractor:

    def __init__(self,
        description: str = "My CRF Extractor",
        config: CRFConfig = CRFConfig(),
        embedding = None,
    ):
        self.description = description
        self.config = config
        self.feature_extractor = FeatureExtractor(config, embedding=embedding)

        self.model = None
        self.best_c_values = None


    def __str__(self):
        return self.description


    def _parse_mlp_document(self, mlp_document: dict, add_labels: bool = True, mlp_field: str = "text_mlp"):
        """
        Parses MLP output document. Extracts tokens, lemmas, and POS tags.
        Adds labels from texta_facts.
        """
        layers = self.feature_extractor.validate_and_extract_layers(mlp_document, mlp_field)
        # add labels from texta_facts
        if add_labels:
            labels = []
            texta_facts = mlp_document.get("texta_facts", [])
            for i, sentence in enumerate(layers[FEATURE_LAYER_WORD]):
                # create initial label list
                labels.append(["0" for x in range(len(sentence))])
                for fact in mlp_document["texta_facts"]:
                    if fact["fact"] in self.config.labels and fact["sent_index"] == i:
                        label = fact["fact"]
                        spans = json.loads(fact["spans"])
                        sent_str = " ".join(layers[FEATURE_LAYER_WORD][i])
                        for span in spans:
                            num_tokens_before_match = len([token for token in sent_str[:span[0]].split(" ") if token])
                            num_tokens_match = len(fact["str_val"].split(" "))
                            # replace initial labels with correct ones
                            for j in range(num_tokens_before_match, num_tokens_before_match+num_tokens_match):
                                try:
                                    labels[i][j] = label
                                except IndexError:
                                    pass
                try:
                    yield [({name:content[i][j] for name,content in layers.items()}, labels[i][j]) for j, token in enumerate(sentence)]
                except IndexError:
                    pass
        else:
            for i, sentence in enumerate(layers[FEATURE_LAYER_WORD]):
                try:
                    yield i, [{name:content[i][j] for name,content in layers.items()} for j, token in enumerate(sentence)]
                except IndexError:
                    pass


    def train(self, mlp_documents: List[dict], mlp_field: str = "text_mlp", save_path: str = "my_crf_model"):
        """
        Trains & saves the model.
        Model has to be saved by the crfsuite package because it contains C++ bindings.
        """
        # prepare data
        # a list containing tokenized documents for CRF
        token_documents = []
        for mlp_document in mlp_documents:
            for sentence in self._parse_mlp_document(mlp_document, mlp_field=mlp_field):
                token_documents.append(sentence)
        # split dataset
        train_documents, test_documents = train_test_split(token_documents, test_size=self.config.test_size)
        # featurize sequences
        X_train = [self.feature_extractor.sent2features(s) for s in train_documents]
        y_train = [self.feature_extractor.sent2labels(s) for s in train_documents]
        X_test = [self.feature_extractor.sent2features(s) for s in test_documents]
        y_test = [self.feature_extractor.sent2labels(s) for s in test_documents]
        # Test different C-values to get optimal model.
        best_f1 = 0
        best_report = None
        # Test all combinations
        for c1_value in self.config.c_values:
            for c2_value in self.config.c_values:
                # create trainer
                trainer = pycrfsuite.Trainer(verbose=self.config.verbose)
                # feed data to trainer
                for xseq, yseq in zip(X_train, y_train):
                    trainer.append(xseq, yseq)
                # set trainer params
                trainer.set_params({
                    'c1': c1_value, # coefficient for L1 penalty
                    'c2': c2_value, # coefficient for L2 penalty
                    'max_iterations': self.config.num_iter, # stop earlier
                    'feature.possible_transitions': True # include transitions that are possible, but not observed
                })
                # create temp path for the temp model
                temp_save_path = f"{save_path}_{uuid.uuid4()}"
                # train & save the model
                trainer.train(temp_save_path)
                # load tagger model for validation
                tagger = pycrfsuite.Tagger()
                tagger.open(temp_save_path)
                # evaluate model
                y_pred = [tagger.tag(xseq) for xseq in X_test]
                report = TaggingReport(y_test, y_pred, self.config.labels)
                #print(report.f1_score)
                # check if model better than our best
                if report.f1_score > best_f1:
                    # found a new best model!
                    best_f1 = report.f1_score
                    self.model = tagger
                    best_report = report
                    self.best_c_values = [c1_value, c2_value]
                    # rename temp file
                    os.rename(temp_save_path, save_path)
                else:
                    # remove temp file
                    os.remove(temp_save_path)
        # model & report to class variables
        return best_report, save_path


    @check_model_loaded
    def tag(self, mlp_document: dict, field_name: str = "text_mlp", label_suffix: str = ""):
        """
        Tags input MLP document.
        """
        facts = []
        seqs_to_predict = self._parse_mlp_document(mlp_document, add_labels=False, mlp_field=field_name)
        tokenized_text = mlp_document[field_name][FEATURE_LAYER_WORD]
        if field_name not in mlp_document:
            raise exceptions.InvalidInputError(f"Field {field_name} not present in input document!")
        sentences = [sent.split(" ") for sent in mlp_document[field_name][FEATURE_LAYER_WORD].split(" \n ")]
        # predict on each sentence
        for i, seq_to_predict in seqs_to_predict:
            # make input edible for feature extractor
            seq_to_predict = [(a, None) for a in seq_to_predict]
            features_to_predict = self.feature_extractor.sent2features(seq_to_predict)
            result = self.model.tag(features_to_predict)
            # generate text tokens for final output
            for tag in self._process_tag_output(result, sentences, i, field_name, label_suffix):
                facts.append(tag)
        out_doc = {
            field_name: {
                FEATURE_LAYER_WORD: tokenized_text
            },
            "texta_facts": facts
        }
        return out_doc


    @check_model_loaded
    def get_features(self, n=20):
        """
        Retrieves positive & negative features for the model.
        """
        info = self.model.info()
        all_feats = Counter(info.state_features).most_common()
        # filter features
        positive_features = [{"feature": f[0], "coefficient": c, "label": f[1]} for f, c in Counter(info.state_features).most_common(n)]
        negative_features = [{"feature": f[0], "coefficient": c, "label": f[1]} for f, c in all_feats[-n:]]
        return {
            "features": {
                "positive": positive_features,
                "negative": negative_features
            },
            "total_features": len(list(all_feats)),
            "showing_features": len(positive_features+negative_features)
        }


    def _process_tag_output(self, tokens: List[str], sentences: List[List[str]], sent_index: int, field_name: str, label_suffix: str = ""):
        """
        Translates result tokens into entities.
        """
        entities = []
        current_entity = []
        current_entity_type = None
        # iterate over tokens and pick matches
        for i, token in enumerate(tokens):
            if token in self.config.labels:
                entity = sentences[sent_index][i]
                current_entity_type = token
                current_entity.append(entity)
            else:
                if current_entity:
                    entities.append((current_entity_type, " ".join(current_entity)))
                    current_entity = []
        if current_entity:
            entities.append((current_entity_type, " ".join(current_entity)))
        # transform output to facts
        for fact_name, str_val in entities:
            # get spans
            tokenized_sentence = " ".join(sentences[sent_index])
            pattern = re.compile(re.escape(str_val))
            for match in pattern.finditer(tokenized_sentence):
                matching_spans = [(match.start(), match.end())]
                fact = {
                    "fact": fact_name if not label_suffix else f"{fact_name}_{label_suffix}", # if the user has specified a suffix, append it to the fact name
                    "str_val": str_val,
                    "sent_index": sent_index,
                    "doc_path": f"{field_name}.{FEATURE_LAYER_WORD}",
                    "spans": json.dumps(matching_spans)
                }
                yield fact


    def load(self, file_path: str):
        """
        Loads CRF model from disk.
        :param str file_path: Path to the model file.
        """
        tagger = pycrfsuite.Tagger()
        tagger.open(file_path)
        self.model = tagger
        return True


    def load_django(self, crf_django_object):
        """
        Loads model file using Django model object. This method is used in Django only!
        :param crf_django_object: Django model object of the Extractor.
        """
        try:
            path = crf_django_object.model.path
            # retrieve tagger info
            self.description = crf_django_object.description
            # load model
            return self.load(path)
        except:
            raise exceptions.ModelLoadFailedError()
