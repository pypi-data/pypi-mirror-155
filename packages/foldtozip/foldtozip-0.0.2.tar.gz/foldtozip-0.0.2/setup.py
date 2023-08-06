from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="foldtozip",
    version="0.0.2",
    author="Coder100",
    author_email="jacobhason86@gmail.coù",
    description="No description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheGamer548/FoldToZipt",
    project_urls={
        "Source-code": "https://github.com/TheGamer548/Pikkit",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)