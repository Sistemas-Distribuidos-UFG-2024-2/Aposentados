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

            
                String N1 = JOptionPane.showInputDialog("Digite sua Nota 1:");
                String N2 = JOptionPane.showInputDialog("Digite sua Nota 2:");
            
                saida.println(N1 + ";" + N2);

                String resposta = entrada.readLine();
                JOptionPane.showMessageDialog(null, "Resposta do servidor: " + resposta);

                if (resposta.equals("fazer N3")) {

                    String N3 = JOptionPane.showInputDialog("Digite a nota N3:");
                    saida.println(N1 + ";" + N2 + ";" + N3);
    
                    // Recebe o resultado final
                    resposta = entrada.readLine();
                    JOptionPane.showMessageDialog(null, resposta);
                }

        } catch (UnknownHostException e) {
            System.err.println("Host desconhecido: " + servidor);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Não foi possível se conectar ao servidor na porta " + porta);
            System.exit(1);
        }
    }
}
