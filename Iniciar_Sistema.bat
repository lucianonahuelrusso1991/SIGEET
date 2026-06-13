@echo off
color 0B
title Sistema de Gestion Escolar - Servidor

echo ========================================================
echo         SISTEMA DE GESTION ESCOLAR - INICIANDO...
echo ========================================================
echo.
echo Por favor, NO cierres esta ventana negra mientras usas el sistema.
echo.

:: Activar el entorno virtual
call entorno_escuela\Scripts\activate.bat

:: Iniciar el servidor local en segundo plano
start /B python manage.py runserver

:: Esperar 3 segundos para que el servidor termine de arrancar
timeout /t 3 /nobreak > NUL

:: Abrir la pagina en el navegador predeterminado
echo Abriendo el navegador...
start http://127.0.0.1:8000

echo.
echo ========================================================
echo El sistema esta funcionando.
echo Para APAGAR el sistema, simplemente cierra esta ventana.
echo ========================================================
:: Mantener la ventana abierta
cmd /k
