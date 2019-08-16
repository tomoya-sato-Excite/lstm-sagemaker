#!/bin/bash

title=$1
content=${2:-application/x-www-form-urlencoded}

curl http://localhost:8080/invocations -H "Content-Type: ${content}" -d "title=${title}"