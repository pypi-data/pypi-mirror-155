import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="u-google-driver",
    version="81.0.4044.138",
    author="seal",
    author_email="seal.xu@qq.com",
    description="seal u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=2.7',
)


import re
