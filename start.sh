#!/bin/bash
app="decryption_test"
docker build -t ${app} .
docker run -d -p 80:80 \
  --name=${app} \
  -v $PWD:/app ${app}
