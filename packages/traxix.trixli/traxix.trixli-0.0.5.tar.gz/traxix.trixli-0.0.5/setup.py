import os
from setuptools import setup, find_namespace_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

    setup(
        name="traxix.trixli",
        version="0.0.5",
        url="https://gitlab.com/trax/trixli",
        packages=find_namespace_packages(include=["traxix.*"]),
        install_requires=required,
        scripts=[
            "traxix/again",
            "traxix/f",
            "traxix/fr",
            "traxix/fp",
            "traxix/fe",
            "traxix/ec2l",
        ],
        author="trax Omar Givernaud",
        author_mail="o.givernaud@gmail.com",
    )
