from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def run_ftp_server():
    # Cria o responsável pela autenticação de usuário
    authorizer = DummyAuthorizer()
    
    # Adiciona um usuário (usuário, senha, diretório, permissões)
    authorizer.add_user("user", "password", "/path/to/ftp/folder", perm="elradfmw")
    
    # Configura o manipulador de FTP (como o servidor vai responder às requisições)
    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Cria o servidor FTP
    server = FTPServer(("0.0.0.0", 21), handler)
    
    # Inicia o servidor
    print("Servidor FTP iniciado...")
    server.serve_forever()

if __name__ == "__main__":
    run_ftp_server()
