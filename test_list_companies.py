import pyodbc

server = 'SATURNO13'
database = 'AnalysisDW'
user = 'data_analysis_admin'
password = 'Hg1y3m9VFJsNrzjw8brjbc'
driver = '{ODBC Driver 17 for SQL Server}'
schema = 'TheEliteGroup_Parameters'

def main():
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
        cursor = conn.cursor()
        print(f"Conectado a {server}/{database}, esquema: {schema}, tabla: Companies")
        query = f'SELECT TOP 20 * FROM [{schema}].[Companies]'
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"Total de compañías encontradas: {len(rows)}")
        for row in rows:
            print(row)
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al consultar compañías: {e}")

if __name__ == "__main__":
    main() 