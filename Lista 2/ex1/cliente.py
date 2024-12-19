from ftplib import FTP

def run_ftp_client():
    
    ftp = FTP()
    ftp.connect("www.inf.ufg.br")  
    ftp.login("user", "password")   
    
    print("Arquivos no servidor FTP:")
    ftp.retrlines("LIST")
    
    with open("arquivo_baixado.txt", "wb") as f:
        ftp.retrbinary("RETR arquivo_no_servidor.txt", f.write)
    
    with open("arquivo_para_subir.txt", "rb") as f:
        ftp.storbinary("STOR arquivo_no_servidor.txt", f) 
    
    ftp.quit()

if __name__ == "__main__":
    run_ftp_client()
