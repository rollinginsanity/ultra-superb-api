What the hell is this thing?
============================

The aim is for this to eventually be a deliberately vulnerable API, implementing some of your favorite OWASP Top 10.

Currently things that are implemented are:

* A basic management API for creating users and API keys (Meta API). All security issues with this API are unintentional, and my own fault.
* An Auth API, currently I've implemented a sketchy version of oAuth. Have a look through the code and laugh.
* The CrappyBank API, currently I've only implemented auth checking, the default index API and an auth-check to validate that oAuth works.

I decided to build this, as I'm looking at building some tooling around continuous checking of APIs for security issues, both technical and business logic. I needed a really bad API to test with, so I decided to build one.


Requirements
============

* Python 3.5+
* Virtualenv
* Pip

To run
======

Set up a virtual environment inside the folder created by a `git clone`. The rest of the steps assume you're either using a Virtual Environment or somehow magically kept your System Packages intact while installing the dependencies for this project.

Run `python create_db.py` if you haven't already (builds the DB). If I make changes to the DB, run `python db_migrate` and `python db_upgrade` to upgrade. If you move back to an earlier commit, use `db_downgrade.py` to roll back to the version that matches the commit you are using.

Run `python start.py` to kick things off.

In the `/postman` is a postman collection with the bits of the API I've build implemented. This will always be up-to-date with what works, as it's how I check stuff is implemented. Specifically run the create user and the api key requests to get started. Also you'll need to create an environment in Postman.

OWASP Top 10 Implementation Status
==================================

I can't promise I'll get everything from this list working. Things like SQL injection might not be easily possible as I'm using an ORM, but leave it with me and let's see how creatively bad I can be.

| OWAP Top 10 Item (2013) | Status |
| --- | --- |
| A1 - Injection | There's some examples of this, specifically command injection, no SQL injection yet. |
| A2 - Broken Authentication and Session Management | Partial, poor randomness in tokens, broken sessions in the works. |
| A3 - Cross Site Scripting | Literally everywhere. |
| A4 - Insecure Direct Object Reference | Partial, can directly reference other user objects. |
| A5 - Security Misconfiguration | Not sure if I'll worry about this one. |
| A6 - Sensitive Data Exposure | Literaly everywhere, from logs to being able to access the data of other users. |
| A7 - Missing Function Level Access Control | As this is an API I'm implicitly forcing authentication for all users, but I might cook up something with this one. |
| A8 - Cross Site Request Forgery | Shoulda already be possible, just need to come up with an example. |
| A9 - Using Components With Known Vulnerabilities | Same as A5, I might not worry about this one explicitly. |
| A10 - Unvalidated Redirects and Forwards | As this is an API I might have to make a heavy handed example... |
