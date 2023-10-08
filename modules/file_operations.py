"""Clase para las operaciones con Archivos"""
import os
import shutil
from modules.directory_operations import Directory

class File(Directory):
    """Clase para el manejo de archivos."""
    def __init__(self, file_name):
        """Inicializa una instancia de la clase File con el nombre de archivo especificado."""
        super().__init__(os.path.dirname(file_name))  # Llama al constructor de la clase base Directory

    def create_file(self, file_path):
        """Crea un nuevo archivo en la ubicación especificada si no existe."""
        if not os.path.isfile(file_path):
            try:
                with open(file_path, 'w') as file:
                    file.write("Contenido del nuevo archivo.")
                print(f"File '{os.path.basename(file_path)}' created successfully.")
            except OSError as e:
                    print(f"Error creating the file: {e}")
        else:
            print(f"The file '{os.path.basename(file_path)}' already exists.")

    def move_file(self, source_path, destination_path):
        """Mueve el archivo a la ubicación especificada."""
        #print(f'move_file primer exists {os.path.join(source_path, self.name)}')
        #print(f'move_file segundo exists {os.path.dirname(destination_path)}')
        try:
            if os.path.exists(os.path.join(source_path)) and os.path.exists(os.path.dirname(destination_path)):
                shutil.move(os.path.join(source_path), destination_path)
                # seguimiento actualizado de la ubicación y el nombre del archivo dps del move
                self.path = os.path.dirname(destination_path)
                self.name = os.path.basename(destination_path) 
                print(f"The file has moved successfully to '{destination_path}'.")
            else:
                print("Please validate the origin and destination path they do not exist")

        except shutil.Error as e:
            print(f"Error of shutil moving file: {e}")
        except Exception as e:
            print(f"Another error moving file: {e}")

    def rename_file(self, path , new_name):
        """Cambia el nombre del archivo."""
        try:
            os.rename(path, os.path.join(os.path.dirname(path), new_name))  # Cambia el nombre en la ruta completa
            self.dir_name = os.path.join(os.path.dirname(path), new_name)  # Actualiza el nombre del objeto File
            print(f"The file has been renamed to '{new_name}'.")
        except FileNotFoundError:
            print(f"Error renaming: The file '{self.name}' was not found.")
        except PermissionError:
            print(f"Error: You do not have permissions to change the file name.")
        except OSError as e:
            print(f"Error renaming the file name: {e}")
        except Exception as e:
            print(f"Unknow error renaming the file: {e}")

    def searcher_file(self, path, file_to_search):
        """Busca un archivo con el nombre especificado en el directorio especificado y sus subdirectorios."""
        try:
            # os.walk() comienza en un directorio raíz y se mueve a través de todos sus subdirectorios de manera recursiva
            # root: El primer valor es la ruta del directorio actual.
            # dirs: El segundo valor es una lista de nombres de subdirectorios en el directorio actual.
            # files: El tercer valor es una lista de nombres de archivos en el directorio actual.
            for root, dirs, files in os.walk(path):
                if file_to_search in files:
                    print(f"The file '{file_to_search}' was found in: {os.path.join(root, file_to_search)}")
        except Exception as e:
            print(f"Unexpected error searching file: {e}")

    def change_permissions_file(self, file_path, permissions_octal):
        """Cambia los permisos del archivo al valor octal especificado."""
        try:
            # Representa en notación octal, cada permiso (lectura, escritura, ejecución) se asigna a un número octal específico.
            permissions = int(permissions_octal, 8)
            os.chmod(file_path, permissions)
            print(f"The permissions of the file '{os.path.basename(file_path)}' has been changed to {permissions_octal}.")
        except ValueError:
            print(f"Error: '{permissions_octal}' is not a valid octal representation of permissions.")
        except FileNotFoundError:
            print(f"Permissions error: The file '{file_path}' was not found.")
        except PermissionError:
            print(f"Error: You do not have permissions to change the file permissions.")
        except OSError as e:
            print(f"Error changing the file permissions: {e}")
        except Exception as e:
            print(f"Unknow error changing permissions: {e}")

    def delete_file(self, file_path):
        """Elimina un archivo especificado por su ruta."""
        try:
            os.remove(file_path)
            print(f"The file '{os.path.basename(file_path)}' has been deleted successfully.")
        except FileNotFoundError:
            print(f"Error: The file '{os.path.basename(file_path)}' was not found.")
        except PermissionError:
            print(f"Error: You do not have permissions to delete the file.")
        except OSError as e:
            print(f"Error deleteing the file: {e}")
        except Exception as e:
            print(f"Unknow error deleting file: {e}")




