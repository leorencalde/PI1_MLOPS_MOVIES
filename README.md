# Proyecto de Recomendación de Películas 
# (Machine Learning Ops) 🤖

## Descripción

Este repositorio contiene un proyecto de Machine Learning para sistemas de recomendación, que incluye un ETL (Extract, Transform, Load) y un Análisis Exploratorio de Datos (EDA).

El proyecto implementa una API para la recomendación de películas utilizando FastAPI. La API permite realizar diversas consultas sobre un conjunto de datos de películas, incluyendo la obtención de recomendaciones basadas en similitudes, la búsqueda de películas por mes o día de estreno, y la información sobre actores y directores.

## Estructura del Proyecto

- **Dataset/**: Contiene los archivos Parquet generados a partir del proceso ETL.
  
- **ETL/**: Incluye el notebook utilizado para la limpieza y transformación de datos.
  
- **EDA/**: Contiene el notebook del Análisis Exploratorio de Datos.
  
- **main.py**: Archivo principal de la API, donde se definen los endpoints y la lógica de negocio.
  
- **requirements.txt:** Lista de dependencias necesarias para ejecutar el proyecto.

## Funcionalidades `Endpoints`

- **`GET /cantidad_filmaciones_mes/{mes}`:** Devuelve la cantidad de películas estrenadas en el mes consultado.
  
- **`GET /cantidad_filmaciones_dia/{dia}`:** Devuelve la cantidad de películas estrenadas en el día consultado.
  
- **`GET /score_titulo/{titulo_de_la_filmacion}`:** Devuelve el título, año de estreno y score de una filmación.
  
- **`GET /votos_titulo/{titulo_de_la_filmacion}`:** Devuelve el título, la cantidad de votos y el promedio de votaciones de una filmación.
  
- **`GET /get_actor/{nombre_actor}`:** Devuelve el éxito de un actor medido a través del retorno, la cantidad de películas en las que ha participado y el promedio de retorno.
  
- **`GET /get_director/{nombre_director}`:** Devuelve el éxito de un director medido a través del retorno, el nombre de cada película dirigida con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
  
- **`GET /recomendacion/{titulo}`:** Devuelve una lista de películas similares basadas en el título proporcionado.

## Despliegue en Render

La API ha sido desplegada utilizando Render. Puedes acceder a la API en el siguiente enlace:

https://mlops-movies-leonardorenteria.onrender.com/docs

## Notebook de ETL

El notebook utilizado para la limpieza y transformación de los datos se encuentra en la carpeta ETL. Este notebook contiene el proceso de extracción, transformación y carga de los datos desde los archivos CSV originales hasta los archivos Parquet utilizados por la API.

## Notebook de EDA

Contiene el análisis exploratorio de datos, incluyendo visualizaciones y análisis de las relaciones entre las variables del dataset.

## Sistema de Recomendación de Películas

- **Descripción:** El sistema de recomendación de películas implementado en el endpoint `/recomendacion/{titulo}` utiliza técnicas de Machine Learning para sugerir películas similares a la proporcionada por el usuario. Este sistema se basa en la similitud de contenido utilizando la vectorización de características combinadas de las películas.

- **Implementación:**

  1. Extracción de Características:
 
     - Se combinan varias características relevantes de las películas (como título, género, descripción) en una única columna llamada `combined_features`.
    
     - Se utiliza la vectorización TF-IDF (Term Frequency-Inverse Document Frequency) para convertir estas características textuales en una matriz numérica que representa la importancia de las palabras en cada película.
    
  2. Cálculo de Similitud:

     - Se calcula la similitud del coseno entre la película proporcionada y todas las demás películas del dataset.
    
     - La similitud del coseno mide la similitud entre dos vectores en función del ángulo entre ellos, proporcionando un valor entre 0 y 1.
    
  3. Priorización por Colección:
 
     - Si la película proporcionada pertenece a una colección, se priorizan las películas de la misma colección en las recomendaciones.
    
     - Esto asegura que las secuelas y películas relacionadas se sugieran primero.
    
  4. Generación de Recomendaciones:

     - Se seleccionan las películas con mayor similitud.
    
     - Se eliminan duplicados y se asegura que la película proporcionada no esté en la lista de recomendaciones finales.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/leorencalde/PI1_MLOPS_MOVIES.git
   cd PI1_MLOPS_MOVIES

2. Crea un entorno virtual:
   ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instala las dependencias:
   ```bash
    pip install -r requirements.txt

## Uso

1. Corre la aplicación:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

2. Abre tu navegador y navega a http://127.0.0.1:8000 para ver el mensaje de bienvenida.

3. Para ver la documentación interactiva de la API, navega a http://127.0.0.1:8000/docs.

## Contribuciones 

Las contribuciones son bienvenidas. Por favor, sigue los pasos a continuación para contribuir:

1. Haz un fork del repositorio.
   
2. Crea una nueva rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).

3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).

4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).

5. Abre un Pull Request.

## Contacto 

**LEONARDO RENTERIA**
   - Email: `leo921120@hotmail.com`
   - Telefono: `+573138228947`
   - Ubicación: `Bogotá DC, Colombia`



