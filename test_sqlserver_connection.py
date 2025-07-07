import pyodbc

server = 'SATURNO13'
database = 'AnalysisDW'
user = 'data_analysis_admin'
password = 'Hg1y3m9VFJsNrzjw8brjbc'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={user};'
    f'PWD={password};'
    f'Encrypt=no;'
    f'TrustServerCertificate=Yes;'
)

try:
    conn = pyodbc.connect(connection_string)
    print(f"Conexión exitosa a {server} (base: {database}) con el usuario {user}")
    conn.close()
except Exception as e:
    print(f"Error al conectar a {server}: {e}") 