# Edu Tests

![](https://elcomercio.pe/resizer/v2/6Y2EDIISGFGVFANEVDCR5LCG34.jpg?auth=f58b5c647a09717054d85bb8b9a6bc624bfcb14fe9c60b5246730ea6a513e2b0&width=1200&height=810&quality=90&smart=true)

## Descripción

Edu Tests es una aplicación diseñada para la gestión de pruebas y evaluaciones. Permite crear pruebas con preguntas y sus respectivas alternativas, asignar estudiantes a las pruebas, asignar respuestas de los estudiantes y obtener los puntajes obtenidos por ellos en cada prueba.

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

1. Como está hosteado en Render, si pasa mucho tiempo inactivo se demorará en reactivarse, aproximadamente 1 minuto para que empiece a funcionar la API. Cualquier cosa, contactarme para reiniciar el server!
2. Por simplicidad, no se implementaron métodos `PUT` ni `DELETE`.
3. Si la creación de alguna pregunta o de alguna alternativa falla, **no se crea nada** de lo mencionado.
4. Se deja a Django la asignación de IDs para las pruebas, preguntas y alternativas.
5. La explicación de la pregunta puede ser vacía, pues puede no ser necesaria en la prueba.
6. El ID de las preguntas debe ser el correspondiente al id que tiene en la DB.
7. El ID de las respuestas del enunciado fue cambiado a `answer_number`, que corresponde al número de respuesta relativo a la pregunta. Eso se hizo así para hacerlo calzar más fácilmente cuando se asignen las respuestas de un estudiante. No se debe poner el ID de la base de datos.
8. Cada pregunta debe tener entre 1 y 5 alternativas, si no, arroja error.
9. Si el estudiante eligió, por ejemplo, la alternativa 5, pero la pregunta tiene 3 alternativas, se cuenta como que **no la respondió**.
10. Si en la asignación de estudiantes a pruebas o en la asignación de alternativas hay algunos que funcionan y otros que fallan, se optó por usar un _207 Multi Status_ en vez de arrojar error, pues los alumnos que sí existían, sí se asignaron.
11. Si se asignan respuestas a alumnos que
12. Se hicieron un par de validaciones cuando se asignan las respuestas, pero no todas por simplicidad del código (Iba a quedar muy engorroso si se validaban todos los campos, pero lo tuve en cuenta).
13. En django está instalada la librería `django-cors-headers` que se usa para poder conectarse a la api desde un frontend. De hecho está incluida la ruta `http://localhost:5173` por si en un futuro se desea realizar un front para la aplicación. Si ese front es desplegado, se debe agregar la ruta a `CORS_ORIGIN_WHITELIST` en el archivo `settings.py`.
14. Pensé en hacer un frontend pero en honor al tiempo no lo hice.

## Organización de archivos

En la carpeta `api` se encuentran archivos importantes como `models.py` que contiene los modelos de la DB,`serializer.py` los serializadores de cada modelo, `views.py` las funciones que utiliza cada ruta, en `urls.py` las rutas. También se encuentran las migraciones en la carpeta `migrations`.

En la carpeta `eduapi` se encuentran archivos de configuración como `settings.py`.

En la carpeta `fixtures` se encuentran los datos que serán cargados a la DB cuando la aplicación inicia por primera vez.

El archivo `build.sh` es utilziado en producción para levantar la aplicación.

## Recomendaciones para los estudiantes

Las recomendaciones para cada estudiante pueden basarse en sus fortalezas y áreas de mejora. Si destacan en ciertos temas, se les puede sugerir que trabajen con ejercicios más complejos o incluso que le enseñen a sus compañeros, ya que esto refuerza más su conocimiento.

En los tópicos donde presenten dificultades, se debe identificar de raíz de donde proviene con una retroalimentación para ver en dónde se encuentra la debilidad y ofrecer apoyo adicional como clases extras, nuevos métodos de estudio o pedir aydua a sus compañeros. y por su puesto se le debe hacer un seguimiento continuo para asegurar que el estudiante progrese de manera constante, entendiendo cada vez mejor la materia.
