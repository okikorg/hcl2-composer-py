from setuptools import setup, find_packages

setup(
    name="py2hcl2",
    version="0.0.9",
    description="A package for generating HCL blocks in Python",
    author="Okik",
    author_email="hello@okik.co.uk",
    url="https://github.com/okikorg/py2hcl2",  # Update with your actual GitHub URL
    packages=find_packages(),
    install_requires=[
        "pydantic>=1.8.2",  # Specify required dependencies
        "rich>=10.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
