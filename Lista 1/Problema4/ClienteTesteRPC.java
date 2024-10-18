import java.io.OutputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.swing.JOptionPane;

public class ClienteTesteRPC {
    public static void main(String[] args) {
        try {
            String sexo = JOptionPane.showInputDialog("Digite seu Sexo (M/F):");
            String altura = JOptionPane.showInputDialog("Digite sua Altura:");

            // Criando o JSON
            String inputJson = "{\"sexo\":\"" + sexo + "\",\"altura\":\"" + altura + "\"}";

            // Enviando requisição para o servidor
            String response = sendPostRequest("http://127.0.0.1:5000/calcular", inputJson);
            JOptionPane.showMessageDialog(null, "Resposta do servidor: " + response);


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static String sendPostRequest(String urlString, String jsonInputString) throws Exception {
        URL url = new URL(urlString);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json; utf-8");
        con.setRequestProperty("Accept", "application/json");
        con.setDoOutput(true);

        try (OutputStream os = con.getOutputStream()) {
            byte[] input = jsonInputString.getBytes("utf-8");
            os.write(input, 0, input.length);
        }

        try (BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "utf-8"))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            return response.toString();
        }
    }
}
