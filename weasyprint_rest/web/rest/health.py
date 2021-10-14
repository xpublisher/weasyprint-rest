#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from flask import request
from flask_restful import Resource


class HealthAPI(Resource):

    def __init__(self):
        super(HealthAPI, self).__init__()

    def get(self):
        pong = request.args.get('ping', '')

        return {
                   "status": "OK",
                   "timestamp": round(time.time() * 1000),
                   **({"pong": pong} if pong else {})
               }, 200
