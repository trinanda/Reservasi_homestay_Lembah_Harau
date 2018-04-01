@flask_objek.route('/tesdb')
def tesdb():
    import psycopg2

    conn = psycopg2.connect("dbname=ta user=ta password=12345 host=service_postgresql_di_dalam_docker")

    cur = conn.cursor()

    cur.execute("SELECT * FROM kamar;")

    id_kamar = cur.fetchone()
    conn.close()
    return "output table kamar: {}".format(id_kamar)

a = tesdb()

print(a)