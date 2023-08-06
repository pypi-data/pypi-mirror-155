from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name="daspython",
    version='1.1.0',
    author='Royal Netherlands Institute for Sea Research',    
    url='https://git.nioz.nl/ict-projects/das-python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
