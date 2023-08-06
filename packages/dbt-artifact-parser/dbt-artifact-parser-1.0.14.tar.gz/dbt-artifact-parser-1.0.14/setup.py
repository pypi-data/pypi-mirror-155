from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="dbt-artifact-parser",
    version="1.0.14",
    description="utility package to parse dbt artifacts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zoe/dbt-artifact-parser",
    scripts=["dbt-artifact-parser"],
    author="Zoe Inc.",
    packages=["bigquery", "dbt_utils", "message", "parsers"],
    py_modules=["alert"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "google-cloud-bigquery==2.28.1",
    ],
)
