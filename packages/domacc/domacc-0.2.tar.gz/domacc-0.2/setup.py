import os

from setuptools import setup

setup(
    name="domacc",
    version="0.2",
    description="Domestic accounting python package",
    url="http://gitlab.com/pepe.bari/domacc",
    author="Pepe Bari",
    author_email="pepe.bari@gmail.com",
    license="MIT",
    packages=["domacc"],
    install_requires=["pandas"],
    zip_safe=False,
    test_suite="nose.collector",
    tests_require=["nose"],
    scripts=["bin/domacc"],
)
