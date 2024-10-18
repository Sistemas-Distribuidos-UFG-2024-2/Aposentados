import java.rmi.Naming;

public class MaioridadeClient {

    public static void main(String[] args) {
        try {
            // Localizar o serviço remoto pelo nome
            MaioridadeService service = (MaioridadeService) Naming.lookup("rmi://localhost/MaioridadeService");

            // Coletar dados do usuário
            String nome = "João";
            String sexo = "masculino";
            int idade = 20;

            // Chamar o método remoto e obter o resultado
            String resultado = service.verificarMaioridade(nome, sexo, idade);
            System.out.println("Resultado: " + resultado);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
