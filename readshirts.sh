#!/bin/bash

REPO="/var/www/demuccracy"
SHIRTS="/var/www/demuccracy/images"

for file in "$SHIRTS"/*; do
    name=${file%.*}
    shirtpath=$(realpath --relative-to="$REPO" "$file")
    echo "INSERT INTO shirts (shirt_id, shirt_name, image) VALUES (NULL, '$name', '$shirtpath');"
done