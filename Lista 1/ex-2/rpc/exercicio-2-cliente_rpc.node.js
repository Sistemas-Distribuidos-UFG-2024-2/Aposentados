const xmlrpc = require('xmlrpc');
const readline = require('readline');

// Configurando o readline para coletar dados do usuário
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Criar cliente RPC
const client = xmlrpc.createClient({ host: 'localhost', port: 8000 });

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

// Coletar dados do usuário e chamar o servidor
coletarDados((nome, sexo, idade) => {
    // Fazer a chamada RPC ao servidor
    client.methodCall('verificar_maioridade', [nome, sexo, idade], (error, response) => {
        if (error) {
            console.log('Erro:', error);
        } else {
            console.log('Resposta do servidor:', response);
        }
        rl.close();
    });
});
