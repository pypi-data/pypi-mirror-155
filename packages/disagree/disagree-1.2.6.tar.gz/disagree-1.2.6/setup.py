import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="disagree",
    version="1.2.6",
    author="Oliver Price",
    author_email="op.oliverprice@gmail.com",
    description="Visual and statistical assessment of annotator agreements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/o-P-o/disagree/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "disagree"},
    packages=setuptools.find_packages(where="disagree"),
    install_requires=[
        "scipy >= 1.6.0",
        "pandas >= 1.4.2",
        "tqdm >= 4.51.0"
    ],
    python_requires=">=3.6",
)
