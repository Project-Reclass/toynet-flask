# Running ToyNet Flask on Windows

## Python

Install Python3.7

## venv
Create a project folder and a venv folder within:

```
$ py -3 -m venv venv
```

Before you work on your project, activate the corresponding environment:

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

## Run the service

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
