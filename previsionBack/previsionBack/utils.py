from django.db import connection

def dispatchall(cursor):
    columns = [col[0] for col in cursor.description]
    return[
        dict(zip(columns,row)) for row in cursor.fetchall()
    ]
    
def requete(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        
def insertion(table, values):
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table} VALUES ({placeholders})"
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query, values)