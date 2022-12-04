import psycopg2

conn = psycopg2.connect(
    database="NftData",
    user="postgres",
    password="Nabster96",
    host="127.0.0.1",
    port="5432"
)
print("db successfully")