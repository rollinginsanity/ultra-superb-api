General Notes
=============


### Response Structure

Responses take the below general form:

```
{
  "data": {},
  "error": {}
}
```

The 'data' element will always hold the data returned by a particular endpoint, however, maybe I forgot to set this up for some endpoints, so sue me :p. Let me know if any endpoints aren't structured properly.

The error element should always hold data relating to an error that has occured. The endpoint will also return a HTTP response code that matches the closest to the error.
