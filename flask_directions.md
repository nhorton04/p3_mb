# Flask Demo

Check out the tiny app in [app.py](app.py). We're going to go through this *very* simple example to illustrate at the most basic level what Flask is doing. Let us take the code step by step here:

## Set up Instance

```python
# minimal example from:
# http://flask.pocoo.org/docs/quickstart/

from flask import Flask

app = Flask(__name__)  # create instance of Flask class
```

First, we create an instance of the [Flask](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask) class. This creates a Web Server Gateway Interface ([WSGI](https://www.fullstackpython.com/wsgi-servers.html)) using default settings (consider the folders and files in the directory, global variables, etc.), so that your Python instance can control some application that runs on the web. In the words of fullstackpython.com:

*"WSGI is by design a simple standard interface for running Python code. [...] you won't need to know much more than*

* *what WSGI stands for (Web Server Gateway Interface)*

* *that a WSGI container is a separate running process that runs on a different port than your web server*

* *your web server is configured to pass requests to the WSGI container which runs your web application, then pass the response (in the form of HTML) back to the requester"*

## Define Flask Object

Next, we'll make changes to the `app` object to make our webapp. Remember, in the WSGI, we need to make translations between HTML and Python, and we need to define locations in our environment. Here, we provide the first option (the main index) for the Web Server to route to, and what the output will be.

```python
@app.route('/')  # the site to route to, index/main in this case
def hello_world() -> str:
    """Let's say Hi to the world.

    Returns:
        str: The HTML we want our browser to render.
    """

    return 'Hello World!'
```

Our web app is starting out really small. We are only building a single page on it, the index page. `@app.route('/')` is a decorator that tells the app to run the following function whenever anyone navigates to that page. The function returns the HTML we want to load (in this case, just the text *"Hello World!"* under the default CSS settings).

## Setup For Scripting

Now, given these instructions, we define the conditions under which the script can run as default. That is, only when we run the file as a script (e.g., using `$ python app.py`) will it activate the web app.

```python
if __name__ == '__main__':
    app.run()
```
The `__name__` here is the name of the Python instance. When running as its own script, the Python instance has the name `"__main__"`. If you're running the file as module, it will have a different name, since it's being called from another module.

Check out [this](http://thepythonguru.com/what-is-if-__name__-__main__/) article for more.

## Running the App

Run the app by `cd`-ing into the directory where `app.py` lives. Then run

```
python app.py
```

You should see something like

```
* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

And then you can load up http://127.0.0.1:5000/ in your browser. Woot!

# Creating a Model-Driven Web App

For our full-fledged model-driven web app to function, we need to create a directory from which to run our app. We need to define a directory because there will be more files for the WSGI to reference than just the vanilla `app.py` as we've done above. Set up a folder (maybe call the folder something like `/predictor_app` like so

```
/predictor_app
  /models        <-- We'll put our model(s) in here
  /templates     <-- The WSGI uses this to build HTML
  ...            <-- We will save a few Python files here
```

I'll call the `/predictor_app` folder our "main directory" going forward.

## Step 1. Save a model

The purpose of a web app is to allow others to access and use some model you've created, on the web. Check out the notebook where we train and store a model that predicts the species of flower based on attributes [here](train_save_model.ipynb).

## Step 2.a. Load the Model

The model that we trained and saved is going to be used to make predictions. So, we need to have it primed and ready for the web app to access! Of course, the model should have been saved (or copied) into the `/models` folder.

In the main directory, create a "worker" script called `predictor_api.py`. *(Note: This file itself is not an API on its own, per se, but the concept is there, so the nomenclature is appropriate enough).*

In this file, we first need to load the model that was saved in the previous step, as well as feature names to be used in processing.

```python
import pickle as pkl
import numpy as np

# lr_model is our simple logistic regression model
# lr_model.feature_names are the four different iris measurements
with open("./models/lr.pkl", "rb") as f:
    lr_model = pkl.load(f)

feature_names = lr_model.feature_names
```

It's important to note that we load these as **global variables** so that they exist in memory once and for all when the page is loaded. You wouldn't want to have to re-load the model every time a prediction is warranted -- the model and the feature names are shared for all potential predictions, so this saves time.

## Step 2.b. Predict on New Data

Now that the model is loaded, we need to be able to use it to predict on new data, or on data that is **POST**ed by the user of the web app. That is, we need to create a function that will

1. ... translate the JSON content of the user's POST request (from Flask) into something the model can read
2. ... make a prediction on the new data
3. ... send the results back to the Flask app in a form it can use

Let's create a function in this file called `make_prediction` to accomplish these steps. Our Flask app can finalize the POST request using this function as an intermediate step.

From the user of the web app, we will receive a dictionary (originally a JSON), `feature_dict`, that might look like

```python
# This `feature_dict` is the only parameter for our function
feature_dict = {
  'sepal length (cm)': 0,
  'sepal width (cm)': 1.2,
  'petal length (cm)': 1.9,
  'petal width (cm)': 0
}
```

We only need the actual values themselves, but we need them in the correct order to feed into the model. Recall that we *saved* this order inside the model as `.feature_names`. So, to get everything in order

```python
x_input = []
for name in lr_model.feature_names:
    x_input_ = float(feature_dict.get(name, 0))
    x_input.append(x_input_)
```

The `mydict.get(item, default)` syntax will go into the dictionary `mydict` and try to return `mydict[item]`. If `item` is not a key for `mydict`, it will return `default`. (The default value for `default` is `None`, but in this case we set it to 0.) This is helpful for situations (like this) where we're not sure if the user is going to input some funny value that doesn't make sense.

Now, we can get the probabilities to report on.

```python
pred_probs = lr_model.predict_proba([x_input]).flat
```

Remember, `.predict_proba` expects a matrix. In this case, we're giving it a "matrix" (array) with one row, namely the one we want to predict on.

Lastly, we want to present our results (the class probabilities) in descending order of probability. We'll reuse the `[::-1]` step syntax to get the list in reverse order.

```python
probs = []
for index in np.argsort(pred_probs)[::-1]:
    prob = {
        'name': lr_model.target_names[index],
        'prob': round(pred_probs[index], 5)
    }
    probs.append(prob)
```

Recall that `np.argsort(a)` returns the indices of `a` which would sort it in ascending order.

Finally, we want to return both the users' input (`x_input`) as well as the probabilities (`probs`). This is so that we can refill the text boxes with the given input (after completing the POST), and of course show the result, respectively.

```python
...
return (x_input, probs)
```

## Step 2.c. Capturing data for the web app

Create a new app file named `predictor_app.py` and save it in our main directory (use our last app as a template). This is our Flask app. In this file, we need to create a function which takes in the data from the POST request, transforms it into something the predictor function can read, and then sends back the results of the function. First, add these imports:

```python
from flask import request
from predictor_api import make_prediction, feature_names
```

Then, add a new route like the one below.

```python
@app.route("/predict", methods=["GET", "POST"])
def predict():
    pass
```

This `/predict` route allows GET and POST requests, which is what we need to either load the page (GET) or post data to get predictions (POST).

Replace the `pass` in the code above with

```python
x_input, predictions = make_prediction(request.args)
```

(`flask.`)`request.args` contains all the arguments passed by our form, and it comes built in with Flask. It is a **list** of dictionaries of the form `{form_name_defined_in_template: form_value}`.

Now, we will return

```python
return flask.render_template('predictor.html',
                             x_input=x_input,
                             feature_names=feature_names,
                             prediction=predictions)
```

We will use these **user-defined** `x_input`, `feature_names`, and `prediction` values later in defining a *template* HTML code for the app. Make sure that at the end of the file, you're setting the contingency for `__name__` to be `"__main__"` before running the app.

```python
# For local development:
if __name__ == '__main__':
    app.run(debug=True)
```

## Step 3.a. Understanding Templates

Now that we have access to the model we saved, given some user input, we need to create a web page that users can interact with. Flask uses a template engine to allow us to render webpages in response to the data in the app (e.g., prediction results). Refer to the documentation for [Jinja2](http://jinja.pocoo.org/docs/2.10/) when you build your apps.

Say we want to build a list. Normally in HTML, we would do this like so:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <title>My Webpage</title>
</head>

<body>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
  </ul>
</body>
</html>
```

In Flask, we can use a template engine to build a list with code:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <title>My Webpage</title>
</head>

<body>
  <ul>
    {% for i in range(1,4) %}
        <li>Item {{ i }}</li>
    {% endfor %}
  </ul>
</body>
</html>
```

In the `/templates` folder, copy-paste this code into an HTML file called something like `predictor.html`. Now, in your `predictor_app.py` file, replace `return 'Hello World!'` with `return flask.render_template('predictor.html')`. Run the app with `python predictor_app.py` and see what happens when you go to that page!

Verify that if you change the range, the list changes too. (You may need to refresh the page after changing your HTML file.)

### Step 3.b. Understanding Forms

To do this step, we're going to first look at forms. Here's a form block that comes from w3schools.

```html
<form action="/action_page.php">
  First name:<br>
  <input type="text" name="firstname" value="Mickey">
  <br>
  Last name:<br>
  <input type="text" name="lastname" value="Mouse">
  <br><br>
  <input type="submit" value="Submit">
</form>
```

It has a few parts:
- The `<form action="/action_page.php"></form>` tag is a wrapper around the rest of the form. It includes the `action` attribute which tells us where to send the results of the form when we're through (the '/' syntax matches what you see in the `_app.py` file in the `@app.route` decorator functions).
- Within that form are standard HTML elements like text and `<br>` tags for line breaks.
- The `<input type="text" name="lastname" value="Mouse">` tag gives us an text field whose default `value` is "Mouse". We'll use this to grab user input. The `name` attribute tells us how to refer to the input block. Make sure that each `<input>` tag has a unique name. Also, note that `<input>`s are self-closing.
- The `<input type="submit" value="Submit">` tag is a special input that renders as a submit button.

### Step 3.c. Incorporating Templates and Forms to build a web page

To start off the template, make sure that your HTML file contains the normal `<DOCTYPE>`, `<html>`, and `<head>` tags (it should if you got Step 3.a. to work). Next, let's create a form which will send/receive information to/from our `/predict` route in the `.app` file.

```html
<form action="/predict">
  {% for f in feature_names %}
      <br>
      {{ f }}
      <br>
      <input type="text" name="{{ f }}" value="{{x_input[loop.index0]}}">
  {% endfor %}
  <br>
  <input type="submit" value="Submit" method="get">
</form>
```

This `loop.index0` syntax can be best understood from the [Jinga documentation on for loops](https://jinja.palletsprojects.com/en/2.10.x/templates/?highlight=index0#for). This syntax is equivalent to the `for i, x in enumerate(mylist)`, where the `i` is represented as `loop.index0`.

Secondly, we'll need a place to put the results. Below this form, we'll have a place for the predictions to go

```html
<p>
  prediction:
  {% for p in prediction %}
    <br>  {{ p['name'] }} ...... {{ 100 * p['prob'] | round(4) }}%
  {% endfor %}
</p>
```

Note how we used the `x_input`, `feature_names`, and `prediction` values from before. Again, you can check out the `| round` syntax [here](https://jinja.palletsprojects.com/en/2.11.x/templates/#round).

Fire up the app with `python predictor_app.py`, go to the predict page [http://localhost:5000/predict](http://localhost:5000/predict), and try it out by changing a few values. What do you notice changes when you click submit?

As usual, the [Flask Docs](http://flask.pocoo.org/docs) and the [Jinja Docs](https://jinja.palletsprojects.com/) are your friends.

# Further Exercises

- Modify the app to output the predicted class (so 'setosa' instead of [0]).
- This is a somewhat ugly app, can you make it prettier?
- Check out the [cancer app](cancer_app) for a preview of what we can do with D3.

<h1 style="color:red">Important Presentation Note!</h1>

If you plan on presenting a project which uses a web app, make sure you video tape your demo for presentation instead of doing it real time! You never know what's going to happen, so put your best foot forward :)
