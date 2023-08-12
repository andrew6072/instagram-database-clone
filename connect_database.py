import psycopg2 as ps

# establishing the connection
conn = ps.connect(database="instagram1",
                  user='postgres',
                  password='Icandoit2706',
                  host='127.0.0.1', port='5432')

conn.autocommit = False

cursor = conn.cursor()


conn.commit()
print("Records inserted........")
cursor.close()
conn.close()

