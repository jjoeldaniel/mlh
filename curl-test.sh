#!/usr/bin/env bash

curl --request POST 127.0.0.1:5000/api/timeline_post -d 'name=Joel&email=joel@mail.com&content=hi!'
curl 127.0.0.1:5000/api/timeline_post
curl --request DELETE 127.0.0.1:5000/api/timeline_post -d 'name=Joel&email=joel@mail.com&content=hi!'
curl 127.0.0.1:5000/api/timeline_post