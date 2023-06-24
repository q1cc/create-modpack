#!/bin/bash

# Grep through modrinth.index.json and output a list of packwiz commands

# Example URL to match: https://cdn.modrinth.com/data/8shC1gFX/versions/RbNy07Bx/BetterF3-4.0.0-Fabric-1.19.2.jar
grep -oP 'https://cdn.modrinth.com/data/[^/]+/versions/[^/]+/[^/]+.jar' modrinth.index.json \
    | sed 's/https:\/\/cdn.modrinth.com\/data\/\([^/]\+\)\/versions\/[^/]\+\/\([^/]\+\).jar/packwiz modrinth install \1 # \2/'
