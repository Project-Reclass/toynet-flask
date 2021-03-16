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

## REST Calls where Body needs to be specified

To send REST calls to local application, you can use something like [Postman](https://www.postman.com/downloads/) ([tutorial](https://learning.postman.com/docs/sending-requests/requests/)) or [Insomnia](https://insomnia.rest/) ([tutorial](https://support.insomnia.rest/article/11-getting-started)).

For Postman, you will need to create a personal account with your email.
Once you are logged in, you can use

<p align="center"> <kbd> <img src="images/postman-newrequest.png" width="350" /> </kbd> </p>

<p align="center"> <kbd> <img src="images/postman-buildingblock.png" width="500" /> </kbd> </p>

You can then use the `Body` tab to provide a JSON key-value set.

<p align="center"> <kbd> <img src="images/postman-requestbody.png" width="350" /> </kbd> </p>

<p align="center"> <kbd> <img src="images/postman-requestresponse.png" width="500" /> </kbd> </p>


## Unit Testing

Run our unit tests from the root directory:

```
$ pytest -v
```

## Making queries directly to SQLite

<p align="center"> <kbd> <img src="images/sqlite-viewer-upload.png" width="450" /> </kbd> </p>

Becuase we are using SQLite in development, we can upload a snapshot of the `toynet-flask/instance/toynet.sqlite` file into an online SQLite viewer such as https://inloop.github.io/sqlite-viewer/ to run queries on it.

<p align="center"> <kbd> <img src="images/sqlite-viewer-query.png" width="450" /> </kbd> </p>