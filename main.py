# Importar librerias
from fastapi import FastAPI
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string

# Descargar recursos necesarios de nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Crear la aplicación FastAPI
app = FastAPI()

# Especificar las rutas absolutas a los archivos Parquet usando raw strings para evitar problemas con las barras invertidas
movies_df_path = 'Dataset/movies_df.parquet' 
credits_cast_df_path = 'Dataset/credits_cast_df.parquet'
credits_crew_df_path = 'Dataset/credits_crew_df.parquet'

# Verificar que los archivos existen
if not os.path.exists(movies_df_path):
    raise FileNotFoundError(f"Archivo no encontrado: {movies_df_path}")
if not os.path.exists(credits_cast_df_path):
    raise FileNotFoundError(f"Archivo no encontrado: {credits_cast_df_path}")
if not os.path.exists(credits_crew_df_path):
    raise FileNotFoundError(f"Archivo no encontrado: {credits_crew_df_path}")

# Leer los archivos Parquet y cargar DataFrames
movies_df = pd.read_parquet(movies_df_path)
credits_cast_df = pd.read_parquet(credits_cast_df_path)
credits_crew_df = pd.read_parquet(credits_crew_df_path)

# Ruta raíz que devuelve un mensaje de bienvenida
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de películas"}

# Endpoint 1: Se ingresa un mes en idioma Español, devuelve la cantidad de películas que fueron estrenadas en el mes consultado
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):

    # Diccionario para mapear los meses en español a sus números correspondientes
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    # Convertir el mes ingresado a minúsculas
    mes = mes.lower()
    
    # Verificar si el mes ingresado es válido
    if mes not in meses:
        return "Mes ingresado no es válido. Por favor, ingrese un mes en español."
    
    # Obtener el número del mes correspondiente
    mes_numero = meses[mes]
    
    # Filtrar el DataFrame por el mes de estreno
    cantidad = movies_df[movies_df['release_date'].dt.month == mes_numero].shape[0]
    
    return f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"

# Endpoint 2: Se ingresa un día en idioma Español, devuelve la cantidad de películas que fueron estrenadas en día consultado
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):

    # Diccionario para mapear los días en español a sus números correspondientes
    dias_semana = {
        'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3, 'viernes': 4, 'sabado': 5, 'domingo': 6
    }
    
    # Convertir el día ingresado a minúsculas
    dia = dia.lower()
    
    # Verificar si el día ingresado es válido
    if dia not in dias_semana:
        return "Día ingresado no es válido. Por favor, ingrese un día en español."
    
    # Obtener el número del día correspondiente
    dia_numero = dias_semana[dia]
    
    # Filtrar el DataFrame por el día de estreno
    cantidad = movies_df[movies_df['release_date'].dt.dayofweek == dia_numero].shape[0]
    
    return f"{cantidad} películas fueron estrenadas el día {dia.capitalize()}"

# Endpoint 3: Se ingresa el título de una filmación, devuelve el título, el año de estreno y el score
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):

   # Filtrar el DataFrame para encontrar la fila con el título especificado
    filmacion = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    
    # Verificar si se encontró la filmación
    if filmacion.empty:
        return f"No se encontró ninguna filmación con el título '{titulo}'"
    
    # Extraer la información de la filmación
    titulo = filmacion['title'].values[0]
    año_estreno = filmacion['release_year'].values[0]
    score = filmacion['popularity'].values[0]
    
    return f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score de {score}"

# Endpoint 4: Se ingresa el título de una filmación, devuelve el título, la cantidad de votos y el valor promedio de las votaciones (No devuelve ningun valor si cuenta con menos de 2000 valoraciones) 
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):

    # Filtrar el DataFrame para encontrar la fila con el título especificado
    filmacion = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    
    # Verificar si se encontró la filmación
    if filmacion.empty:
        return f"No se encontró ninguna filmación con el título '{titulo}'"
    
    # Extraer la cantidad de votos
    cantidad_votos = filmacion['vote_count'].values[0]
    
    # Verificar si la cantidad de votos es al menos 2000
    if cantidad_votos < 2000:
        return f"La película '{titulo}' no cumple con la condición de tener al menos 2000 valoraciones."
    
    # Extraer el valor promedio de votaciones
    promedio_votos = filmacion['vote_average'].values[0]
    titulo = filmacion['title'].values[0]
    año_estreno = filmacion['release_year'].values[0]
    
    return f"La película '{titulo}' fue estrenada en el año {año_estreno}. La misma cuenta con un total de {cantidad_votos} valoraciones, con un promedio de {promedio_votos}"

# Endpoint 5: Se ingresa el nombre de un actor, devuelve el éxito del mismo medido a través del retorno, la cantidad de películas en las que ha participado y el promedio de retorno
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):

    # Convertir el nombre del actor a minúsculas para búsqueda insensible a mayúsculas/minúsculas
    nombre_actor = nombre_actor.lower()
    
    # Filtrar el DataFrame de créditos para encontrar todas las filas con el nombre del actor en el cast
    actor_movies = credits_cast_df[credits_cast_df['cast_name'].str.lower() == nombre_actor]
    
    # Verificar si se encontró al actor en alguna filmación
    if actor_movies.empty:
        return f"No se encontró a '{nombre_actor}' en el dataset."
    
    # Obtener el género del actor (asumiendo que todos los registros para el mismo actor tienen el mismo género)
    genero = actor_movies['cast_gender'].values[0]
    if genero == 1:
        titulo = "La actriz"
    elif genero == 2:
        titulo = "El actor"
    else:
        titulo = " "  # Caso por defecto si no se puede determinar el género
    
    # Obtener los IDs de las películas en las que ha participado el actor
    movie_ids = actor_movies['id'].unique()
    
    # Filtrar el DataFrame de películas para obtener las películas en las que ha participado el actor
    actor_movies_info = movies_df[movies_df['id'].isin(movie_ids)]
    
    # Calcular el retorno total y el promedio de retorno
    retorno_total = actor_movies_info['return'].sum()
    cantidad_peliculas = actor_movies_info.shape[0]
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    
    return f"{titulo} {nombre_actor.title()} ha participado de {cantidad_peliculas} filmaciones, consiguiendo un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación"

# Endpoint 6: Se ingresa el nombre de un director, devuelve el éxito del mismo medido a través del retorno. Además, devuelve el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):

    # Convertir el nombre del director a minúsculas para búsqueda insensible a mayúsculas/minúsculas
    nombre_director = nombre_director.lower()
    
    # Filtrar el DataFrame de créditos para encontrar todas las filas con el nombre del director en la crew y su rol sea 'Director'
    director_movies = credits_crew_df[(credits_crew_df['crew_name'].str.lower() == nombre_director) & 
                                          (credits_crew_df['crew_job'].str.lower() == 'director')]
    
    # Verificar si se encontró al director en alguna filmación
    if director_movies.empty:
        return f"No se encontró a '{nombre_director}' en el dataset."
    
    # Obtener los IDs de las películas dirigidas por el director
    movie_ids = director_movies['id'].unique()
    
    # Filtrar el DataFrame de películas para obtener las películas dirigidas por el director
    director_movies_info = movies_df[movies_df['id'].isin(movie_ids)]
    
    # Calcular el retorno total y el promedio de retorno
    retorno_total = director_movies_info['return'].sum()
    cantidad_peliculas = director_movies_info.shape[0]
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0
    
    # Crear una lista con la información de cada película
    peliculas_info = []
    for _, row in director_movies_info.iterrows():
        info = {
            'titulo': row['title'],
            'fecha_lanzamiento': row['release_date'],
            'retorno_individual': row['return'],
            'costo': row['budget'],
            'ganancia': row['revenue']
        }
        peliculas_info.append(info)
    
   # Crear un mensaje con la información del director
    mensaje = f"El director {nombre_director.title()} ha dirigido {cantidad_peliculas} películas. Ha conseguido un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    mensaje += "Detalles de las películas dirigidas: "
    
    for info in peliculas_info:
        mensaje += f"Título: {info['titulo']}, Fecha de Lanzamiento: {info['fecha_lanzamiento']}, Retorno: {info['retorno_individual']}, Costo: {info['costo']}, Ganancia: {info['ganancia']}\n"
    
    return mensaje

# Sistema de recomendacion: Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

def limpiar_texto(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Limpiar las descripciones de las películas
movies_df['clean_overview'] = movies_df['overview'].apply(lambda x: limpiar_texto(x) if isinstance(x, str) else '')

# Dar más peso a los géneros duplicando la información de géneros
movies_df['weighted_genres'] = movies_df['genres_name'] + ' ' + movies_df['genres_name'] + ' ' + movies_df['genres_name']

# Combinar los títulos, descripciones y géneros ponderados
movies_df['combined_features'] = movies_df['title'] + ' ' + movies_df['clean_overview'] + ' ' + movies_df['weighted_genres']

# Vectorización del texto usando TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(movies_df['combined_features'])

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):

    if titulo not in movies_df['title'].values:
        return f"La película '{titulo}' no se encontró en el dataset."
    
    # Obtener el índice de la película con el título dado
    idx = movies_df[movies_df['title'] == titulo].index[0]
    
    # Calcular la similitud del coseno entre la película dada y todas las demás
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

    # Obtener el ID de la colección de la película consultada
    collection_id = movies_df.at[idx, 'belongs_to_collection_id']
    
    # Obtener los índices de las películas con mayor similitud
    similar_indices = cosine_sim.argsort()[::-1][1:6]
    
    # Obtener los títulos de las películas similares
    similar_movies = movies_df.iloc[similar_indices]['title'].tolist()

    # Si la película pertenece a una colección, priorizar las películas de la misma colección
    if pd.notnull(collection_id):
        collection_movies = movies_df[movies_df['belongs_to_collection_id'] == collection_id]['title'].tolist()
        similar_movies = collection_movies + [movie for movie in similar_movies if movie not in collection_movies]

    # Excluir la película que se pasó como argumento de la lista de recomendaciones
    similar_movies = [movie for movie in similar_movies if movie != titulo]

    # Eliminar duplicados manteniendo el orden
    similar_movies = list(dict.fromkeys(similar_movies))

    # Si hay menos de 5 recomendaciones, agregar más basadas en la similitud
    if len(similar_movies) < 5:
        additional_indices = cosine_sim.argsort()[::-1][6:]
        additional_movies = movies_df.iloc[additional_indices]['title'].tolist()
        additional_movies = [movie for movie in additional_movies if movie not in similar_movies and movie != titulo]
        similar_movies.extend(additional_movies[:5 - len(similar_movies)])
    
    # Asegurarse de que no haya duplicados en la lista final
    final_recommendations = []
    for movie in similar_movies:
        if movie not in final_recommendations:
            final_recommendations.append(movie)
        if len(final_recommendations) == 5:
            break
    
    # Si después de eliminar duplicados aún hay menos de 5 recomendaciones, añadir más basadas en la similitud
    if len(final_recommendations) < 5:
        additional_indices = cosine_sim.argsort()[::-1][len(similar_movies)+1:]
        additional_movies = movies_df.iloc[additional_indices]['title'].tolist()
        additional_movies = [movie for movie in additional_movies if movie not in final_recommendations and movie != titulo]
        final_recommendations.extend(additional_movies[:5 - len(final_recommendations)])
    
    return final_recommendations[:5]


# Ejecutar la aplicación con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
