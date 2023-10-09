# am_python
## proyecto_chatbot


Ejecutar chatbot.py
```sh
python3 chatbot.py
```
Crear ambiente virtual 
```sh
pip install -r requirements.txt
```

Activa el ambiente virtual para windows

```sh
.\env\Scripts\activate

```
### Directorios y rutas

Al iniciar solicitara una ruta de trabajo para directorios y archivos.

Se debe configurar la ruta del path_corpus files_directories.txt en el chatbot.py en __main__ esto dependera del directorio donde se descargo el arbol de directorios del proyecto.

Ejemplo:

```sh
path_corpus = r"E:\Python_PCAP\Proyecto_PCAP\chatbot\modules\files_directories.txt"

```

### Instrucciones de uso del chatbot

Al inicio solicitara una ruta absoluta de trabajo:

1-Se debe crear una Base de datos en mysql con el nombre CONTRACTS_DB, esta es la cadena de conexion:

```sh
db_url = "mysql+mysqlconnector://root:admin@localhost/CONTRACTS_DB"

```
### crear tabla contrato en BD

```sh 
create table contrato (
nivel_entidad varchar(255) 
,nombre_de_la_entidad varchar(255) 
,nit_de_la_entidad varchar(255) 
,departamento_entidad varchar(255) 
,municipio_entidad varchar(255) 
,estado_del_proceso varchar(255) 
,modalidad_de_contrataci_n varchar(255) 
,objeto_a_contratar varchar(600) 
,objeto_del_proceso varchar(600) 
,tipo_de_contrato varchar(255) 
,fecha_de_firma_del_contrato date 
,fecha_inicio_ejecucion varchar(50) 
,fecha_fin_ejecucion varchar(50) 
,tipo_contrato varchar(255) 
,numero_del_contrato varchar(255) 
,numero_de_proceso varchar(255) 
,valor_contrato decimal(15,2) 
,nom_raz_social_contratista varchar(255) 
,url_contrato varchar(255) 
,origen varchar(255) 
,documento_proveedor varchar(40) 
,year_firma varchar(6) 
,month_firma varchar(6) 
,fecha_firma_yyyymm varchar(20)
);
```

2-En las instrucciones de crear directorios y archivos se debe poner la palabra para la instruccion y el nombre del archivo y directorio que se desea que tenga el directorio o archivo.

Ejemplo palabras para uso del chatbot:

`create directory new` -> Crea directorio new para este caso
`create file file_1.txt` -> crea archivo file_1.txt para este caso
`list files` -> muestra la lista de archivos y directorios de una carpeta
`rename directory hola to nuevo` -> cambia el nombre del directorio hola por nuevo
`rename file archivo.txt to renombrado.txt` -> cambia el nombre del archivo.txt por renombrado.txt
`move file` -> solicitara la ruta absoluta del origen y del destino para mover el archivo asi
ejemplo:
    origen Y:\test\file_1.txt 
    destino Y:\test\temp
`delete file files.csv` -> borra archivo files.csv
`change permissions files.csv to 745` -> cambia los permisos del archivo files.csv al formato octal 745
`search files_1.txt` -> busca el archivo files_1.txt e indica la ruta absoluta donde lo encuentra
`insert data to DB` -> solicita la ruta absoluta del archivo de datos procesados *.csv a cargar en la BD my sql
`graphic` -> solicita la ruta del insumo csv para lectura de datos, el NIT y el año para graficar. Genera y guarda la grafica.

3-En algunos casos se solicita ingresar la ruta absoluta para el proceso 

ejemplo, use la ruta donde descargo el programa: 

```sh
E:\Python_PCAP\Proyecto_PCAP\chatbot\data\data_et\data_processed.csv
```

4-Los graficos generados quedaran grabados en la ruta del insumo de datos csv.
