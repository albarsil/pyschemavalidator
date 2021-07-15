# pyschemavalidator

This package contains a decorator for endpoints in flask and a way to validate dictionary/JSON elements. 
It omits the need to validate the data yourself and allow its usage by other kinds of APIs like graphql through the `UniversalValidator`.

## Installation

Use pip to install the package from PyPI:

```bash
pip install pyschemavalidator
```

## Usage

This package provides a flask route decorator to validate a JSON payload or dictionary elements.

```python
from flask import Flask, make_response, jsonify, g, url_for
from pyschemavalidator import validate_param

# example imports
from models import Model

app = Flask(__name__)

@app.route('/invocations', methods=['POST'])
@validate_param(key="sepal_length", keytype=float, isrequired=True)
@validate_param(key="sepal_width", keytype=float, isrequired=True)
@validate_param(key="petal_length", keytype=float, isrequired=True)
@validate_param(key="petal_width", keytype=float, isrequired=True)
def register():
    # if the payload is invalid, the request will be aborted with the appropriate error code

    # do model inference
    data = request.get_json(silent=True, force=False)
    
    output = Model.predict(data.get('sepal_length'), data.get('sepal_width'), data.get('petal_length'), data.get('petal_width'))
    return make_response(jsonify({"output:": output}), 200)
```

The payload is verified through the parameters set on the decorators. If the body does not meet the decorator's specifications it returns a standard response with the appropriate error code.

You can also use the package without the decorator style as below:

```python
from pyschemavalidator.validators import UniversalValidator

# Creates a Universal validator to the dictionary/JSON elements
request_validator = UniversalValidator()
request_validator.add(key="example1", keytype=str, isrequired=True)
request_validator.add(key="example2", keytype=str, isrequired=False)

# Example data
data = {"example1": "test", "example2": "test"}

# Add some validations to the JSON/dictionary element
status_code, message = request_validator.validate(
    tag1=data.get("example1"),
    tag2=data.get("example2")
)

if status_code != 200: # It means that something got wrong with the validation
    raise ValueError(message)
else
    ... # Do whatever you want
```


## Mimetype checking

As of 1.2.0 this decorator uses `flask.request.get_json(force=False)` to get the data. This means the mimetype of the request has to be 'application/json'.

## Error handling

On validation failure, the library calls `flask.make_response` and passes the error code and the message.

## Testing

The following are the steps to create a virtual environment into a folder named "venv" and install the requirements.

```bash
# Create virtualenv
python3 -m venv venv
# activate virtualenv
source venv/bin/activate
# update packages
pip install --upgrade pip setuptools wheel
# install requirements
python setup.py install
```

Tests can be run with `python setup.py test` when the virtualenv is active.

# Changelog

1.0.3 - Fix description and README

1.0.2 - Fix the missing required parameter issue

1.0.1 - Fix the bonduaries issue

1.0.0 - First release