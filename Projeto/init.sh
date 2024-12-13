#!/bin/bash

# Lista de scripts a serem executados
scripts=(
    "loadbalancer.py"
    "servico_saude.py"
    "middleware.py"
    "servico_nomes.py"
    "servidor.py"
    "client.py"
)

# Caminho para o interpretador Python (ajuste se necessário)
python_cmd="python"

echo "Iniciando scripts..."

for script in "${scripts[@]}"; do
    echo "Abrindo terminal para: $script"
    # Use o comando 'cmd.exe' com argumentos completos para evitar problemas de execução
    cmd.exe /c start "Executando $script" $python_cmd $script
    sleep 1 # Pausa de 1 segundo para evitar sobreposição
done

echo "Todos os scripts foram iniciados."