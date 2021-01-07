#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging


__author__ = "Scott Bowe"
__license__ = "Apache v2"
__version__ = "1.0"


MANAGEENGINEURL = ' https://sdp.company.com/api/v3/requests'

##The route with ALERTID is for calls from vROPS, without is LI
@app.route("/endpoint/manageengine/<TOKEN>", methods=['POST'])
@app.route("/endpoint/manageengine/<TOKEN>/<ALERTID>", methods=['POST','PUT'])
def manageengine(TOKEN=None, ALERTID=None):
    """
    Create a new incident for the bigpanda service identified by `APIKEY` in the URL.
    Uses https://www.manageengine.com/products/service-desk/sdpod-v3-api/SDPOD-V3-API.html.
    """
    if not MANAGEENGINEURL:
        return ("MANAGEENGINEURL parameter must be set properly, please edit the shim!", 500, None)
    if not TOKEN:
        return ("TOKEN must be set in the URL (e.g. /endpoint/manageengine/<TOKEN>/<APPKEY>", 500, None)
    HEADERS = {"Accept": "application/json", "Content-Type": "application/json", "TECHNICIAN_KEY": TOKEN}

    # Retrieve fields in notification
    a = parse(request)

    payload = {
        input_data = "request": {
        "subject": a['description'],
        "description": a['moreinfo'],
        "requester": {
            "name": "TICKET OPENER"
        },
        "group": {
            "name": "ASSIGNMENT GROUP"
        },
        "technician": {
            "name": "TECHNICIAN ASSIGNMENT"
        }
    }
    }
    return callapi(MANAGEENGINEURL, 'post', json.dumps(payload), HEADERS)
