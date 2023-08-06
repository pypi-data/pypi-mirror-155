[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  ![GitHub last commit](https://img.shields.io/github/last-commit/jthop/flask-xtra-info?style=flat-square)

<!-- [![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)  -->


# Flask-Xtra-Info #


Simple Flask Extension to manage several tasks I was repeadidly doing in every project.


- **Request ID generation** - Track your requests across multiple APIs
- **Request ID parsing** - Use request ids from other services *[coming soon - not complete]*
- **Response timing** - Log the total time in ms spent processing the request
- **Instance ID generation** - Identify different flask instances
- **Automatic logging** - Automatically generate access-log style log entries
- **Log filter** - Use our log filter to insert the ids into your logs


## Use ##


After installing the extension you can get started right away

    from flask import Flask
    from flask_xtra_info import XtraInfoExtension
    
    app = Flask(__name__)
    
    # setting the config to false in the line below is simply an example
    app.config['XTRA_INFO_GEN_INSTANCE_ID'] = False
    
    # finally, instantiate the extension
    xtra = XtraInfoExtension(app)
    

We also suppoort the *app factory* pattern

    from flask import Flask
    from flask_xtra_info import XtraInfoExtension
    
    xtra = XtraInfoExtension()

    create_app():
        app = Flask(__name__)
        xtra.init_app(app)

Once the extension has been instantiated you can find the data in your response headers as well as access it in your logs.

## Configuration ##


The extension is configured via Flask's built-in config object, app.config.  If unfamiliar with Flask's app.config, you can read more at: 
<https://flask.palletsprojects.com/>

| Variable | Default | Type | Description |
| --- | --- | --- | --- |
| XTRA_GEN_REQUEST_ID | `True` | Boolean | Should the extension generate request ids |
| XTRA_GEN_INSTANCE_ID | `True` | Boolean | Should the extension generate an instance id |
| XTRA_TIME_RESPONSE | `True` | Boolean | Should the extension time the response |
| XTRA_CREATE_ACCESSLOG | `True` | Boolean | Should the extension automatically generate access-log style logs |
| XTRA_INSERT_VERSION | `True` | Boolean | Should the extension insert the app version in the header |
| XTRA_ACCESSLOG_FMT |  | [^1] | Header | In addition you can include request_id, instance_id and response_time. |
| XTRA_REQUEST_ID_HEADER | `X-Request-Id` | String | Header to use for request-id |
| XTRA_INSTANCE_ID_HEADER | `X-Instance-Id` | String | Header to use for instance-id |
| XTRA_RESPONSE_TIME_HEADER | `X-Response-Time` | String | Header to use for the response time |
| XTRA_VERSION_HEADER | `X-App-Version` | String | Header to use for the app version |


## Log Filter ##

Finally, an example of using the log filter with dictConfig
    
    import logging
    from logging.config import dictConfig
    from xtra_info import XtraInfoLogFilter
    
    
    LOG_CFG = {
        "version": 1,
        "formatters": {
            "xtra_info_format": {
                "format": "%(message)s requestId=%(request_id)s via: %(instance_id)s took %(response_time)s ms"
            }
        },
        "filters": {
            'xtra_info_filter': {
                '()': XtraInfoLogFilter
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "xtra_info_format",
                "level": "DEBUG",
                "filters: ["xtra_info_filter"]
            }
        }
    }
    
    dictConfig(LOG_CFG)
    
The 3 variables available to you in your log formatting will be:
- request_id
- instance_id
- response_time


[^1]: '{now} - {ip} - - "{method} {path}" {status_code}'
