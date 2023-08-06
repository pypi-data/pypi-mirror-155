#!/bin/bash

set -ex

function wait_for() {
    rm -f /tmp/setup-gitea.out
    success=false
    for delay in 1 1 5 5 15 15 15 30 30 30 30 ; do
	if "$@" >> /tmp/setup-gitea.out 2>&1 ; then
	    success=true
	    break
	fi
	cat /tmp/setup-gitea.out
	echo waiting $delay
	sleep $delay
    done
    if test success = false ; then
	cat /tmp/setup-gitea.out
	return 1
    else
	grep 'Access token was successfully created' < /tmp/setup-gitea.out | sed -e 's/.* //' > /srv/gitea/gitea-root-token
	return 0
    fi
}

function setup_gitea() {
    local user="$1"
    local password="$2"
    local email="$3"

    sleep 5 # for some reason trying to run "gitea admin" while gitea is booting will permanently break everything
    if sudo docker exec --user 1000 gitea gitea admin user list --admin | grep "$user" ; then
	sudo docker exec --user 1000 gitea gitea admin user change-password --username "$user" --password "$password"
    else
	wait_for sudo docker exec --user 1000 gitea gitea admin user create --access-token --admin --username "$user" --password "$password" --email "$email"
    fi
}

setup_gitea "$@"
