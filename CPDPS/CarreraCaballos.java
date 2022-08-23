import java.util.*;
import java.lang.Thread;

public class CarreraCaballos extends Thread {

    public static void main(String args[]) {

        int cantidadCaballos = 6;
        List<Caballo> caballos = new ArrayList<Caballo>();
        boolean hayUnGanador = false;

        // Inicializamos los caballos
        for (int i=0; i<cantidadCaballos; i++) {
            // Tiene un numero exageradamente grande para
            // que haya una diferencia importante entre threads
            caballos.add(i, new Caballo("Caballo N" + i, 1, 9223372036854775807L, hayUnGanador));
            caballos.get(i).start();
        }

        // Seguimiento de posiciones
        while (!hayUnGanador) {
            // Limpiamos la consola
            System.out.print("\033\143"); // Esto es solo para OS basados en Linux

            // Orden de posiciones
            caballos.sort((o1, o2) -> Long.toString(o1.distanciaRecorrida).compareTo(Long.toString(o2.distanciaRecorrida)));

            // Imprimimos en consola
            for (int i=0; i<cantidadCaballos; i++) {
                System.out.print("#" + i + "\t" + caballos.get(i).nombreDelCaballo + " (recorrido " + caballos.get(i).distanciaRecorrida + " km)\n");
            }

            // Hacemos que quede imprimido el
            // resultado un tiempo antes que
            // se limpie la consola
            try {
                Thread.sleep(100);
            } catch (Exception e) {
                System.out.println(e);
            }
        }

        // Finaliza threads
        try {
            for (int i=0; i<cantidadCaballos; i++) {
                caballos.get(i).join();
            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

class Caballo extends Thread {

    String nombreDelCaballo;
    long avanzePorCiclo;
    long distanciaTotal;
    boolean hayUnGanador;

    long distanciaRecorrida;

    public Caballo(String nombre, long velocidad, long distancia, boolean ganador) {
        nombreDelCaballo = nombre;
        avanzePorCiclo = velocidad;
        distanciaTotal = distancia;
        hayUnGanador = ganador;
        distanciaRecorrida = 0;
    }

    public void run() {
        while ((this.distanciaRecorrida < this.distanciaTotal) && !hayUnGanador) {
            this.distanciaRecorrida = this.distanciaRecorrida + this.avanzePorCiclo;
        }
        hayUnGanador = true;
    }
}
