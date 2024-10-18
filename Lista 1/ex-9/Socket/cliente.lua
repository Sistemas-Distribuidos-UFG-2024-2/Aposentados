local socket = require("socket")

-- Função cliente para enviar o valor e o naipe da carta
function cliente(valor, naipe)
    local cliente_socket = socket.tcp()
    cliente_socket:connect("localhost", 12345)
    
    -- Enviar valor e naipe como uma string no formato "valor,naipe"
    local dados = valor .. "," .. naipe
    cliente_socket:send(dados .. "\n")  -- Adiciona \n para indicar o fim da mensagem
    
    -- Receber a resposta do servidor
    local resposta = cliente_socket:receive("*l")
    print("Nome da carta: " .. resposta)
    
    cliente_socket:close()
end

-- Exemplo: enviar valor 1 (Ás) e naipe 1 (Ouros)
cliente(1, 1)
