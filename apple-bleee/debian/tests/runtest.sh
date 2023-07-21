#!/bin/sh

set -e

export HOME=$AUTOPKGTEST_TMP

echo "Testing adv_airpods"
python3 adv_airpods.py -h

echo "Testing adv_wifi"
python3 adv_wifi.py -h

echo "Testing airdrop_leak"
python3 airdrop_leak.py -h

echo "Testing ble_read_state"
python3 ble_read_state.py -h

echo "Testing hash2phone/hashmap_gen_sqlite"
python3 hash2phone/hashmap_gen_sqlite.py

echo "Testing fill sqlite DB with hash2phone/hashmap_gen_sqlite"
python3 hash2phone/hashmap_gen_sqlite.py dbinit
python3 hash2phone/hashmap_gen_sqlite.py 1213XXXXXX

echo "Testing hashmap_gen"
python3 hash2phone/hashmap_gen.py
