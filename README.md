# Homestay Reservation Harau Valley

### feature on this app
- Geo-Alchemy using MapBox 
    - this feature is for admin to set the homestay location
- Google Maps views 
    - is for views the homestay location as a user
- Notifications feature using Twilio SMS Gateway and GMAIL API
    - this feature is for user and admin :
        - admin notifications if someone orders room
        - user notifications to get orders informations
- Download invoice as .pdf
- and other feature that you can explore when running this app

### Instalation process
```bash
$ git clone https://github.com/trinanda/Reservasi_homestay_Lembah_Harau.git
$ cd Reservasi_homestay_Lembah_Harau
```
- set your credential at **web_app/settings.py**
    - > for more informations how to do that you can go to that file
    
- make sure you already set the important things on the above

- run the Docker
```bash
$ sudo docker-compose up --build 
```
- on the other terminal session, enter to Docker container
```bash
$ sudo ./scripts/masuk_ke_docker.sh
```
- and run the alembic migrations to make all table that you have declare on your models
```bash
$ alembic revision --autogenerate -m 'initial_db'
$ alembic upgrade head
```
- you will get some error if you run the upgrade command above, because until now the alembic version and geoalchemy2 version that doesn't matching.
- And so.. the solution is :
    - go to migrations/versions/ and open the versions file that you recently create
        - import Geometry on the above of upgrade function
            ```
            from geoalchemy2.types import Geometry
            ```
        - then on geoalchemy2.types.Geometry change to just use Geometry, or the script is like this:
            ```
            sa.Column('point', Geometry(geometry_type='POINT'), nullable=True),
            ```
    - go to postgreSQL service on the docker container by running this command :
    ```bash
      $ sudo ./scripts/masuk_ke_service_postgres_didalam_docker.sh 
    ```
    - then run the update command inside the service
    ```bash
      $ apt-get update
      $ apt-get install postgresql-9.6-postgis-scripts
      $ psql -h localhost -p 5432 -U ta -W 
          # the password just blank, so you can just hit the enter button
      $ CREATE EXTENSION postgis;
    ```

