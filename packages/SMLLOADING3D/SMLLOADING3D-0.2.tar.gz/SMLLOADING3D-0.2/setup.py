from setuptools import setup

with open("README.md", "r") as fh:
    long_description=fh.read()
setup(
    name="SMLLOADING3D",
    version="0.2",
    description="loading 3D",
    py_modules=["Loading3D"],
    package_dir={"": "src"},
    classifiers=[
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["numba"],
    license="LICENSE.txt",
    author="Mr. Hanh",
)