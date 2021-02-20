# Simple web crawler

This is a simple web crawler based on a breadth-first approach. It takes a start URL and the depth as arguments. It follows only URLs with the same domain as the start URL; prints out the links to the screen; and saves the results to a JSON file called `data.json`.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

```
$ git clone https://github.com/felipemarineli/WebCrawler.git
```

### Prerequisites

- [Python 3.8.2](https://www.python.org/downloads/release/python-382/)

### Installing

Make sure there is an up-to-date version of [pip](https://pip.pypa.io/en/stable/) installed

```
$ pip3 install --upgrade --user pip
```

Install a [virtual environment](https://virtualenv.pypa.io/en/latest/) under `/WebCrawler`

```
$ cd ./WebCrawler
$ python3 -m venv env
```

Activate the virtual environment

```
$ source env/bin/activate
```

Install requirements.txt

```
$ pip install -r requirements.txt
```

### Usage:

The call takes two arguments: *start_url* and *depth*
```
$ python main.py "https://www.sciencemag.org/" 2
```                                
