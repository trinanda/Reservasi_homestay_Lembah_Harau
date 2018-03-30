#!/usr/bin/env bash
chown -R $USER:$USER migrations/versions/*
rm -rf migrations/versions/*
chown -R $USER:$USER web_app/
rm -rf web_app/files/*
alembic downgrade base
alembic revision --autogenerate -m 'inisialisasi database'
alembic upgrade head