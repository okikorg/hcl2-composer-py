from setuptools import setup, find_packages

__version__ = "0.0.9"

# Read requirements.txt and store contents in a list
with open("./requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="py2hcl2",
    version=__version__,
    packages=find_packages(),
    author="Okik",
    author_email="hello@okik.co.uk",
    description="HCL2 code generator for Terraform",
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
