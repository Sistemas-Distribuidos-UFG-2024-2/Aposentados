/*Implementação do Servidor*/

import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;

public class CartaBaralhoImpl extends UnicastRemoteObject implements CartaBaralho {
    
    private static final String[] VALORES = {
        "", "Ás", "Dois", "Três", "Quatro", "Cinco", "Seis", "Sete", 
        "Oito", "Nove", "Dez", "Valete", "Dama", "Rei"
    };
    
    private static final String[] NAIPES = {
        "", "Ouros", "Paus", "Copas", "Espadas"
    };
    
    protected CartaBaralhoImpl() throws RemoteException {
        super();
    }

    @Override
    public String nomeCarta(int valor, int naipe) throws RemoteException {
        if (valor < 1 || valor > 13 || naipe < 1 || naipe > 4) {
            return "Carta inválida";
        }
        return VALORES[valor] + " de " + NAIPES[naipe];
    }
}
