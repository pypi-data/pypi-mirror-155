import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="COMMON-SERVICE-ROF",
    version="1.0.0",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Anand Jain",
    author_email="anandjain2096@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["rof"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "rof=rof.__main__:main",
        ]
    },
)