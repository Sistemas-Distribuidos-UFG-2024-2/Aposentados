import java.rmi.Remote;
import java.rmi.RemoteException;

public interface ReajusteService extends Remote {
    String calcularReajuste(String nome, String cargo, double salario) throws RemoteException;
}
