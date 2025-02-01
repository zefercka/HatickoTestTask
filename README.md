docker-compose up -d --build
docker exec -it db_server pg_restore -U postgres -d hatiko /backup/hatiko_server_backup.backup
docker exec -it db_bot pg_restore -U postgres -d hatikoBot /backup/hatiko_bot_backup.backup
docker start server
docker start bot