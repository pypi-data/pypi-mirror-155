import sys

from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 9)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""WARNING: This package has only been validated on Python 3.9+.""")

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "numpy==1.22.4",
    "pandas==1.4.2",
    "python-dateutil==2.8.2",
    "pytz==2022.1",
    "six==1.16.0"
]

setup(
    name="scd_type2",
    version="0.1.0",
    author="Zac Clery",
    author_email="zacclery@gmail.com",
    description="Simplifies and unifies the logic for performing SCD type 2 data comparisons.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=requires,
    keywords='scd type2 scd_type2 slowly changing dimensions slowly-changing-dimensions',
    entry_points={
        'console_scripts': [
            'scd_type2=scd_type2.__main__:main',
            'scd=scd_type2.__main__:main',
        ],
    },
)
