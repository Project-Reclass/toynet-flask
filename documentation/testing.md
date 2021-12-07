# Testing

## REST Calls through Chrome Devtools

Go to: `http://127.0.0.1:5000/api/value/5001`
<p align="center"> <kbd> <img src="images/values-goodID.png" width="600" /> </kbd> </p>
Open Network tab of Chrome DevTools (right click screen & click "Inspect")
<p align="center"> <kbd> <img src="images/values-goodID-200.png" width="500" /> </kbd> </p>

Go to: `http://127.0.0.1:5000/api/value/1`
<p align="center"> <kbd> <img src="images/values-badID.png" width="350" /> </kbd> </p>
Open Network tab of Chrome DevTools (right click screen & click "Inspect")
<p align="center"> <kbd> <img src="images/values-badID-404.png" width="500" /> </kbd> </p>

## Manually Testing Complex REST APIs

To send REST calls with complex body or authentication structures, you can use [Postman](https://www.postman.com/downloads/) ([tutorial](https://learning.postman.com/docs/sending-requests/requests/)) or [Insomnia](https://insomnia.rest/) ([tutorial](https://support.insomnia.rest/article/11-getting-started)) to construct the queries. For development, run the application locally using `flask run`, and set your target to `https://127.0.0.7:5000/<your api endpoint>`.

For Postman, you will need to create a personal account with your email.
Once you are logged in, you can use

<p align="center"> <kbd> <img src="images/postman-newrequest.png" width="350" /> </kbd> </p>

<p align="center"> <kbd> <img src="images/postman-buildingblock.png" width="500" /> </kbd> </p>

### (CASE 1) Body needs to be specified

You can then use the `Body` tab to provide a JSON key-value set.

<p align="center"> <kbd> <img src="images/postman-requestbody.png" width="500" /> </kbd> </p>

<p align="center"> <kbd> <img src="images/postman-tokenresponse.png" width="500" /> </kbd> </p>

### (CASE 2) Auth Token required (JWT)

You can provide the JWT token (which you grab through the login API above) in the `Auth` tab with the option `Bearer Token`.

<p align="center"> <kbd> <img src="images/postman-authtoken.png" width="350" /> </kbd> </p>

You can resuse the JWT token until it expires, and you can have different users access the API simultaneously.

<p align="center"> <kbd> <img src="images/postman-authrepeat.png" width="350" /> </kbd> </p>

## Unit Testing

Run our unit tests from the root directory:

```
$ pytest -v
```

<p align="center"> <kbd> <img src="images/pytest-pass.png" width="350" /> </kbd> </p>

When a unit test fails, the stack trace and any other error messages are printed to the console.

<p align="center"> <kbd> <img src="images/pytest-badassert.png" width="350" /> </kbd> </p>

You can use print statements to debug, and `assert True` to stub tests.

<p align="center"> <kbd> <img src="images/pytest-prints.png" width="350" /> </kbd> </p>

Print statements only show up on the console for failed tests. You can purposefully fail a test `assert False` to see print statments.

<p align="center"> <kbd> <img src="images/pytest-runprints.png" width="350" /> </kbd> </p>

## Making queries directly to SQLite

<p align="center"> <kbd> <img src="images/sqlite-viewer-upload.png" width="450" /> </kbd> </p>

Becuase we are using SQLite in development, we can upload a snapshot of the `toynet-flask/instance/toynet.sqlite` file into an online SQLite viewer such as https://inloop.github.io/sqlite-viewer/ to run queries on it.

<p align="center"> <kbd> <img src="images/sqlite-viewer-query.png" width="450" /> </kbd> </p>

**Note:** This method is recommended for manual tests (running `flask run`) as the temporary SQLite files used for unit testing are automatically deleted at the end of the test.
