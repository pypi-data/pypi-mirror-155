from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SparkSchemafy",
    version="0.1.1",
    description="Formats spark schema output into a schema definition",
    py_modules=["SparkSchemafy"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ["pyspark >= 3.0.0 ",
                        "pandas >= 1.2.0"],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
    url="https://github.com/MichaelShoemaker/schemafy",
    author="Michael Shoemaker",
    author_email="mikeshoemaker2000@yahoo.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"]
)