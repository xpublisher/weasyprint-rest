#!/usr/bin/env bash

curl -F 'html=@html_files/example.html' -X POST -F 'mode=pdf' http://localhost:5000/api/v1.0/print --output output.pdf



# | When doing the following, change "loops" in "print.py" Line 98 to 1.  |
# v => so you can simultate many request on the API                       v

# for i in {1..1000}
# do
#     curl -F 'html=@html_files/example.html' -X POST -F 'mode=pdf' http://localhost:5000/api/v1.0/print --output output.pdf
#     echo "==> $i"
# done