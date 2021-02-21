sh datadir.sh
fig stop && fig rm --force && fig up -d &&fig ps
sh initdb.sh