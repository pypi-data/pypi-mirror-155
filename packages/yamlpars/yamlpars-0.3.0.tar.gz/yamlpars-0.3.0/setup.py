from setuptools import setup

with open("requirements.txt") as installation_requirements_file:
    requirements = installation_requirements_file.read().splitlines()

setup(
    name="yamlpars",
    version="0.3.0",
    packages=["yamlpars"],
    url="https://github.com/matpompili/yamlpars",
    author="Matteo Pompili",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="TODO",
    install_requires=requirements,
    test_suite="tests",
    package_data={"": ["LICENSE"]},
)
