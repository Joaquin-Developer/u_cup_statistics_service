#!/bin/bash
source /home/jparilla/envs/env/bin/activate
uvicorn app.main:app --port 8001 --reload
