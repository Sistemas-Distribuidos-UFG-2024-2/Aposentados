#!/bin/bash

# Lista de scripts a serem executados
scripts=(
    "loadbalancer.py"
    "servico_saude.py"
    "middleware.py"
    "servico_nomes.py"
    "servidor.py"
    "app.py"
)

# Caminho para o interpretador Python (ajuste se necessário)
python_cmd="python3"  # Assumindo que Python 3 é o padrão

echo "Iniciando scripts..."

# Loop para executar cada script
for script in "${scripts[@]}"; do
    echo "Abrindo terminal para: $script"
    # Executa o script em um novo terminal
    gnome-terminal -- bash -c "$python_cmd $script; exec bash"
    sleep 1 # Pausa de 1 segundo para evitar sobreposição
done

echo "Todos os scripts foram iniciados."
