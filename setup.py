from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="cmsis-svd-codec",
    version="0.1.0",
    description="A CMSIS-SVD file encoder to generate svd files programmatically, which is useful when parsing other descriptor formats.",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/engdoreis/cmsis-svd-codec",
    author="Douglas Reis",
    author_email="engdoreis@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["lxml >= 4.9.2"],
    python_requires=">=3.9",
)