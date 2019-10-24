import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abbrevscrape",
    version="0.1.2",
    author="Alexander Dunne",
    author_email="alexdunne@gmail.com",
    description="Script that scrapes abbreviations from wiktionary.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/dunnesquared/abbrevscrape",
    packages=setuptools.find_packages(),
    # Include this line to ensure abbrevscrape is installed as a module
    py_modules=["abbrevscrape"],
    install_requires=["bs4", "requests"],
    tests_require=["nose"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # If any package contains *.txt files, include them
    package_data={'': ['*.txt']},
    include_package_data=True,
    )
