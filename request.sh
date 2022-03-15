#!/usr/bin/env bash

curl -F 'html=@xml/example.html' -X POST -F 'mode=pdf' http://localhost:5000/api/v1.0/print --output hallo.pdf