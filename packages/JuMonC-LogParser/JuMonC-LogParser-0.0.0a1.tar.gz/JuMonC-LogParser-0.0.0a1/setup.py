import pathlib
from setuptools import setup

from JuMonC_LogParser._version import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "JuMonC_LogParser/README.md").read_text()

setup(
    name="JuMonC-LogParser",
    version=__version__,
    install_requires=["JuMonC>=0.8", "ply"],
    entry_points={
        "JuMonC": [
            "LogParser = JuMonC_LogParser.LogParser",
        ]
    },
    description="LogParser plugin for JuMonC",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.jsc.fz-juelich.de/coec/jumonc-logparser",
    author="Christian Witzler",
    author_email="c.witzler@fz-juelich.de",
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
)