import java.io.*;
import java.net.*;
import javax.swing.JOptionPane;

public class Cliente {
    public static void main(String[] args) {
        String servidor = "127.0.0.1";  
        int porta = 5000;  

        try (
            Socket socket = new Socket(servidor, porta);
            
            PrintWriter saida = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        ) {
            System.out.println("Conectado ao servidor.");

            
                String sexo = JOptionPane.showInputDialog("Digite seu Sexo (M/F):");
                String altura = JOptionPane.showInputDialog("Digite sua Altura:");
            
                saida.println(sexo + ";" + altura);

                String resposta = entrada.readLine();
                JOptionPane.showMessageDialog(null, "Resposta do servidor: " + resposta);

        } catch (UnknownHostException e) {
            System.err.println("Host desconhecido: " + servidor);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Não foi possível se conectar ao servidor na porta " + porta);
            System.exit(1);
        }
    }
}
