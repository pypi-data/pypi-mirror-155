from typing import List, Tuple
from enum import Enum

from . import exceptions

# define token extractor names & defaults
EXTRACTOR_ISUPPER = "isupper"
EXTRACTOR_ISTITLE = "istitle"
EXTRACTOR_HASDIGIT = "hasdigit"
EXTRACTOR_STR_LEN = "strlength"

# define feature layers & defaults
FEATURE_LAYER_WORD = "text"
FEATURE_LAYER_LEMMA = "lemmas"
FEATURE_LAYER_POS = "pos_tags"
FEATURE_LAYER_GRAMMAR = "word_features"

DEFAULT_EXTRACTORS = [EXTRACTOR_ISUPPER, EXTRACTOR_ISTITLE, EXTRACTOR_HASDIGIT, EXTRACTOR_STR_LEN]
KNOWN_EXTACTORS = [EXTRACTOR_ISUPPER, EXTRACTOR_ISTITLE, EXTRACTOR_HASDIGIT, EXTRACTOR_STR_LEN]

DEFAULT_LAYERS = [FEATURE_LAYER_WORD, FEATURE_LAYER_LEMMA, FEATURE_LAYER_POS, FEATURE_LAYER_GRAMMAR]
KNOWN_LAYERS = [FEATURE_LAYER_WORD, FEATURE_LAYER_LEMMA, FEATURE_LAYER_POS, FEATURE_LAYER_GRAMMAR]


class FeatureType(Enum):
    MAIN = "main"
    CONTEXT = "context"


class FeatureExtractor:

    def __init__(self, config, embedding=None):
        self.config = config
        self.embedding = embedding


    @staticmethod
    def str_length(string: str):
        """
        Checks whether string contrains any numbers.
        """
        return len(string)


    @staticmethod
    def has_digit(string: str):
        """
        Checks whether string contrains any numbers.
        """
        return any(chr.isdigit() for chr in string)


    def check_blacklist(self, string: str):
        """
        Checks whether token should be used as a feature.
        Returns boolean.
        """
        # TODO: Implement
        return False


    def _extract_features(self, item: dict, word_index: int, extractors_to_use: list, feature_type: FeatureType, token: str):
        """
        Extract features from token and surrounding tokens based on window size.
        """
        features = []
        # select features from selected layers
        if feature_type == FeatureType.MAIN:
            layers_to_use = self.config.feature_layers
        elif feature_type == FeatureType.CONTEXT:
            layers_to_use = self.config.context_feature_layers

        for layer in layers_to_use:
            if layer not in item:
                raise exceptions.InvalidInputError(f"Layer {layer} not present in document!")
            # extract values from Grammar layer
            if layer == FEATURE_LAYER_GRAMMAR:
                for grammar_feature in item[layer].split("|"):
                    feat_list = grammar_feature.split("=")
                    # check if list contains key & val(otherwise it's useless)
                    if len(feat_list) == 2:
                        features.append(f"{word_index}:{layer}:{feat_list[0]}={feat_list[1]}")
            # extract values from other (flat) layers
            else:
                value = item[layer].lower()
                if not self.check_blacklist(value):
                    features.append(f"{word_index}:{layer}={value}")
            # add some suffixes from token
            if layer == FEATURE_LAYER_WORD:
                for i in range(self.config.suffix_len[0], self.config.suffix_len[1]+1):
                    features.append(f"{word_index}:{layer}.suffix={value[-i:]}")
        # add ectractors
        for extractor in extractors_to_use:
            if extractor == EXTRACTOR_ISUPPER:
                feature_value = token.isupper()
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            elif extractor == EXTRACTOR_ISTITLE:
                feature_value = token.istitle()
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            elif extractor == EXTRACTOR_HASDIGIT:
                feature_value = self.has_digit(token)
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            elif extractor == EXTRACTOR_STR_LEN:
                feature_value = self.str_length(token)
                features.append(f"{word_index}:{FEATURE_LAYER_WORD}.{extractor}={feature_value}")
            # add more token-based extractors here!

        # get similar lemmas from embedding
        if self.embedding and FEATURE_LAYER_LEMMA in item:
            most_similar_lemmas = self.embedding.get_similar([item[FEATURE_LAYER_LEMMA]], n=self.config.embedding_n_similar)
            if len(most_similar_lemmas):
                for most_similar_lemma in most_similar_lemmas:
                    most_similar_lemma = most_similar_lemma["phrase"]
                    features.append(f"{word_index}:{FEATURE_LAYER_LEMMA}.embedding={most_similar_lemma}")
        # replace newlines as it breaks taggerinfo()
        features = [f.replace("\n", "") for f in features]
        return features


    def word2features(self, sent: List[tuple], i: int):
        """
        Transforms token with it's layers into features.
        I denotes the token ID in the list of tokens.
        """
        # empty list for all features
        features = []
        # add bias
        if self.config.bias:
            features.append("bias")
        # this is the current token
        item = {}
        for layer_name in self.config.feature_layers:
            item[layer_name] = sent[i][0][layer_name]
        word = sent[i][0][FEATURE_LAYER_WORD]
        features.extend(self._extract_features(item, "0", self.config.feature_extractors, FeatureType.MAIN, word))
        # check if not the first token in sentence
        if i > 0:
            for window in range(1, self.config.window_size+1):
                try:
                    item1 = {}
                    for layer_name in self.config.context_feature_layers:
                        item1[layer_name] = sent[i-window][0][layer_name]
                    word1 = sent[i-window][0][FEATURE_LAYER_WORD]
                    features.extend(self._extract_features(item1, f"-{window}", self.config.context_feature_extractors, FeatureType.CONTEXT, word1))
                except IndexError:
                    pass
        else:
            # beginning of sentence
            features.append("BOS")
        # check if not the last token in sentence
        if i < len(sent)-1:
            for window in range(1, self.config.window_size+1):
                try:
                    item1 = {}
                    for layer_name in self.config.context_feature_layers:
                        item1[layer_name] = sent[i+window][0][layer_name]
                    word1 = sent[i+window][0][FEATURE_LAYER_WORD]
                    features.extend(self._extract_features(item1, f"+{window}", self.config.context_feature_extractors, FeatureType.CONTEXT, word1))
                except IndexError:
                    pass
        else:
            # end of sentence
            features.append("EOS")
        
        return features


    def sent2features(self, sent: List[tuple]):
        # featurize everything except labels
        return [self.word2features(sent, i) for i in range(len(sent))]


    @staticmethod
    def sent2labels(sent: List[tuple]):
        # retrieve labels from tuple
        return [item[1] for item in sent]


    def validate_and_extract_layers(self, mlp_document: dict, field_name: str):
        """
        Validates the MLP document structure to have proper fields.
        """
        field_path = field_name.split(".")
        # parse field path
        for field_path_component in field_path:
            if field_path_component not in mlp_document:
                raise exceptions.InvalidInputError(
                    f"Invalid field_name param for the document. Field component {field_path_component} not found in document!"
                )
            mlp_subdoc = mlp_document[field_path_component]
        # check the resulting subdocument structure
        if not isinstance(mlp_subdoc, dict):
            raise exceptions.InvalidInputError("Document is not a dict!")
        # empty dict for layers
        layers = {}
        # always add FEATURE_LAYER_WORD because words might not me used as features,
        # but we might use the extractive features from words.
        fields_to_check = set(self.config.feature_layers + self.config.context_feature_layers + [FEATURE_LAYER_WORD])
        # check if mlp fields are present
        for field in fields_to_check:
            if field not in KNOWN_LAYERS:
                raise exceptions.InvalidInputError(f"Field '{field}' is an unknown MLP field!")
            if field not in mlp_subdoc:
                raise exceptions.InvalidInputError(f"Field '{field}' not present in the document!")
            # add layer if not present
            if field not in layers:
                layers[field] = []
            # split field into sents
            # use "LBR" as sentence break marker for POS tag layer
            if field in (FEATURE_LAYER_POS, FEATURE_LAYER_GRAMMAR):
                sentences = mlp_subdoc[field].split(" LBR ")
            else:
                sentences = mlp_subdoc[field].split(" \n ")
            # add sent to layer
            for sentence in sentences:
                sentence_tokens = sentence.split(" ")
                layers[field].append(sentence_tokens)
        return layers
