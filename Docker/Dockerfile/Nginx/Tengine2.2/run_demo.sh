#!/usr/bin/env bash
sudo docker run --rm -i -t -p 80:80 -v /Users/yunai/Documents/html:/usr/share/nginx/html yunai/tengine:2.2.0-alpine