import os

class Directory():
    """Clase para el manejo de directorios."""
    def __init__(self, dir_name):
        """Inicializa una instancia de la clase Directory con la ruta y nombre especificados."""
        self.dir_name = dir_name  # Ruta del directorio / en la herencia se referirá a la ruta del archivo


    def create_dir(self, directory_path):
        """Crea un nuevo directorio en la ubicación especificada si no existe."""
        if not os.path.exists(directory_path):
            try:
                os.mkdir(directory_path)  # Crea un directorio en la ruta completa
                print(f"Directory '{directory_path}' created successfully.")
            except OSError as e:
                print(f"Error creating the directory: {e}")
        else:
            print(f"The directory '{directory_path}' already exists.")

    def show_list_dir(self, directory_path):
        """Muestra una lista de archivos y subdirectorios en el directorio actual."""
        try:
            content_list = os.listdir(directory_path)  # Lista de contenido en la ruta completa
            print(f'\nThe elements in the path {directory_path} are : \n')
            for element in content_list:
                print(element)
            print(f'\n')
        except FileNotFoundError:
            print(f"Error: The directory '{directory_path}' was not found.")
        except PermissionError:
            print(f"Error: You do not have permission to access the directory '{directory_path}'.")
        except OSError as e:
            print(f"Error listing the directory '{directory_path}': {e}")
        except Exception as e:
            print(f"Unknow error listing files: {e}")

    def rename_dir(self, path , new_name):
        """Cambia el nombre del directorio."""
        try:
            os.rename(path, os.path.join(os.path.dirname(path), new_name))  # Cambia el nombre en la ruta completa
            self.dir_name = os.path.join(os.path.dirname(path), new_name)  # Actualiza el nombre del objeto Directory
            print(f"The directory has been renamed correctly to '{new_name}'.")
        except FileNotFoundError:
            print(f"Error: The directory '{self.dir_name}' was not found.")
        except PermissionError:
            print(f"Error: You do not have permissions to change the directory name.")
        except OSError as e:
            print(f"Error renaming the directory name: {e}")
        except Exception as e:
            print(f"Unknow error renaming the directory: {e}")
