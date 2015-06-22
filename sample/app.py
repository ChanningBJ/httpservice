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
