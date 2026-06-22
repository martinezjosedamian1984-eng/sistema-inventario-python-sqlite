# Sistema de Gestión de Inventario

# Descripción del proyecto

Este proyecto consiste en una aplicación de consola desarrollada en Python para gestionar el inventario de productos de un pequeño comercio.

La aplicación permite registrar productos, visualizar el inventario completo, buscar productos, actualizar información, eliminar registros y generar reportes de productos con bajo stock.

El proyecto fue desarrollado como parte del Proyecto Integrador Final de la materia Prácticas Profesionalizantes I, simulando un entorno profesional de trabajo en Ciencia de Datos e Inteligencia Artificial.

# Problema identificado

Muchos pequeños comercios llevan el control de sus productos de forma manual o desorganizada. Esto puede generar errores en el stock, dificultad para encontrar productos y falta de información para tomar decisiones.

# Solución propuesta

Se desarrolló un sistema de inventario en Python con persistencia de datos en SQLite. El sistema permite guardar la información de los productos en una base de datos local y consultar los datos desde una interfaz de terminal mejorada con la librería Rich.

# Tecnologías utilizadas

* Python
* SQLite
* Rich
* datetime
* Git
* GitHub
* Trello

# Funcionalidades principales

* Registrar nuevos productos.
* Visualizar productos registrados.
* Actualizar productos mediante su ID.
* Eliminar productos mediante su ID.
* Buscar productos por ID, nombre o categoría.
* Generar reportes de productos con bajo stock.
* Registrar fecha y hora de carga de productos.
* Mostrar información en tablas dentro de la terminal.

# Estructura del proyecto

```text
entregafinal/
├── entrega_final.py
├── README.md
├── requirements.txt
├── informe_etica.md
├── .gitignore
└── capturas/
```

# Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

2. Ingresar a la carpeta del proyecto:

```bash
cd entregafinal
```

3. Crear y activar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Instalar dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecutar la aplicación:

```bash
python entrega_final.py
```

# Base de datos

La aplicación utiliza SQLite. Al ejecutar el programa se crea automáticamente una base de datos local llamada `inventario.db`.

La tabla principal se llama `productos` y contiene los siguientes campos:

* id
* codigo
* nombre
* descripcion
* cantidad
* precio
* categoria
* fecha_registro

# Metodología de trabajo

Para la planificación del proyecto se utilizó una metodología ágil basada en Scrum. El trabajo se organizó en tareas dentro de un tablero Trello, separando actividades en etapas como backlog, tareas pendientes, tareas en progreso, revisión y finalización.

# Roles simulados

Aunque el trabajo fue individual, se simularon roles propios de un equipo tecnológico:

* Product Owner: definición del problema y funcionalidades principales.
* Scrum Master: organización de tareas y seguimiento del avance.
* Developer: implementación del sistema en Python.
* Data/QA Analyst: pruebas de funcionamiento, validaciones y revisión de datos.

# Aprendizajes obtenidos

Durante el desarrollo del proyecto se practicó el uso de Python aplicado a un problema real, persistencia de datos con SQLite, validación de entradas, organización del código en funciones, documentación profesional y uso de herramientas colaborativas.

También se reforzó la importancia de planificar antes de programar, probar cada funcionalidad y documentar el proceso de trabajo.

# Mejoras futuras

* Crear una versión web con Flask.
* Agregar inicio de sesión para usuarios.
* Exportar reportes a CSV.
* Agregar gráficos de stock.
* Mejorar el diseño visual de la interfaz.
* Incorporar filtros más avanzados por categoría y precio.

# Autor

Proyecto desarrollado por Jose Damián Martínez para la materia Aproximación al Mundo Laboral.
