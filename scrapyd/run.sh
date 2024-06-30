#!/bin/bash

mkdir -p /var/lib/scrapyd/logs
logparser -dir /var/lib/scrapyd/logs &
scrapyd &
wait -n
exit $?
