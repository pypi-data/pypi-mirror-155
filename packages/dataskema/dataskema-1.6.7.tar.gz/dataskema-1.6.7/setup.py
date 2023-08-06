# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    readme_description = fh.read()

setup(
    name='dataskema',
    packages=['dataskema', 'dataskema.decorators'],
    include_package_data=True,  # -- para que se incluyan archivos sin extension .py
    version='1.6.7',
    description='Data schema to validate parameters easily, quickly and with minimal code',
    long_description=readme_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    author='Luis A. González Rivas',
    author_email="lagor55@gmail.com",
    license="MIT",
    url="https://github.com/lagor-github/dataskema",
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable", "Intended Audience :: Developers",
        "Operating System :: OS Independent"],
    )
