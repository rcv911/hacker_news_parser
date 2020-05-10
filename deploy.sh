#!/usr/bin/env bash
sudo docker-compose -f deploy_postgres.yml up -d
alembic upgrade +1
sudo docker-compose -f deploy_app.yml up -d
