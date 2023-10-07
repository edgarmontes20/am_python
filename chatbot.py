import nltk
from modules.nl_processing import Nlp
import os
from modules.directory_operations import Directory
from modules.file_operations import File
from charts.chart_generation import DataProcessor
from data.manage_db import Upload_csv_to_db
from datetime import datetime

def run_chatbot(chat):
    """
        Manejador de ejecución de chatbot haciendo uso de modelos implementados
        
        Args: 
            chat (str): Objeto instanciado de la clase Nlp   
            
        Returns:
            None
    """
               
    try:
        flag = True
        chat.talk_to_client(f"My name is {chat.BOT_NAME}. I will answer your queries about file and directory manipulation .")
        while flag:
            chat.talk_to_client("Please type a request about files and directories. If you want to exit, type Bye!")
            user_response = input()
            if "bye" in user_response.lower():
                flag = False
                chat.talk_to_client("Bye! take care..")
            elif "thank" in user_response.lower():
                flag = False
                chat.talk_to_client("You are welcome..")
            elif chat.greeting(user_response) is not None:
                chat.talk_to_client(chat.greeting(user_response))
            else:
                tokens = nltk.word_tokenize(user_response)
                chat.talk_to_client(chat.response(user_response))
                # 1. Crear directorio
                if 'create directory' in user_response:
                    if 'directory' in tokens and tokens.index('directory') + 1 < len(tokens):
                        name = tokens[tokens.index('directory') + 1]
                        directory_path = os.path.join(dir_path, name)
                        directorio = Directory(directory_path)
                        directorio.create_dir(directory_path)
                    else:
                        chat.talk_to_client("Invalid input. Please specify a directory name.")
                # 2. Crear archivo
                elif 'create file' in user_response:
                    if 'file' in tokens and tokens.index('file') + 1 < len(tokens):
                        name = tokens[tokens.index('file') + 1]
                        file_path = os.path.join(dir_path, name)
                        archivo = File(file_path)
                        archivo.create_file(file_path)
                    else:
                        chat.talk_to_client("Invalid input. Please specify a directory name.")
                # 3. Mostrar lista de archivos y subdirectorios
                elif 'list files' in user_response:
                    #print(chat.directory.list_files())
                    path_dir = os.path.join(dir_path, name)
                    directorio = Directory(path_dir)
                    directorio.show_list_dir(path_dir)
                # 4. Renombrar directorio
                elif 'rename directory' in user_response:
                    old_name = tokens[tokens.index('directory') + 1]
                    new_name = tokens[tokens.index('to') + 1]  
                    path = os.path.join(dir_path, old_name)            
                    nombre_directorio = Directory(path) # instancia un objeto de la clase directory
                    nombre_directorio.rename_dir(path, new_name) # le envia el nuevo nombre como parametro
                # 5. Renombrar archivo
                elif 'rename file' in user_response:
                    old_name = tokens[tokens.index('file') + 1]
                    new_name = tokens[tokens.index('to') + 1]
                    path = os.path.join(dir_path, old_name)
                    #path = input("Please enter the absolute path of the file, including the actual file name you want to rename: ")
                    #new_name = input("Please enter the new file name: ")
                    nombre_archivo = File(path)  # instancia un objeto de la clase File
                    nombre_archivo.rename_file(path, new_name) # le envia el nuevo nombre como parametro
                # 6. Mover archivo
                elif 'move file' in user_response:
                    ##tokens = user_response.split()
                    # Encontrar los índices de las palabras clave "file" y "to"
                    ##move_index = tokens.index("file")
                    ##to_index = tokens.index("to")
                    source_path = input("Please enter the actual absolute path of the file you want to move: ")
                    destination_path = input("Please enter the destination absolute path of the file: ")
                    mover_archivo = File(source_path) # instancia la clase File con la ruta origen
                    mover_archivo.move_file(source_path, destination_path) # llama al metodo move con la ruta origen y ruta destino
                # 7. Eliminar archivo
                elif 'delete file' in user_response:
                    name = tokens[tokens.index('file') + 1]                   
                    file_path = os.path.join(dir_path, name)
                    archivo = File(file_path) # instancia la clase File con la ruta absoluta del archivo a eliminar
                    archivo.delete_file(file_path) # invoca el metodo delete con la ruta absoluta del archivo a eliminar
                # 8. Cambiar permisos de archivo recibe formato octal Ej 744
                elif 'change permissions' in user_response:
                    ##tokens = user_response.split()
                    # Encontrar los índices de las palabras clave "permissions" y "to"
                    ##name = tokens.index("permissions")
                    ##to_index = tokens.index("to")
                    ##file_path = " ".join(tokens[name + 1:to_index])
                    ##name = tokens[tokens.index('permissions') + 1]
                    ##permissions = int(" ".join(tokens[to_index + 1:]), 8)
                    file_path = input("Please enter the absolute path of the file, including the file name you want to modify permissions: ")
                    permissions = input("Please enter the new permissions in octal format Ex: 745 : ")
                    archivo = File(file_path)
                    archivo.change_permissions_file(file_path, permissions)
                # 9. Buscar archivo en directorio y subdirectorios
                elif 'search' in user_response or 'find' in user_response or 'lookup' in user_response:
                    search_keywords = ['search', 'find', 'lookup']
                    name = tokens[tokens.index('search') + 1]
                    file_to_find = tokens[tokens.index(next((word for word in tokens if word in search_keywords), None)) + 1] if any(word in tokens for word in search_keywords) else None
                    base_directory = dir_path
                    archivo = File(base_directory)
                    archivo.searcher_file(base_directory, file_to_find)
                # 10. Sube data_processed.csv a una BD
                elif 'insert data to base' in user_response:

                    input_file_path = input("Please enter the absolute path of the CSV file name to upload: ")
                    upload_file = Upload_csv_to_db(input_file_path)
                    grafica.upload_info(upload_file)

                # 11. Buscar el NIT en dentro de data_processed.csv y grafica el valor de contratos por año-mes
                elif 'graphic' in user_response:
                    #input_file_path = input("Please enter the absolute path of the CSV file that you want to use for generating graphics:  ")
                    input_file_path = r'E:\Python_PCAP\Proyecto_PCAP\chatbot\data\data_et\data_processed.csv'
                    grafica = DataProcessor(input_file_path) # instancia la clase DataProcessor con la ruta ABS del insumo de datos
                    group_filter = input("Please enter the ID (NIT) to filter: ") # solicita NIT para filtro de datos

                    try:
                        # solicita año para filtrar datos del NIT
                        selected_year = int(input("Please enter the year you want to choose to generate graphics: "))
                    except ValueError:
                        # sino se digita año asigna none y grafica todos los años hallados para el NIT 
                        # Obtener la fecha y hora actual
                        actual_date = datetime.now()
                        # Obtener el año actual
                        selected_year = actual_date.year
                    grafica.process_data(group_filter)  # Pasa NIT al método process_data -> procesa lotes
                    grafica.generate_plot_info(group_filter, selected_year)  # Pasa NIT y AÑO al método generate_plot -> grafica datos y guarda
                elif "bye" in user_response.lower():
                    chat.talk_to_client("Bye! take care..")
                    break

    except LookupError as err:
        print ('Tenemos un error',err)  

if __name__ == '__main__':
    
    dir_path = r'E:\Python_PCAP\Proyecto_PCAP\chatbot\Work_folder'
    #print(dir_path)

    #obtener la ruta absoluta del directorio.
    absolute_path = os.path.abspath(dir_path)
    #print(absolute_path)
    
    #Instanciando objeto de tipo Directory
    directory = Directory(absolute_path)
    
    #Ruta con corpus usado para entrenar el modelo
    path_corpus = r"E:\Python_PCAP\Proyecto_PCAP\chatbot\modules\files_directories.txt"

    
    #Instanciando objeto de tipo Nlp
    chatbot = Nlp(directory, path_corpus)
    print('Intanciado objeto')
    chatbot.initialize_nlp()
    print('Inicializado modulo nlp')
    run_chatbot(chatbot)
    print('Chat finalizado')
