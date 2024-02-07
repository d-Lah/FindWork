#!/bin/bash
~/FindWork/

source .env

export SECRET_KEY=$SECRET_KEY
export CRYPTOGRAPHY_FERNET_KEY=$CRYPTOGRAPHY_FERNET_KEY

pytest find_work/tests/$1
