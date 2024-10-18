const net = require('net');
const readline = require('readline');

// Configurando o readline para coletar dados do usuário
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Função para coletar os dados da pessoa
function coletarDados(callback) {
    rl.question('Informe o nome: ', (nome) => {
        rl.question('Informe o sexo (masculino/feminino): ', (sexo) => {
            rl.question('Informe a idade: ', (idade) => {
                callback(nome, sexo, idade);
            });
        });
    });
}

// Criar conexão com o servidor
const client = new net.Socket();
client.connect(5000, 'localhost', () => {
    console.log('Conectado ao servidor.');

    // Coletar os dados do usuário e enviar para o servidor
    coletarDados((nome, sexo, idade) => {
        const dados = `${nome},${sexo},${idade}`;
        client.write(dados);  // Envia os dados para o servidor
    });
});

// Receber a resposta do servidor
client.on('data', (data) => {
    console.log(data.toString());  // Exibir a resposta do servidor
    client.destroy();  // Fechar a conexão após receber a resposta
});

// Fechar a conexão
client.on('close', () => {
    console.log('Conexão encerrada.');
    rl.close();
});
