from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="ciscouctoolkit",
    version="2.126",
    author="Michael Ralston",
    author_email="michaelaaralston2@gmail.com",
    description="Cisco CUCM AXL Library, PAWS, DIME, IMP AXL, Log Collection.",
    license="MIT",
    url="https://github.com/MichaelRalston98/ciscouctoolkit",
    keywords=["Cisco", "Call Manager", "CUCM", "AXL", "VoIP"],
    packages=["UCToolkit"],
    package_data={"UCToolkit": ["*.wsdl", "*.xsd", "CUCM/*/*/*", "IMP/*/*/*", "paws/*"],},
    install_requires=[
        'xmltodict',
        'requests',
        'zeep',
        'lxml',
        'urllib3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)