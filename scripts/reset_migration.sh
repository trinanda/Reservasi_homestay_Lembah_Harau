#!/usr/bin/env bash
alembic downgrade base
chown -R $USER:$USER migrations/versions/
rm -rf migrations/versions/*
chown -R $USER:$USER web_app/files/
rm -rf web_app/files/* .png .jpg
alembic revision --autogenerate -m 'inisialisasi database'
alembic upgrade head