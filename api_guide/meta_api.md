Meta API
========

Meta Functions, shortcuts for boostrapping the API, instead of having formal provisioning processes for creating users and so on.

### /admin/register

The admin token is just a simple api-key type construct used for hitting the meta API and authenticating.

Methods (POST)

Authentication - None

#### Request:

```
POST /meta/v1/admin-register HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: 50d536f5-b183-2768-8f86-5a6b43765994

{  
    "name": "test1642"
}
```

#### Required Headers:

`Content-Type: application/json`

#### Request body

* 'name' - Mandatory. The name assigned to the token. Not really used for anything at the moment. Can't be a duplicate, call it whatever you want.

#### Response

```
{
  "data": {
    "key": "9b68765c421d53d3c434892765ffb08e8f6b5b62699e1494275eff82d8bd39a7adccdff577b7684a03e62697d5a75b8059cda1d9c9fe83547b6a638abe7d9067",
    "name": "test1643"
  },
  "error": {}
}
```

#### Response Body

* 'key' - The API key that can be stored and used for other requests in the meta-api.
* 'name' - The name of the Key that has been created, as defined by the user in the request.



### /admin/user/<int:userid>

This api both supports GET and POST, but always just user information for the chosen userID.

Methods (GET, POST)

Authentication - API KEY (But as it turns out, not implemented yet :\)

#### Request:

```
GET /meta/v1/user/1 HTTP/1.1
Host: localhost:5000
Cache-Control: no-cache
```

#### Required Headers:

```
token: api_key
```

#### Request body

N/A

#### Response

```
{
  "data": {
    "user_id": 1,
    "username": "test"
  },
  "error": {}
}
```

#### Response Body

* 'user_id' - The ID of the user.
* 'username' - The username of the user.



### /admin/user/create

Endpoint for creating new users.

Methods (POST)

Authentication - API KEY (But as it turns out, not implemented yet :\)

#### Request:

```
POST /meta/v1/user/create HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: bc816d1d-0452-6541-491e-babf8c2f4992

{
    "username": "username",
    "password": "password"
}
```

#### Required Headers:

```
token: api_key
```


#### Request body

N/A

#### Response

```
{
  "data": {
    "user_id": 3,
    "username": "username"
  },
  "error": {}
}
```

#### Response Body
