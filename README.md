# httpservice
This is a python http service package based on flask. This package provides a simple way to define http parameters and perform parameter verifications, also includes http api doc generation.

## Requirements

This package is for python 3 only since enum is emploied.

## Install

```
python setup.py install
```

## Usage

### Define a http service

```python
import httpservice
from flask import Flask
from flask import jsonify

class SampleParameters(httpservice.HttpParameters):
    #             type default_value is_optional allowed_values comments
    parameter1 = (int, None,         False,        None,        'comments for parameters')
    parameter2 = (str, 'iphone',     True,         ['iphone', 'ipad', 'gphone', 'gpad'])


class SampleService:

    def __init__(self):
        pass

    @staticmethod
    def get_parameters():
        return SampleParameters

    @staticmethod
    def on_get(http_parameters):
        return http_parameters

app = Flask(__name__)
@app.route("/sample/service")
def model_resource():
    return jsonify(httpservice.on_http_get(SampleService))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
```

The sample code above defines a http service on /sample/service with two parameters: parameter1 is an integer and parameter2 is a string which can only be iphone, ipad, gphone or gpad.

#### The input parameter

class SampleParameters gives following information:
- the service take 2 parameters: parameter1 and parameter2.
- parameter1 should be an integer value, any other values will cause an error.
- parameter1 is requried, not providing this parameter will cause an error.
- parameter2 is a string value which can only be one of gphone, iphone, gpad and ipad.
- parameter2 is opetional, not providing this parameter will not causing any error, but will use 'iphone' as the default value.

#### The service class

SampleService is the service class, it should provide following two static function:
- get_parameters: Aimple return SampleParameters class
- on_get: The parameter http_parameters is a dictionary, the keys are the parameter names defined in SampleParameters, the values are the value given in the request url, which are already converted to the real type. For instance, the value of parameter1 here will be integer value, not a string.

### Generate the document

```python
from httpservice.DocGenerator import DocGenerator
import app

if __name__ == '__main__':
    doc_generator = DocGenerator('doc','doc_html')
    doc_generator.add_service(app.SampleService)
    doc_generator.generate_doc()
```

The code above will read some raw documents from doc and generate the html output in doc_html.

After run the doc generator, you will find index.html on doc_html, which is the API document, also some markdown files will be generated on path 'doc'.

## Credicts

https://github.com/uvtc/rippledoc
