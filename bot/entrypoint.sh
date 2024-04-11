#!/bin/bash

gunicorn -w 4 -b 0.0.0.0:8000 webhook:app --worker-class aiohttp.GunicornWebWorker
#python3 main.py
