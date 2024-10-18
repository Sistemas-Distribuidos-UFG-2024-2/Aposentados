const net = require('net');
const readline = require('readline');

// Cria uma interface para entrada de dados do usuário
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Função para coletar os dados do funcionário
function coletarDados(callback) {
    rl.question("Informe o nome do funcionário: ", (nome) => {
        rl.question("Informe o cargo do funcionário (operador/programador): ", (cargo) => {
            rl.question("Informe o salário do funcionário: ", (salario) => {
                callback(nome, cargo, salario);
            });
        });
    });
}

// Criando o socket cliente
const client = new net.Socket();

client.connect(12345, 'localhost', () => {
    console.log('Conectado ao servidor');

    // Coletar os dados do funcionário e enviar ao servidor
    coletarDados((nome, cargo, salario) => {
        const dados = `${nome},${cargo},${salario}`;
        client.write(dados);
    });
});

// Receber o resultado do servidor
client.on('data', (data) => {
    console.log(data.toString());
    client.destroy();  // Fecha a conexão após receber a resposta
});

// Tratamento de erro
client.on('error', (err) => {
    console.log(`Erro: ${err.message}`);
    client.destroy();
});

// Finalizar o readline quando o cliente é destruído
client.on('close', () => {
    rl.close();
});
