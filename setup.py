from setuptools import (
    setup,
    find_packages,
)


with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="migrations",
    version="0.1.4",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    author="Trushin Pavel",
    description="Asynchronous SQL migration tool",
)
