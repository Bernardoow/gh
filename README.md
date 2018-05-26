# gh

[![Build Status](https://travis-ci.org/Bernardoow/gh.svg?branch=master)](https://travis-ci.org/Bernardoow/gh) [![Coverage Status](https://coveralls.io/repos/github/Bernardoow/gh/badge.svg?branch=master)](https://coveralls.io/github/Bernardoow/gh?branch=master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/398cdbcd735a4bffaefcd3a1f9e75e84)](https://www.codacy.com/app/Bernardoow/gh?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Bernardoow/gh&amp;utm_campaign=Badge_Grade)


Crawler to Github repositories.

## First steps

Install pipenv and execute these commands:
1. Initialize the pipenv with python 3.6
    * Ex: pipenv --python 3.6
2. pipenv install
3. pipenv install -d (If you want execute reports)


## How execute the crawler?

At the root of project, we need call main.py passing three params:
- path_output_folder: Where output will be saved.
    * Ex: your/path/here

- path_input_file: Where file with repositories is saved.
    * Ex:
        1. userX/repoA
        2. userY/Brepo

- path_output_csv_file: Path to create a new csv file.
    * Ex: your/path/here/new_csv_file.csv

**python main.py path_output_folder path_input_file path_output_csv_file**

The command above just scrapy master branch. If do you want scrapy all branches you need put the command --branches.

**python main.py path_output_folder path_input_file path_output_csv_file --branches**

## How execute tests?

At the root of project, execute python -m unittest.

## How generete reports?

At the root of project execute these comands:
1. coverage run --source src setup.py test
2. coverage html