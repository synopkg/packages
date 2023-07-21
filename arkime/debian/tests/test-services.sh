#!/bin/sh

set -e

arkime-wise-start
if ! systemctl is-active -q arkimewise; then
    echo "FAILURE: arkimewise service is not active"
    exit 1
fi

arkime-wise-stop

arkime-parliament-start
if ! systemctl is-active -q arkimeparliament; then
    echo "FAILURE: arkimeparliament service is not active"
    exit 1
fi
arkime-parliament-stop
