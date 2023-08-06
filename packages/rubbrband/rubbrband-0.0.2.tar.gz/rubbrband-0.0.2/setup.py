import os
from setuptools import setup

setup(
    name = "rubbrband",
    version = "0.0.2",
    author = "Rubbrband Inc",
    author_email = "contact@rubbrband.com",
    description = "A library to interact with the Rubbrband API.",
    long_description="A library to interact with the Rubbrband API",
    license = "BSD",
    keywords = "rubbrband cache serverless",
    url = "https://github.com/rubbrband/rubbrband-python",
    packages=['rubbrband'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)