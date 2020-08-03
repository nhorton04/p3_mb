import flask
from flask import request
from predictor_api import make_prediction, feature_names

app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template('index.html')

@app.route("/predict", methods=["POST", "GET"])
def predict():
    x_input, predictions = make_prediction(request.args)
    return flask.render_template('predictor.html',
                                x_input=x_input,
                                feature_names=feature_names,
                                prediction=predictions)

@app.route("/about")
def about():
    return flask.render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
