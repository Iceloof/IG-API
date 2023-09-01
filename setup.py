import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ig-trading-api",
    version="1.0.6",
    author="Hurin Hu",
    author_email="hurin@live.ca",
    description="Simple IG trading API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iceloof/IG-API",
    packages=setuptools.find_packages(),
    install_requires=['pytz','pandas','pycryptodome'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
