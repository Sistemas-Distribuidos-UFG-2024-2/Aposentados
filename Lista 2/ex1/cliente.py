from ftplib import FTP

def run_ftp_client():
    # Conecta ao servidor FTP
    ftp = FTP()
    ftp.connect("www.inf.ufg.br")  
    ftp.login("user", "password")   # Substituir pelo usuário e senha
    
    # Lista os arquivos no diretório remoto
    print("Arquivos no servidor FTP:")
    ftp.retrlines("LIST")
    
    # Download de um arquivo
    with open("arquivo_baixado.txt", "wb") as f:
        ftp.retrbinary("RETR arquivo_no_servidor.txt", f.write)  # Substituir com o nome do arquivo real no servidor
    
    # Upload de um arquivo
    with open("arquivo_para_subir.txt", "rb") as f:
        ftp.storbinary("STOR arquivo_no_servidor.txt", f)  # Substituir pelo nome do arquivo no servidor
    
    # Desconecta do servidor
    ftp.quit()

if __name__ == "__main__":
    run_ftp_client()
