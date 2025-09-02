#!/bin/sh

mkdir -p /config

# Создание redis.conf
cat <<EOF > /config/redis.conf
bind 0.0.0.0
appendonly yes
appendfsync everysec
EOF

# Создание users.acl
cat <<EOF > /config/users.acl
user default off
user ${REDIS_USER} on >${REDIS_PASSWORD} ~* +@all
EOF

exec redis-server /config/redis.conf --aclfile /config/users.acl