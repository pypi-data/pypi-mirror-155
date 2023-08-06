# Welcome to the DAS Python package

The [Royal Netherlands Institute for Sea Research](https://www.nioz.nl) has its data management system to help scientists archive and access their data. This tool is called: **Data Archive System (DAS)** and this package is its Python client.

To install this package use the following command:

```powershell
    $ pip install daspython
```

# Publish this package

In order to deploy this package into pypi.org execute the following commands.

## Install the package in the local machine

```
    $  pip install -e .
```

## Install the build/ setup tools

```powershell
    $ python -m pip install --user --upgrade setuptools wheel
```

Install twine

```
    $ python pip install twine
```

Deploy the package into PyPi

```
    $ python twine upload dist/*
```

# Generate the packages

```powershell
    $ python setup.py sdist bdist_wheel
```

# Contents

1. [Authentication](#authentication)
1. [Attributes](#attributes)
    * [AttributeService](#attributeservice)
      * [Get](#get-attribute)
1. [Entries](#entries)
    * [EntryService](#entryservice)
      * [Get All](#get-all-entries)
      * [Get](#get-entry)
      * [Get Entry By Code](#get-entry-by-code)    
      * [Get Entry by Name](#get-entry-by-name)  
      * [Get Entries Level](#get-entries-level)
      * [Create Entry](#create-entry)
      * [Update Entry](#update-entry)
      * [Delete Entry](#delete-entry)
      * [Get Entry Id](#get-entry-id)
      * [Create csv template](#create-csv-template)
      * [Insert Entries from CSV](#insert-entries-from-csv)
1. [Entry Fields](#entryfields)
      * [Get All](#get-all-entryfields)
1. [Searches](#searches)
    * [SearchService](#searchservice)
      * [Search Entries](#search-entries)

The best way to see how each method is used is visiting out [automated test scripts](https://git.nioz.nl/ict-projects/das-python/-/tree/master/tests) page.

# Authentication

Use this class to authenticate and keep your token that will be needed to use with all other service classes.

##### Usage

```python
from daspython.auth.authenticate import DasAuth

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    
```