import setuptools

setuptools.setup(
    name="nerdler_tc",
    version="1.0.1",
    description="Clean text from special characters and blanks",
    long_description="This module provides a simple class to remove special chars (ex. Ä -> A, ö -> o) from a string. It also removes blanks and tabs.",
    author="nerdler_pt",
    author_email="no-reply@nerdler.pt",
    packages=["nerdler_tc"],
    url="https://www.nerdler.pt",
    license="MIT",
    platforms="any"
)