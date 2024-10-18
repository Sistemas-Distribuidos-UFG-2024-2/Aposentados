import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Cliente {
    public static void main(String[] args) {
        try {
            // Conecta ao registro RMI no servidor
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            // Busca o objeto remoto
            CartaBaralho stub = (CartaBaralho) registry.lookup("CartaBaralho");

            // Exemplo: valor 1 (Ás) e naipe 1 (Ouros)
            String resposta = stub.nomeCarta(1, 1);
            System.out.println("Nome da carta: " + resposta);
            
        } catch (Exception e) {
            System.err.println("Exceção no cliente: " + e.toString());
            e.printStackTrace();
        }
    }
}
