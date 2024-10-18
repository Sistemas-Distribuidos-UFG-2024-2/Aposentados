import java.rmi.Remote;
import java.rmi.RemoteException;

public interface CartaBaralho extends Remote {
    String nomeCarta(int valor, int naipe) throws RemoteException;
}
