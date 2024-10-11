# Edu Tests

## Descripción

Edu Tests es una aplicación diseñada para la gestión de pruebas y evaluaciones. Permite crear pruebas con preguntas y alternativas, asignar estudiantes a las pruebas, asignar respuestas de los estudiantes y obtener los puntajes obtenidos de ellos en cada prueba.

## Requisitos (para ejecutar en local)

- Python 3.12.7

## Instrucciones para ejecutarlo en local

1. Abrir cmd y entrar a la carpeta back con el comando `cd back`
2. (Opcional) Crear un entorno virtual con `python -m venv env`
3. - Activar el entonrno virtual con `.\env\Scripts\activate` para Windows
   - Activar el entonrno virtual con `source env/bin/activate` para macOS/Linux
4. Instalar las dependencias con `pip install -r requirements.txt`
5. Limpiar la base de datos (está en la nube) con `python manage.py flush --no-input`
6. Ejecutar las migraciones con `python manage.py migrate`
7. Cargar la data inicial con `python manage.py loaddata fixtures/fixtures.json`
8. (Opcional) Crear un superusuario para django con el comando `python manage.py createsuperuser`
9. Correr el servidor con `python manage.py runserver`

## Para acceder al servicio en línea

- La URL de la API es: https://edu-tests-back.onrender.com/api/

## Rutas

- Crear y obtener un estudiante: https://edu-tests-back.onrender.com/api/students/
- Crear una prueba: `POST` https://edu-tests-back.onrender.com/api/test/
- Obtener una prueba por el id: `GET` https://edu-tests-back.onrender.com/api/test/{test_id}
- Obtener todas las pruebas: `GET` https://edu-tests-back.onrender.com/api/tests/
- Asignar estudiantes a una prueba: `POST` https://edu-tests-back.onrender.com/api/{test_id}/assign/
- Asignar las respuestas respondidas por los alumnos en una prueba: `POST` https://edu-tests-back.onrender.com/api/{test_id}/answers/
- Obtener los puntajes de los alumnos de una prueba: `GET` https://edu-tests-back.onrender.com/api/{test_id}/answers/

## Consideraciones y suposiciones

1. Por simplicidad, no se implementaron métodos `PUT` ni `DELETE`.
2. Si la creación de alguna pregunta o de alguna alternativa falla, **no se crea nada** de lo mencionado.
3. Se deja a Django la asignación de IDs para las pruebas, preguntas y alternativas.
4. La explicación de la pregunta puede ser vacía, pues puede no ser necesaria en la prueba.
5. EL ID de las respuestas del enunciado fue cambiado a `answer_number`, que corresponde al número de respuesta relativo a la pregunta. Eso se hizo así para hacerlo calzar más fácilmente cuando se asignen las respuestas de un estudiante.
6. Si el estudiante eligió, por ejemplo, la alternativa 5, pero la pregunta tiene 3 alternativas, se cuenta como que **no la respondió**.
7. Si en la asignación de estudiantes a pruebas o en la asignación de alternativas hay algunos que funcionan y otros que fallan, se optó por usar un _207 Multi Status_ en vez de arrojar error, pues los alumnos que sí existían, sí se asignaron.
8. Se hicieron un par de validaciones cuando se asignan las respuestas, pero no todas por simplicidad del código.
9. En django está instalada la librería `django-cors-headers` que se usa para poder conectarse a la api desde un frontend. De hecho está incluida la ruta `http://localhost:5173` por si en un futuro se desea realizar un front para la aplicación. Si ese front es desplegado, se debe agregar la ruta a `CORS_ORIGIN_WHITELIST` en el archivo `settings.py`.

## Recomendaciones para los estudiantes

Las recomendaciones para cada estudiante pueden basarse en sus fortalezas y áreas de mejora. Si destacan en ciertos temas, se les puede sugerir que trabajen con ejercicios más complejos o incluso que le enseñen a sus compañeros, ya que esto refuerza más su conocimiento.

En los tópicos donde presenten dificultades, se debe identificar de raíz de donde proviene con una retroalimentación para ver en dónde se encuentra la debilidad y ofrecer apoyo adicional como clases extras, nuevos métodos de estudio o pedir aydua a sus compañeros. y por su puesto se le debe hacer un seguimiento continuo para asegurar que el estudiante progrese de manera constante, entendiendo cada vez mejor la materia.
