# toynet-flask
Backend service of ToyNet emulator and learning platform

# Requirements

## Python

Install Python3.7

## venv
Create a project folder and a venv folder within:

Linux / MacOS:
```
$ mkdir myproject
$ cd myproject
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
pip3 install -r requirements.txt
```

# Run the service

MacOS / Linux:
```
$ export FLASK_APP=flasksrc
$ export FLASK_ENV=development // restarts server after code changes
$ flask run
 * Running on http://127.0.0.1:5000/
 ```

Windows:
```
> set FLASK_APP=flasksrc
> set FLASK_ENV=development // restarts server after code changes
> flask run
```

Windows PowerShell:
```
> $env:FLASK_APP = "flasksrc"
> $env:FLASK_ENV = "development" // restarts server after code changes
> flask run
```

![Running App](https://github.com/Project-Reclass/toynet-flask/blob/main/images/hello-reclass.png)