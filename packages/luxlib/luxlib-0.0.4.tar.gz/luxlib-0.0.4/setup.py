import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="luxlib",
    version="0.0.4",
    author="Valentin Thuillier",
    author_email="valentinrthuillier@gmail.com",
    description="LuxLIB est une librairie Python permettant la mise à jour automatique depuis un serveur. Mais aussi de pouvoir mettre à jour son serveur depuis le client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheAngelLCF/LuxLIB",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)