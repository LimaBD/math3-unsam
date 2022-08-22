public class CarreraCaballos extends Thread {
    public static void main(String args[]) {
        Caballo jugadorUno = new Caballo("#1", 6);
        Caballo jugadorDos = new Caballo("Rapido y Furioso", 6);
        Caballo jugadorTres = new Caballo("Rocket", 6);

        jugadorUno.start();
        jugadorDos.start();
        jugadorTres.start();

        try {
            jugadorUno.join();
            jugadorDos.join();
            jugadorTres.join();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

class Caballo extends Thread {
    static String nombreDelCaballo;
    static int velocidadPorCiclo;

    public Caballo(String nombre, int velocidad) {
        nombreDelCaballo = nombre;
        velocidadPorCiclo = velocidad;
    }

    public void run() {
        int distanciaRecorrida = 0;
        int distanciaTotal = 70000;

        while (distanciaRecorrida < distanciaTotal) {
            distanciaRecorrida = distanciaRecorrida + velocidadPorCiclo;
        }

        System.out.println("Caballo #" + nombreDelCaballo + " ganador!");
    }
}
