import org.apache.xmlrpc.XmlRpcClient;
import org.apache.xmlrpc.XmlRpcException;

import javax.swing.JOptionPane;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Vector;

public class ClienteRPC {
    public static void main(String[] args) {
        try {
            XmlRpcClient client = new XmlRpcClient("http://127.0.0.1:5000/");
            
            // Coleta as notas do usuário
            String N1 = JOptionPane.showInputDialog("Digite sua Nota 1:");
            String N2 = JOptionPane.showInputDialog("Digite sua Nota 2:");
            
            Vector<Object> params = new Vector<>();
            params.add(Double.parseDouble(N1));
            params.add(Double.parseDouble(N2));
            
            String response = (String) client.execute("calcular_resultado", params);
            JOptionPane.showMessageDialog(null, "Resposta do servidor: " + response);
            
            if (response.equals("fazer N3")) {
                String N3 = JOptionPane.showInputDialog("Digite a nota N3:");
                
                params.add(Double.parseDouble(N3));
                response = (String) client.execute("calcular_resultado", params);
                
                JOptionPane.showMessageDialog(null, "Resposta final: " + response);
            }
        } catch (MalformedURLException | XmlRpcException e) {
            e.printStackTrace();
        }
    }
}
