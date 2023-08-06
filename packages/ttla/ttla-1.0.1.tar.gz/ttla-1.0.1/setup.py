import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    cleaned = ""
    for line in long_description.split('\n'):
        if '[![Build Status]' in line:
            pass
        elif '[![codecov]' in line:
            pass
        else:
            cleaned += line + "\n"
    long_description = cleaned

setuptools.setup(
    name="ttla",
    version="1.0.1",
    author="Ahmad Alobaid, Emilia Kacprzak",
    author_email="aalobaid@fi.upm.es",
    description="Typology-based semantic labelling of numeric columns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oeg-upm/ttla",
    packages=["detect", "label", "commons"],
    install_requires=[
        'easysparql', 'Flask', 'requests', 'rdflib', 'PPool', 'pandas', 'fuzzycmeans', 'coverage', 'chardet'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
