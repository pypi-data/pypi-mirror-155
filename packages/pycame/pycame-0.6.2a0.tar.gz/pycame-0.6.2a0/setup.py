import os

from setuptools import find_packages, setup

setup(
    name="pycame",
    version="0.6.2-alpha",
    description="CAME ETI/Domo API Python client",
    long_description="CAME ETI/Domo API Python client",
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="https://github.com/lrzdeveloper/python-came-manager/issues",
    license="",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: Other/Proprietary License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ],
    packages=find_packages(exclude=["examples"]),
    python_requires=">=3.8",
    install_requires=[
        "requests~=2.26",
        "aiohttp~=3.7"
    ]
)
