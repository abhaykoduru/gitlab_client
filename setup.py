import codecs
import os.path
import re
from setuptools import setup, find_packages


# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))


# The text of the README file
README = (HERE / "README.md").read_text()


def load(filename):
    # use utf-8 if this throws up an error
    return open(filename, "rb").read().decode("utf-8")


def read(*parts):
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="gitlab_v4",
    version="0.0.3",
    description="Wrapper for Gitlab API v4",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abhaykoduru/gitlab_client",
    author="Abhay Santhosh Koduru",
    author_email="k.abhaysanthosh@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["gitlab_client"],
    include_package_data=True,
    install_requires=load("requirements.txt")
)
