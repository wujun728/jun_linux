#!/bin/bash
docker build -t supermy/docker-storm_base:0.9.3 mystorm/storm
docker build -t supermy/docker-storm-nimbus:0.9.3 mystorm/storm-nimbus
docker build -t supermy/docker-storm-supervisor:0.9.3 mystorm/storm-supervisor
docker build -t supermy/docker-storm-ui:0.9.3 mystorm/storm-ui
