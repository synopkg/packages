#!/bin/sh

set -e

amass enum --nocolor -d megacorpone.com | LC_ALL=C sort -n > generated_output

diff generated_output debian/tests/static_output
exit $?
