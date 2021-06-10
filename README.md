# toynet-flask
Backend service of ToyNet emulator and learning platform

Created with:
- https://flask.palletsprojects.com/en/1.1.x/ for application structure and SQLite database (will become PostgreSQL)
- https://flask-restful.readthedocs.io/en/latest/quickstart.html for Flask-RESTful
- https://flask.palletsprojects.com/en/1.1.x/testing/ for pytest

# Requirements

## Python

Install Python3.7

## venv
Create a project folder and a venv folder within:

Linux / MacOS:
```
$ git clone https://github.com/Project-Reclass/toynet-flask
$ cd toynet-flask
$ python3 -m venv venv
```

On Windows:
```
$ py -3 -m venv venv
```

Before you work on your project, activate the corresponding environment:

Linux / MacOS:
```
$ . venv/bin/activate
```

On Windows:
```
> venv\Scripts\activate
```

Install Python Requirements (add new requirements via `pip3 freeze > requirements.txt.`)
```
$ pip3 install -r requirements.txt
```

You can exit this virtual environment anytime via running:
```
$ deactivate
```

More information [here](https://docs.python.org/3/library/venv.html)

# Run the service

MacOS / Linux:
```
$ export FLASK_APP=flasksrc

# restarts server after code changes
$ export FLASK_ENV=development

# creates instance/toynet.sqlite
$ flask init-db 
Initialized the database.

$ flask run
 * Serving Flask app "flasksrc" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 220-725-712
 ```

Windows:
```
> set FLASK_APP=flasksrc
> set FLASK_ENV=development
> flask init-db
> flask run
```

Windows PowerShell:
```
> $env:FLASK_APP = "flasksrc"
> $env:FLASK_ENV = "development"
> flask init-db
> flask run
```

Go to: `http://127.0.0.1:5000/`
<p align="center"> <kbd> <img src="documentation/images/hello-reclass.png" width="300" /> </kbd> </p>

# Test the Service

Visit [testing documentation](documentation/testing.md).

# Troubleshooting

**Q: How do I use a table I added in `schema.sql` or `seed_data/<resource>.sql`?**<br/>
A: Delete instance/toynet.sqlite and run flask init-db again.

**Q: How do I get rid of a table?**<br/>
A: Delete `instance/toynet.sqlite` and run `flask init-db` again.

**Q: I added a test file but it isn't being picked up by pytest**<br/>
A: Make sure the file is named `test_***.py`

# Swagger API Documentation
Swagger is a useful tool that will automate our API documentation as well as
facilitate arguments checking for missing values passed to Flask.
In order to make use of Swagger you must do five things:
1. When modifying the `__init__.py` to include your new API endpoints, also add
   a line that registers them with Swagger:
```python
docs.register(YourApiEndpointClass)
```
2. Make sure that your source file imports:
```python
from marshmallow import Schema, fields, ValidationError
from flask_apispec import marshal_with, MethodResource
from flask import request # if you are loading fields from a POST body, for instance
```
3. Ensure that your class (`YourApiEndpointClass` above) inherits from
   `MethodResource` instead of `Resource`
4. Define your request/response schemas, specifically the fields that are
   present and their types. You can look at the beginning of
   `flasksrc/session.py` for examples. If a field is required in a request (not
   a response) you can specify `required=True`.
5. For methods using the schema for the HTTP request, add the decorator
   `@marshall_with(YourApiEndpointClassHttpMethodSchema)` that you defined for
   it

A good example file is `flasksrc/sessions.py`.

## Viewing API Specification
After running your Flask deployment, you will be able to vie the raw JSON
specification at `localhost:5000/swagger/`
If you want to have a more graphical depiction of the specification, you can
browse to `localhost:5000/swagger-ui/`

One approach is to curl the endpoint and pipe the JSON output into `jq` for
syntax-highlighted output:
```bash
curl http://localhost:5000/swagger/ | jq
```
<p align="center"> <kbd> <img src="documentation/images/curl_swagger.png" width="300" /> </kbd> </p>

You can also browse to the url:
<p align="center"> <kbd> <img src="documentation/images/browser_swagger-ui.png" width="300" /> </kbd> </p>
From here, you can click on resources for additional information in a more visual interface:
<p align="center"> <kbd> <img src="documentation/images/browser_swagger-ui_detailed.png" width="300" /> </kbd> </p>
You can also scroll to the bottom and view the model specifications, expanding fields as needed:
<p align="center"> <kbd> <img src="documentation/images/browser_swagger-ui_models_detailed.png" width="300" /> </kbd> </p>

After writing your specification schemas, marking the endpoints to be
documented, and properly adding decorators and parent classes to the API
resources, you should confirm that the Swagger documentation matches what you
expect at these two resources.

# FYIs

**1. We have not rigorously tested different `USER_GROUP_ID`s.**
