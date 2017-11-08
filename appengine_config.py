import os

from google.appengine.ext import vendor


DEV_ENV = os.environ.get("SERVER_SOFTWARE", "Development").startswith("Development")

DEBUG_MODE_ENABLED = DEV_ENV

APP_CONFIG = {

    "PROVIDERS": {

        "VDISK": {
            "AUTHORIZE_URL": "https://auth.sina.com.cn/oauth2/authorize",
            "ACCESS_TOKEN_URL": "https://auth.sina.com.cn/oauth2/access_token",
            "APP_KEY": "****************",
            "APP_SECRET": "*************************8"
        }

    },

    "EMAIL": {
        "SENDER": "beambook.kindle@gmail.com",
        "BCC": "dcenrie@gmail.com"
    },

    "PAGE_SIZE": "30",

    "FETCH_AND_EMAIL_QUEUE": {
        "NAME": "fetch-and-email-queue",
        "URL": "/tasks/sender"
    }

}

if not DEV_ENV:
    APP_CONFIG["PROVIDERS"]["VDISK"]["APP_KEY"] = "******************"
    APP_CONFIG["PROVIDERS"]["VDISK"]["APP_SECRET"] = "********************************"

# Add any libraries install in the "lib" folder.
vendor.add("lib")
