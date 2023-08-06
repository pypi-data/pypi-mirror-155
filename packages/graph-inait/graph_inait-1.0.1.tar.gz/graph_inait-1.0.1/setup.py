import setuptools


setuptools.setup(
    name="graph_inait",
    version="1.0.1",
    author="Jose Mielgo",
    author_email="mielgosez@gmail.com",
    description="Python graph class.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["matplotlib",
                      "h5py"]
)
