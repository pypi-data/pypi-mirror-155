from setuptools import setup, setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyDapi2",
    version="0.3.10",
    author="Fabrice Voillat",
    author_email="dev@dassym.com",
    keywords = ['Dassym', 'motor', 'api', 'dapi'],
    description="The PyDapi2 library offers a Python implementation of the Dassym API version 2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['lxml'],
    url="https://github.com/dassym/PyDapi2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    include_package_data=True
)