Descripción Breve del Proyecto:

El proyecto implementa un sistema de gestión para una empresa que administra órdenes de compra, emisión de facturas y envío de productos, utilizando Python con Flask y MySQL. Incluye un módulo de login, un menú principal y funcionalidades completas para registrar órdenes, calcular automáticamente el IVA (19%), generar facturas y marcar productos como despachados.

Además, incorpora un proceso real de Integración Continua (CI/CD) mediante GitHub Actions, automatizando instalación de dependencias, validación del código y un despliegue simulado, siguiendo un flujo de trabajo profesional con ramas, commits, merges y evidencias.


Integrantes:

Raúl Alvarez Zuñiga


Librerías Utilizadas:

(Python)

Flask: Framework web ligero para manejar rutas, formularios, sesiones y la estructura general de la aplicación.

mysql-connector-python: Librería que permite conectar Python con MySQL (Laragon) para gestionar la base de datos.

pytest: Herramienta de pruebas unitarias utilizada por el pipeline CI/CD para validar el funcionamiento del proyecto.


Instrucciones de Ejecución:

1) Iniciar Laragon

2) Abre Laragon

3) Presiona Start All (comprobar que MySQL esté activo)

4) Crear la Base de Datos (CREATE DATABASE proyecto_empresa;)

5) Ejecutar el script SQL de tablas (usuarios, órdenes, facturas, envíos).

6) Instalar Dependencias

7) En la terminal, dentro de la carpeta del proyecto (pip install -r requirements.txt" - Esto instalará: *Flask, *mysql-connector-python, *pytest (para CI/CD))

8) Ejecutar la Aplicación desde la carpeta del proyecto (src/app.py)

9) Ingresar al Sistema y abrir en el navegador: http://localhost:5000

10) Usar el usuario por defecto:
Usuario: admin
Clave: 1234

Listo, ahora solo a navegar por el sistema.