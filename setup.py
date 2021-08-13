from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def load(filename):
    # use utf-8 if this throws up an error
    return open(filename, "rb").read().decode("utf-8")


setup(
    name="gitlab_wrapper",
    version="0.0.1",
    description="Wrapper for Gitlab API v4",
    py_modules=['gitlab_wrapper.py'],
    package_dir={'': 'src'},
    packages=find_packages(),
    author="Abhay Santhosh Koduru",
    author_email="k.abhaysanthosh@gmail.com",
    url="https://gitlab.com/abhaykoduru/gitlab_client",
    install_requires=load("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ], 
    # complete list of classifiers at https://pypi.org/classifiers
    long_description=long_description,
    long_description_content_type="text/markdown",
)
