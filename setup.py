import setuptools

setuptools.setup(
    name="mysql2ch",
    version="0.0.1",
    author="",
    author_email="",
    description="import mysql data into clickhouse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'clickhouse-driver',
        'PyMySQL'
    ]
)
