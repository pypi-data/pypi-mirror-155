#!/bin/bash

set -ex

function setup_woodpecker() {
    local gitea_host="$1"
    local woodpecker_host="$2"

    if test -f /srv/woodpecker/secrets/gitea-client-id ; then
	echo Gitea OAuth credentials already exist
    else
	local token=$(cat /srv/gitea/gitea-root-token)
	mkdir -p /srv/woodpecker/secrets
	curl -XPOST -H "Content-Type: application/json" -H "Authorization: token ${token}" -d '{"name":"woodpecker","redirect_uris":["https://'$woodpecker_host'/authorize"]}' http://$gitea_host:8080/api/v1/user/applications/oauth2 > /tmp/oauth.json
	jq --raw-output .client_id < /tmp/oauth.json > /srv/woodpecker/secrets/gitea-client-id
	jq --raw-output .client_secret < /tmp/oauth.json > /srv/woodpecker/secrets/gitea-client-secret
    fi
}

setup_woodpecker "$@"
