import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Servidor {
    public static void main(String[] args) {
        try {
            CartaBaralhoImpl carta = new CartaBaralhoImpl();
            // Inicia o registro RMI na porta 1099
            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("CartaBaralho", carta);  // Registra o objeto
            System.out.println("Servidor RMI está pronto.");
        } catch (Exception e) {
            System.err.println("Exceção no servidor: " + e.toString());
            e.printStackTrace();
        }
    }
}
