import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
import os

class DataProcessor:
    def __init__(self, input_file):
        """
        Inicializa una instancia de la clase DataProcessor.

        Args:
            input_file (str): Ruta del archivo CSV de entrada.

        Nota: default_factory es una función o un tipo de dato que se utiliza para crear el valor predeterminado cuando 
        se accede a una clave que no existe en el diccionario. Es útil cuando se acumulan valores por claves en un diccionario 
        y no se sabe de antemano cuáles serán todas las claves posibles

        """
        self.input_file = input_file
        self.sums_by_group = defaultdict(float)  # Diccionario para almacenar las sumas por grupo

    def process_data(self, group_filter):
        """
        Procesa los datos del archivo CSV por lotes y calcula las sumas por grupo.
        """
        chunk_size = 1000  # Tamaño de cada fragmento
        chunk = []

        with open(self.input_file, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Leer la cabecera (encabezados) si es necesario

            for row in reader:
                chunk.append(row) # va creando la lista de 1000 filas
                if len(chunk) >= chunk_size:
                    # completa 1000 y llama al metodo procesar, pasa group_filter - NIT como argumento
                    self.process_chunk(chunk, group_filter)  
                    chunk = []  # vacia la lista para el siguiente lote

            if chunk:
                self.process_chunk(chunk, group_filter)  # hace el ultimo lote y Pasa group_filter como argumento

    def process_chunk(self, chunk, group_filter):
        """
        Procesa un fragmento de filas y actualiza las sumas por grupo.

        Args:
            chunk (list): Fragmento de filas del archivo CSV.
            group_filter (str): El grupo a filtrar (o None para mostrar todos).
        """
        found = False  # Variable para rastrear si se encontró el group_filter en el chunk
        for row in chunk:
            # Ajusta el formato según los datos de la columna [23] fecha_firma_yyyymm como los key de agrupación 
            grupo = datetime.strptime(row[23], '%Y-%m')  
            valor1 = float(row[16])  # Obtiene los value -> La columna [16] valor_contrato

            if row[2] == group_filter:  # aplica el filtro de NIT a cada lote procesado del archivo
                if grupo in self.sums_by_group:
                    self.sums_by_group[grupo] += valor1 # si el key existe acumula valor_contrato
                else:
                    self.sums_by_group[grupo] = valor1 # si el key NO existe lo crea y asigna el valor_contrato
                found = True

        if not found:
            print(f"The ID {group_filter} was not found in the data")

        self.sums_by_group = dict(sorted(self.sums_by_group.items()))       
            
    def generate_plot_info(self, group_filter, selected_year):
        """
        Formate la informacion para el gráfico de barras a partir de los datos procesados, con la opción de filtrar por grupo y año.

        Args:
            group_filter (str): El grupo a filtrar.
            selected_year (int): El año seleccionado para el gráfico.
        """
        # Crea las listas para el grafico a partir de key(año-mes) eje x | value (valor contrato) eje y
        x = []
        y = []

        # Recorre el diccionario y llena las listas X - Y
        
        for grupo, suma in self.sums_by_group.items():
            fecha_formateada = datetime.strftime(grupo, "%Y-%m") # formatea la fecha del key como 2023-07
            x.append(fecha_formateada)
            y.append(suma)

        if selected_year is not None:  # Valida si se envio un año para seleccionar de los datos a graficar.
            # aplica un filtro con compresion de listas por el año ingresado por consola
            year_filter = [date for date in x if datetime.strptime(date, "%Y-%m").year == selected_year]
            # reasigna a la lista x la lista filtrada
                   
        x = year_filter
        # busca para elemento de la lista de keys años filtrados el value q le corresponde y lo asigna al eje Y
        y = [self.sums_by_group[datetime.strptime(date, "%Y-%m")] for date in year_filter] 

        # Verificar si el valor de selected year es válido
        year_exists = any(str(selected_year) in date for date in x)
        if year_exists is False:
            print(f"The year {selected_year} was not found in the data") 
        else:
            self.ploting(x,y,group_filter,selected_year)
        
    def ploting(self, axis_x, axis_y, group_filter, selected_year):

        plt.figure(figsize=(10, 8))  # Ajusta el tamaño de la ventana del gráfico 
        plt.bar(axis_x, axis_y, width=0.5) # asigna los datos de ejes para la grafica y ancho de barras
        plt.xlabel('Contracts Sign Dates')
        plt.ylabel('Contract Amounts')
        plt.title(f'Value contract signed per year-month for ID (NIT) {group_filter} ({selected_year})')
        plt.xticks(rotation = 90)
        self.save_figure(group_filter,selected_year) # llama al metodo q guardara la grafica generada
        plt.show() # muestra la grafica al usuario

    def save_figure(self, group_filter, selected_year):
        """
        Guarda el gráfico de barras en la misma ruta del insumo inicial

        Args:
            group_filter (str): El grupo a filtrar (o None para mostrar todos).
            selected_year (int): El año seleccionado para el gráfico.
        """
        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now()
        # Formatear la fecha y hora en el formato deseado (yyyymmdd_hh_mm_ss)
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y%m%d%H%M%S")
        # establece nombre de archivo *.jpg para el nit y año consultado
        figure_file_name = 'Contracts_chart_' + str(selected_year) + '_Nit_'+ group_filter + '_' + fecha_hora_formateada + '.jpg'
        # guarda grafica en el mismo directorio donde esta el archivo insumo de datos
        plt.savefig(os.path.join(os.path.dirname(self.input_file),figure_file_name))

