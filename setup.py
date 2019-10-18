import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wiktionary_abbreviation_scraper",
    version="0.1.0",
    author="Alexander Dunne",
    author_email="author@example.com",
    description="Script that scrapes abbreviations from wiktionary.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL 3.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
