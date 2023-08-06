import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setup(
    name="hiddenlayer-python",
    version="0.0.3",
    packages=find_packages(),
    include_package_data=True,
    description="HiddenLayer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.github.com/hiddenlayersec/hiddenlayer-python",
    author="HiddenLayer",
    author_email="contact@hiddenlayer.com",
    install_requires=["requests", "numpy", ""],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
)
