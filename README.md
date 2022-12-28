# ToyNet Flask
This is the Backend service of the ToyNet emulator and learning platform.

### Requirements
The following tutorial applies to Linux/MacOS development environment. 
For Windows OS: Visit Windows documentation [here](documentation/windows.md).

### Python
Install [Python3.7](https://www.python.org/downloads/)

## venv - Virtual Environments
This will create a project folder and a venv folder within:
```
$ git clone https://github.com/Project-Reclass/toynet-flask
```
```
$ cd toynet-flask
```
```
$ python3 -m venv venv
```

Before you work on your project, activate the corresponding environment:
```
$ . venv/bin/activate
```

Install the Python Requirements (add new requirements via: `$ pip3 freeze > requirements.txt`)
```
$ pip3 install -r requirements.txt
```

You can exit this virtual environment at anytime via running:
```
$ deactivate
```

Look here for more information on [venvs](https://docs.python.org/3/library/venv.html).
___

## ToyNet Docker Image

From there, make sure to build the toynet [docker](https://www.docker.com) image from the `toynet_mininet` directory.   
*Make sure* you tag it with the same tag you use for the below environment variable for `TOYNET_IMAGE_TAG`.   

First you will need to download mininet. You can do this by initializing the submodule with these commands:
```
$ cd toynet_mininet
```
```
$ git submodule update --init --recursive
```



You will then need to build the image which will work with the top-level Makefile (refer to note in the Makefile section below). The default way is to go into the `toynet_mininet` submodule and run one of the following, also in the `toynet_mininet` directory:

##### *If you want a TEST(dev) image then run:*
```
$ make test-image
```

##### *If you want a PRODUCTION(prod) image then run:*
```
$ make prod-image
```


**Note:** See the [toynet_mininet README](https://github.com/Project-Reclass/toynet-flask/blob/main/toynet_mininet/README.md) for more information on building and developing `toynet_mininet`.

_____
## Run the service
**Make sure that if you are testing anything related to sessions or network emulation, that you build the appropriate image (dev or prod) in `toynet-mininet`.**

### Requirements
The following tutorial applies to Linux/MacOS development environment. 
For Windows OS: Visit Windows documentation [here](documentation/windows.md).

To go back to the toynet-flask directory, type: 
```
$ cd .. 
```

Populate environment variables for testing:
```
$ source environment/env-dev
```

Populate environment variables for production:
```
$ source environment/env-prod
```

Create the reclass_network:
```
$ docker network create reclass_network
```

Create the instance/toynet.sqlite:
```
$ flask init-db 
```

Now you can initialized the database with:
```
$ flask run
```
After you have entered `flask run`, you should see the following in the terminal:
```
 * Serving Flask app "flasksrc" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 220-725-712
```

Click on `http://127.0.0.1:5000/` to open the program in your browser.
<p align="center"> <kbd> <img src="documentation/images/hello-reclass.png" width="300" /> </kbd> </p>

_____

### About the Makefile
The `Makefile` facilitates common workflows. You can use the Makefile to run everything in Docker containers, as opposed to running Flask locally as described above. The Makefile has build targets that build the Docker image and other build targets that run the image as a container. 

**Note:** Run the command below for more detailed instructions about the build targets to help understand the above steps. The instructions above are basically saying that the commands listed or building the image are compatible with how the Makefile works (specifically, that they will tag the images in a way that other Makefile commands will also work). 
```
$ make help
```

___ 
### About Swagger API Documentation

Visit [swagger documentation](documentation/swagger.md) to generate living documentation about available API endpoints alongside your flask instance.

### To Learn how to Test the Service

Visit [testing documentation](documentation/testing.md) to learn how to unit test, run manual tests in development, and query SQLite files.

___
## Dependencies

This project was created using:
- [Pallet Projects Flask Tutorial](https://flask.palletsprojects.com/en/1.1.x/) for application structure and SQLite database (will become PostgreSQL)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/quickstart.html) for Flask-native restful API
- [Pallet Projects Testing Tutorial](https://flask.palletsprojects.com/en/1.1.x/testing/) for pytest
- [Swagger](https://swagger.io/) for autogenerated API documentation
- [Argon2](https://argon2-cffi.readthedocs.io/en/stable/argon2.html) for password hashing
- [User Authentication & Authorization Tutorial](https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935), [Using JWT in pytest Stack Overflow](https://stackoverflow.com/questions/46846762/flask-jwt-extended-fake-authorization-header-during-testing-pytest) for authentication / authorization
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html) & [Marshmallow Tutorial](https://www.cameronmacleod.com/blog/better-validation-flask-marshmallow) for parsing REST request body
___

## For Troubleshooting

**Q: How do I use a table I added in `schema.sql` or `seed_data/<resource>.sql`?**<br/>
A: Delete instance/toynet.sqlite and run flask init-db again.

**Q: How do I get rid of a table?**<br/>
A: Delete `instance/toynet.sqlite` and run `flask init-db` again.

**Q: I added a test file but it isn't being picked up by pytest**<br/>
A: Make sure the file is named `test_***.py`

___

## FYIs

1. We have not rigorously tested different `USER_GROUP_ID`s.**   
2. This project is licensed under [GPLv3](/LICENSE)
3. We would like to acknowledge our amazing Contributors for all of there help with Project Reclass:
    * Tay Nishimura
    * John Chung
    * Arthur Lacey
    * Blaze Bissar
    * Shaili Smith
    * Yujing Gao
    * Berkan Yilmaz   


