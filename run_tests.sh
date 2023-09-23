#!/bin/bash
~/FindWork/

source .env

export SECRET_KEY=$SECRET_KEY

pytest find_work/tests_api
