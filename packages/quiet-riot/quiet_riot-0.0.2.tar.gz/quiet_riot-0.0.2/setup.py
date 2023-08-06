import setuptools

requires = ["setuptools>=42",
                 "wheel",
                 "boto3==1.17.84"]


REQUIRES = [
                "setuptools>=42",
                 "wheel",
                 "boto3==1.17.84"
]
setuptools.setup(
    name="quiet_riot",
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    package_data={'quiet_riot': ["results/*.txt","wordlists/*.txt","*.txt"]},
    install_requires=REQUIRES,
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "src"},
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
)
