import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class MaioridadeServiceImpl extends UnicastRemoteObject implements MaioridadeService {

    protected MaioridadeServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public String verificarMaioridade(String nome, String sexo, int idade) throws RemoteException {
        sexo = sexo.toLowerCase();
        if (sexo.equals("masculino") && idade >= 18) {
            return nome + " já atingiu a maioridade.";
        } else if (sexo.equals("feminino") && idade >= 21) {
            return nome + " já atingiu a maioridade.";
        } else {
            return nome + " ainda não atingiu a maioridade.";
        }
    }

    public static void main(String[] args) {
        try {
            java.rmi.registry.LocateRegistry.createRegistry(1099);
            MaioridadeServiceImpl service = new MaioridadeServiceImpl();
            java.rmi.Naming.rebind("MaioridadeService", service);
            System.out.println("Servidor RMI pronto.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
