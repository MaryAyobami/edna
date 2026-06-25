#!/bin/bash

cargo build --release
mkdir output &> /dev/null || true

BUILDDIR=$(git rev-parse --show-toplevel)

# the cryptdb benchmark talks to mysql through the cryptdb proxy
# (applications/proxy), which has to be running first
mysql -utester -ppass --execute='DROP DATABASE IF EXISTS myclass_cryptdb;'
(cd $BUILDDIR/applications/proxy; cargo build --release)
RUST_LOG=error $BUILDDIR/target/release/proxy &> proxy.out &
proxy_pid=$!
trap "kill $proxy_pid &> /dev/null" EXIT

for i in $(seq 30); do
	if ss -ltn 2>/dev/null | grep -q ':62292'; then
		break
	fi
	sleep 1
done

crypto=true
schema="src/schema_nocrypto.sql"

if $crypto; then
	schema="src/schema.sql"
fi

l=20
u=2000
RUST_LOG=error $BUILDDIR/target/release/cryptdb-srv \
    -i myclass_cryptdb --schema $schema --config sample-config.toml \
    --benchmark true --crypto $crypto \
    --nusers $u --nlec $l --nqs 4 &> \
    output/${l}lec_${u}users_$crypto.out
echo "Ran test for $l lecture and $u users"
rm -f *txt

kill $proxy_pid &> /dev/null
