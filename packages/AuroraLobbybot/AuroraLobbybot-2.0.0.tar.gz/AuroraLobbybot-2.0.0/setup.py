import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AuroraLobbybot",
    version="2.0.0",
    author="Zockerwolf76",
    author_email="",
    description="Python package to create FN Lobbybots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={'':"src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    
)