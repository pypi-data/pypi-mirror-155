import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "texta-crf-extractor",
    version = read("VERSION").strip(),
    author = "TEXTA",
    author_email = "info@texta.ee",
    description = ("texta-crf-extractor"),
    license = "GPLv3",
    packages = ["texta_crf_extractor"],
    data_files = ["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description = read("README.md"),
    long_description_content_type = "text/markdown",
    url = "https://git.texta.ee/texta/texta-crf-extractor-python",
    install_requires = read("requirements.txt").strip().split("\n"),
    include_package_data = True,
    extras_require = {
        'mlp': ['texta-mlp']
    }
)
