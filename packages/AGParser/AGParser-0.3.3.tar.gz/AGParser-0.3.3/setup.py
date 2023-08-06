import setuptools 

setuptools.setup(
    name="AGParser",
    version="0.3.3",
    description="Parsing library",
    long_description_content_type="text/markdown",
    author="Alexandr Grikurov",
    author_email="grikurovaa@email.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(include=["AG_Parser"]),
    include_package_data=True,
    install_requires=["pandas", "beautifulsoup4 ", "requests", "tqdm"]
)
