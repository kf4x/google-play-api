# Google Play Store API

A python wrapper for accessing the google play store.


## Useage

```bash
git clone https://github.com/javierchavez/google-play-api.git 
```

###### Cookie

Go to the [play store](http://play.google.com) click on a app and click on install **do not** install it. We just want to make sure the cookie is set.

Locate the cookies. There are plenty of tools out there to help you do so.

**You are looking for**

```
"SSID"
"SID"
"SAPISID"
"PREF"
"PLAY_PREFS"
"PLAY_ACTIVE_ACCOUNT"
"OGPC"
"NID"
"HSID"
"APISID"
"_gat"
"_ga"
```

Now open up the example `main.py` and paste in the corresponing values.

###### token

In your browser locate the event with the name 

	getdevicepermissions?authuser=0

Click it, then click the headers tab (in chrome). Scroll down to form data and copy the **token** value. Paste in corrosponding area in `main.py`

 