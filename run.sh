#! /bin/bash

(cd ./stackoverflow/src && gunicorn stack.wsgi --log-file -)
