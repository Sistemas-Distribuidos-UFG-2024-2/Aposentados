import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class ReajusteServiceImpl extends UnicastRemoteObject implements ReajusteService {

    protected ReajusteServiceImpl() throws RemoteException {
        super();
    }

    @Override
    public String calcularReajuste(String nome, String cargo, double salario) throws RemoteException {
        cargo = cargo.toLowerCase();
        double salarioReajustado;

        if (cargo.equals("operador")) {
            salarioReajustado = salario * 1.20;
        } else if (cargo.equals("programador")) {
            salarioReajustado = salario * 1.18;
        } else {
            return "Cargo inválido.";
        }

        return "Nome: " + nome + ", Salário reajustado: R$" + salarioReajustado;
    }

    public static void main(String[] args) {
        try {
            java.rmi.registry.LocateRegistry.createRegistry(1099);
            ReajusteServiceImpl service = new ReajusteServiceImpl();
            java.rmi.Naming.rebind("ReajusteService", service);
            System.out.println("Servidor RMI pronto.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
