import csv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def parse_fecha(fecha_str):
    """
    Parsea una cadena de fecha en múltiples formatos y la devuelve en formato 'YYYY-MM-DD'.

    Args:
        fecha_str (str): La cadena de fecha a analizar.

    Returns:
        str: La cadena de fecha analizada en formato 'YYYY-MM-DD', o None si falla el análisis.
    """
    formatos = ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']  # Agrega más formatos si es necesario
    for formato in formatos:
        try:
            return datetime.strptime(fecha_str, formato).strftime('%Y-%m-%d')
        except ValueError:
            pass
    return None

class CSVToDBLoader:
    def __init__(self, db_url):
        """
        Inicializa CSVToDBLoader con una URL de base de datos.

        Args:
            db_url (str): La URL para conectarse a la base de datos.
        """
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def load_csv_to_db(self, csv_file_path, table_name):
        """
        Carga datos desde un archivo CSV en una tabla de la base de datos.

        Args:
            csv_file_path (str): La ruta al archivo CSV.
            table_name (str): El nombre de la tabla de la base de datos.
        """
        try:
            # Crea una sesión de SQLAlchemy como manejador de contexto
            with self.Session() as session:
                # Consulta para verificar los registros existentes en la tabla
                query_2 = text(f"SELECT * FROM {table_name};")
                print("Executing query to verify existing records in the table...")
                session.execute(query_2)

                # Before loading the data, print a debug message
                print(f"Loading data from the CSV file into the {table_name} table...")

                # Open the CSV file and load the data into the database
                with open(csv_file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        # Parse the date into the correct format ('YYYY-MM-DD')
                        fecha_firma = parse_fecha(row['fecha_de_firma_del_contrato'])
                        if fecha_firma:
                            row['fecha_de_firma_del_contrato'] = fecha_firma
                        else:
                            print(f"Unable to parse the date in any valid format in the row: {row}")
                            continue
                        
                        # Create an SQL expression as text
                        insert_statement = text(f"INSERT INTO {table_name} ({', '.join(row.keys())}) VALUES ({', '.join([':%s' % k for k in row.keys()])})")

                        # Execute the SQL expression
                        session.execute(insert_statement, row)

                # Commit the changes to the database
                session.commit()

                print(f"Data from the CSV file successfully loaded into the {table_name} table.")
        except SQLAlchemyError as e:
            print(f"Error loading CSV data into the database: {str(e)}")

"""
if __name__ == "__main__":
    # Database connection URL (adjust according to your configuration)
    db_url = "mysql+mysqlconnector://root:admin@localhost/CONTRACTS_DB"

    # Path to the CSV file you want to load
    csv_file_path = r"E:\Python_PCAP\Proyecto_PCAP\chatbot\data\data_et\data_processed.csv"

    # Name of the table in the database
    table_name = "contrato"

    # Print the database connection URL as a debug message
    print(f"Database connection URL: {db_url}")

    # Create an instance of the CSVToDBLoader class
    loader = CSVToDBLoader(db_url)

    # Execute a test query to verify the connection to the table
    with loader.engine.connect() as connection:
        test_query = text(f"SELECT * FROM {table_name} LIMIT 5;")
        result = connection.execute(test_query)

    # Print the results of the test query
    print("Results of the test query:")
    for row in result:
        print(row)

    # Load the CSV file into the database
    loader.load_csv_to_db(csv_file_path, table_name)
"""