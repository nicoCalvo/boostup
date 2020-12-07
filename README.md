# BoostUp HubSpot API OAUTH2

## How To

start the server using
```
make testserver
```
or
```
make prodserver
```

Open the Browser in the url:

```
https://localhost:9999
```

_NOTE_: https is required due to a restriction on the HubSpot Oauth2 implementation that does not allow http
redirections


The app will redirect you to Hubspot login prompt. The account associated for the demo (which is linked to the
app_key and app_secret) is:

```
boostuphubspot@gmail.com

```
_password not provided in this doc_


Once the login process is completed, choose the account

```
App Test Account 1
```

This account is allowed to pull contacts scope related data, other account will fail to connect the service with Hubspot's API.