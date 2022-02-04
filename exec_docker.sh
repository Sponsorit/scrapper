#!/bin/bash

# this stores the container id
CONTAINER_ID=$(docker run -it scrapper:0.0.2)

docker cp $CONTAINER_ID:usr/src/app/twitch_users_networks.csv ./output/tn.csv