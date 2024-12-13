@echo off
set python_cmd=python

echo Iniciando scripts...

start cmd /k %python_cmd% loadbalancer.py
start cmd /k %python_cmd% servico_saude.py
start cmd /k %python_cmd% middleware.py
start cmd /k %python_cmd% servico_nomes.py
start cmd /k %python_cmd% servidor.py
start cmd /k %python_cmd% app.py

echo Todos os scripts foram iniciados.
