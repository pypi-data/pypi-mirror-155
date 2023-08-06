import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orbit_etl",
    version="0.5",
    author="Benjamin Jeffrey",
    author_email="ben.jeffrey@orbitremit.com",
    description="Package for extracting data from MySQL and loading to GCS in CSV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orbitremit/orbit_etl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'pymysql',
        'google-cloud-secret-manager',
        'google-cloud-storage',
        'configparser',
        'dask',
        'dask[dataframe]'
    ]
)
