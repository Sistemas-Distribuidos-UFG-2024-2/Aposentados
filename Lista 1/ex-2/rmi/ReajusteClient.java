import java.rmi.Naming;

public class ReajusteClient {

    public static void main(String[] args) {
        try {
            // Localizar o serviço remoto pelo nome
            ReajusteService service = (ReajusteService) Naming.lookup("rmi://localhost/ReajusteService");

            // Coletar dados do usuário
            String nome = "Maria";
            String cargo = "operador";
            double salario = 3000.00;

            // Chamar o método remoto e obter o resultado
            String resultado = service.calcularReajuste(nome, cargo, salario);
            System.out.println("Resultado: " + resultado);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
