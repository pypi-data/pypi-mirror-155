# Rubbrband Python Library

The Rubbrband Python library provides convenient access to the Rubbrband API from applications written in Python. It includes a class for API resources that clients can initialize with their API key, which they can retrieve from https://dashboard.rubbrband.com.

## Documentation

See the Python API docs here.

## Installation

You do't need this source code unless you want to change the package. To install the package and use it, just run

`pip install --upgrade rubbrband`

## Requirements

Python 2.7+ or Python 3.4+

## Usage

The library needs to be configured with your accounts' API key which is available in your Rubbrband Dashboard.

```
import rubbrband
rubbrband.api_key = "rb_test_..."

# get a cache entry
user = rubbrband.replay("user_1")

# remove a cache entry
rubbrband.delete("user_1")

# add a new entry
rubbrband.put("user_2", {'name': 'Jiminee Cricket'})
```
