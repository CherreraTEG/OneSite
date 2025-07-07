import os
import pyodbc


# Parámetros de conexión
server = 'SATURNO13'
database = 'AnalysisDW'
username = 'data_analysis_admin'
password = 'Hg1y3m9VFJsNrzjw8brjbc'

# Crear la cadena de conexión
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

try:
    # Conectar
    conn = pyodbc.connect(connection_string)
    print("Conexión exitosa.")

    # Crear cursor
    cursor = conn.cursor()

    # Ejemplo de query
    query = "SELECT TOP 10 * FROM TheEliteGroup_Parameters.Companies"
    cursor.execute(query)

    # Traer resultados
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    print("Error al conectar o consultar:", e)

finally:
    # Cerrar conexión
    if 'conn' in locals():
        conn.close()
