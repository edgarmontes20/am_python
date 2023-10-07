import random
import string
import warnings
import nltk
from nltk.stem import WordNetLemmatizer                                                                            
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
# from file import File
# from directory import Directory
# from charts import chart



class Nlp:
    def __init__(self, directory, path_corpus):
        self.sent_tokens = []
        self.GREETING_INPUTS = ("hi", "hello", "greetings", "sup", "what's up", "hey")
        self.GREETING_RESPONSES = ["hey", "hi","*nods*", "hi there", "hello", "I am glad you are chatting with me"]
        self.BOT_NAME = "ER-Bot"
        self.directory = directory
        self.path_corpus = path_corpus

    def initialize_nlp(self):
        
        warnings.filterwarnings('ignore')
        
        #Bajar vocabulario auxiliar
        #*************************#
        
        #Paquete de datos que contiene modelos y recursos para la tokenización de texto en diferentes idiomas. 
                
        #Popular 
        nltk.download('popular', quiet=True)
        
        #Punkt proporciona reglas y algoritmos para dividir el texto en oraciones
        nltk.download('punkt', quiet=True)
        
        nltk.download('wordnet', quiet=True)

        #Lee el contenido del archivo para tokenizarlo posteriormente
        with open(self.path_corpus, 'r', encoding='utf8', errors='ignore') as fin:
            row = fin.read().lower()

        #Para dividir un texto en oraciones individuales. 
        self.sent_tokens = nltk.sent_tokenize(row)

    def lem_tokens(self, tokens):
        """Lematiza las palabras base (lema): "corriendo", "corre", "corrió" --> "correr".

        Args:
            tokens (list): Lista con palabras o tokens individuales

        Returns:
            (list): Lista con palabras lematizadas
        """
        lemmer = WordNetLemmatizer()
        return [lemmer.lemmatize(token) for token in tokens]

    def lem_normalize(self, text):
               
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        
        #word_tokenize --> divide un texto o una oración en una lista de palabras o tokens individuales.
        #                   "Hello, how are you today?" --> ['Hello', ',', 'how', 'are', 'you', 'today', '?']
        
        #Devuelve un texto normalizado (convierte a minusculas, elimina puntuciación y lematiza)
        return self.lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    #Retornar un saludo si el suario envia uno
    def greeting(self, sentence):
        for word in sentence.split():
            if word.lower() in self.GREETING_INPUTS:
                return random.choice(self.GREETING_RESPONSES)

    #Procesar el input del usuario, obtener la respuesta y retornarla
    def response(self, user_response):
        bot_response = ''
        
        # Adiciona la respuesta del usuario a la lista de tokens enviados para procesar la similitud
        self.sent_tokens.append(user_response)
        
        #Crea y entrena un modelo de Vectorizador Tf-Idf
        TfidfVec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        
        #Obtiene el valor más similar usando metodo de similitud de coseno
        vals = cosine_similarity(tfidf[-1], tfidf)
        
        #Obtiene el índice de respuestas para elegir de la matriz ([-2]: últimos 2 elementos)
        #Respuesta más similar
        idx = vals.argsort()[0][-2]
        
        #Obtiene una copia del array "vals" reducido
        flat = vals.flatten()
        flat.sort()

        #Incluye a la respuesta del bot la cadena de respuesta
        if flat[-2] == 0:
            bot_response = bot_response + "I am sorry, but I don't understand your request"
        else:
            bot_response = bot_response + self.sent_tokens[idx]
        
        #Elimina la respuesta del usuario de la lista de tokens enviados
        self.sent_tokens.remove(user_response)

        return bot_response

    def talk_to_client(self, message):
        print(f"{self.BOT_NAME}: " + message)

    # def exc_chatbot(self):

    #     flag = True
    #     self.talk_to_client(f"My name is {self.BOT_NAME}. I will answer your queries about file and directory manipulation .")
    #     while flag:
    #         self.talk_to_client("Please type a request about files and directories. If you want to exit, type Bye!")
    #         user_response = input()
    #         if "bye" in user_response.lower():
    #             flag = False
    #             self.talk_to_client("Bye! take care..")
    #         elif "thank" in user_response.lower():
    #             flag = False
    #             self.talk_to_client("You are welcome..")
    #         elif self.greeting(user_response) is not None:
    #             self.talk_to_client(self.greeting(user_response))
    #         else:
                
    #             try:
    #                 tokens = nltk.word_tokenize(user_response)
    #                 self.talk_to_client(self.response(user_response))
    #                 if 'list files' in user_response:
    #                     print(self.directory.list_files())
    #                 elif 'create file' in user_response:
    #                     name = tokens[tokens.index('file') + 1]
    #                     self.directory.create_file(name)
    #                 elif 'create directory' in user_response:
    #                     name = tokens[tokens.index('directory') + 1]
    #                     self.directory.create_directory(name)
    #                 elif 'rename directory' in user_response:
    #                     new_name = tokens[tokens.index('to') + 1]
    #                     self.directory.rename_directory(new_name)   
    #                 elif 'rename' in user_response:
    #                     old_name = tokens[tokens.index('rename') + 1]
    #                     new_name = tokens[tokens.index('to') + 1]
    #                     file = File(os.path.join(self.directory.path, old_name))
    #                     file.rename(os.path.join(self.directory.path, new_name))                    
    #                 elif 'delete file' in user_response:
    #                     name = tokens[tokens.index('file') + 1]
    #                     file = File(os.path.join(self.directory.path, name))
    #                     print(file)
    #                     file.delete()
    #                 elif 'search' in user_response or 'find' in user_response or 'lookup' in user_response:
    #                     search_keywords = ['search', 'find', 'lookup']
    #                     #name = tokens[tokens.index('search') + 1]
    #                     name = tokens[tokens.index(next((word for word in tokens if word in search_keywords), None)) + 1] if any(word in tokens for word in search_keywords) else None
    #                     matches = self.directory.search_file(name)
    #                     print( f'Se encontraron los siguientes archivos: {", ".join(matches)}')
    #                 elif 'move file' in user_response:
    #                     tokens = user_response.split()
    #                     # Encontrar los índices de las palabras clave "move" y "to"
    #                     move_index = tokens.index("file")
    #                     to_index = tokens.index("to")
    #                     file_path = " ".join(tokens[move_index + 1:to_index])
    #                     destination_path = " ".join(tokens[to_index + 1:])

    #                     print(file_path)
    #                     print(destination_path)
    #                     self.directory.move_file(file_path, destination_path)
    #                 elif 'change permissions' in user_response:
    #                     tokens = user_response.split()
    #                     # Encontrar los índices de las palabras clave "move" y "to"
    #                     name = tokens.index("permissions")
    #                     to_index = tokens.index("to")
    #                     file_path = " ".join(tokens[name + 1:to_index])
    #                     name = tokens[tokens.index('permissions') + 1]
    #                     permissions = int(" ".join(tokens[to_index + 1:]), 8)
    #                     file = File(os.path.join(self.directory.path, name))
    #                     file.change_permissions(permissions)
    #                 elif 'graphic' in user_response:
    #                     name = tokens[tokens.index('permissions') + 1]
    #                     entity_select = tokens[tokens.index('entity') + 1]
    #                     #chart.graph_chart(entity_select)
    #             except LookupError as err:
    #                 print ('Tenemos un error',err)             

# if __name__ == '__main__':
    
#     directory_path = r'D:\AM\chatbot\data\data_test'
#     print(directory_path)

#     #obtener la ruta absoluta del directorio.
#     absolute_path = os.path.abspath(directory_path)
#     directory = Directory(absolute_path)
    
#     chatbot = Nlp(directory)
#     print('Intanciado objeto')
#     chatbot.initialize_nlp()
#     print('Inicializado modulo nlp')
#     chatbot.exc_chatbot()
#     print('Corriendo nlp')