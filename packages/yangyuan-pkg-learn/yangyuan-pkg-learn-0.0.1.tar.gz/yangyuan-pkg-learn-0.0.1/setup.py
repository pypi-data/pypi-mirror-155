import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "yangyuan-pkg-learn",
    version = "0.0.1",
    author = "Yuan Yang",
    author_email = "messiyuan16@gmail.com",
    description = "The first example pkg build for learn",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/yangyuan0107/packaging_tutorial",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent ",
    ],
)