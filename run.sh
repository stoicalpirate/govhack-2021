#!/bin/sh

# Read all env variables and export using jq
ALLVARS=$(jq .Values api/local.settings.json)
for s in $(echo $ALLVARS | jq -r "to_entries|map(\"\(.key)=\(.value|tostring)\")|.[]" ); do
    export $s
done

# Build and run the app
yarn run build && swa start dist --api api
