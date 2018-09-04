## Installation and proccess:
```
$ git clone https://trinanda3@bitbucket.org/trinanda3/reservasi-homestay-lembah-harau_2.git
$ cd reservasi-homestay-lembah-harau_2
```

**Masuk ke Docker:**
```sh
$ sudo ./scripts/masuk_ke_docker.sh 
```

**Alembic migrations:**
```
$ alembic revision --autogenerate -m 'inisialDb'

Ketika mencoba untuk menjalankan | alembic upgrade | akan error, karena versi alembic belum support dengan geoalcheny, solusinya ada dibawah:
```

**add geoalchemy to versions file and install postgis on docker postgres service:**
```
buka file versions yang ada di folder migrations/versions, kemudian
import baris dibawah ini ke versions file :
--------------------------------------------
from geoalchemy2.types import Geometry
--------------------------------------------
kemudian pada def upgrade(): function ->
 pada | geoalchemy2.types.Geometry | hapus (geoalchemy2.types) tukar itu dengan hanya cukup menggunakan | Geometry |
 atau baris kode nya seperti ini : -> sa.Column('point', Geometry(geometry_type='POINT'), nullable=True),
----------------------------------------------------------------------------------------
masih belum bisa di | alembic upgrade | buka terminal ->

$ docker-compose exec service_postgresql_di_dalam_docker bash
$ apt-get update
$ apt-get install postgresql-9.6-postgis-scripts
$ psql -h localhost -p 5432 -U ta -W          --> password nya kosong atau enter langsung saja
$ CREATE EXTENSION postgis;
----------------------------------------------------------------------------------------
kembali ke docker service -> buka terminal ->
$ sudo docker-compose exec aplikasi_web_di_dalam_docker bash
$ alembic upgrade head
```
