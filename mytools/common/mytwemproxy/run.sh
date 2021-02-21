#!/bin/bash

main() {
  /usr/bin/python /generate_configs.py
  /usr/bin/supervisord
}

main