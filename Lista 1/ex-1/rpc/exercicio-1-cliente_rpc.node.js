const xmlrpc = require('xmlrpc');
const readline = require('readline');

// Cria a interface para coletar dados do funcionário
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Função para coletar dados do funcionário
function coletarDados(callback) {
    rl.question("Informe o nome do funcionário: ", (nome) => {
        rl.question("Informe o cargo do funcionário (operador/programador): ", (cargo) => {
            rl.question("Informe o salário do funcionário: ", (salario) => {
                callback(nome, cargo, parseFloat(salario));
            });
        });
    });
}

// Criando o cliente RPC para se conectar ao servidor
const client = xmlrpc.createClient({ host: 'localhost', port: 8000, path: '/' });

// Coletar os dados do funcionário e enviar ao servidor via RPC
coletarDados((nome, cargo, salario) => {
    client.methodCall('calcula_reajuste', [nome, cargo, salario], (error, value) => {
        if (error) {
            console.log('Erro: ', error);
        } else {
            console.log(value);  // Exibe o nome e o salário reajustado
        }
        rl.close();
    });
});
