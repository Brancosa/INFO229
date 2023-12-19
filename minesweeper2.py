import random
from tkinter import font
import time
import tkinter as tk

class TipoCasilla:
    Mina = 'mina'
    Numero = 'numero'
    Vacia = 'vacia'

class Casilla:
    def __init__(self, tipo=TipoCasilla.Vacia, valor=0):
        # Inicializa una casilla con un tipo y valor predeterminados
        self.tipo = tipo
        self.valor = valor
        self.descubierta = False
        self.marcada = False
        self.banderas = False  # Variable para gestionar el estado de la bandera

class Tablero:
    def __init__(self, ancho, alto, minas):
        # Inicializa un tablero con las dimensiones especificadas y genera minas aleatorias
        self.ancho = ancho
        self.alto = alto
        self.minas = minas
        self.casillas = [[Casilla() for _ in range(ancho)] for _ in range(alto)]
        self.generar_minas()

    def generar_minas(self):
        # Genera minas en posiciones aleatorias en el tablero
        posiciones = [(x, y) for x in range(self.ancho) for y in range(self.alto)]
        minas_pos = random.sample(posiciones, self.minas)
        for x, y in minas_pos:
            self.casillas[x][y] = Casilla(tipo=TipoCasilla.Mina)

class Cronometro:
    def __init__(self, root):
        # Inicializa un cronómetro con una etiqueta en la interfaz gráfica
        self.root = root
        self.label = tk.Label(self.root, text="", font=("Arial", 15))
        self.label.grid(row=1, column=ancho)
        self.tiempo_inicio = time.time()
        self.actualizar_cronometro_id = None

    def actualizar_cronometro(self):
        # Actualiza el cronómetro mostrando el tiempo transcurrido
        if juego.juego_en_progreso:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            minutos, segundos = divmod(tiempo_transcurrido, 60)
            horas, minutos = divmod(minutos, 60)
            self.label.config(text="%02d:%02d:%02d" % (horas, minutos, segundos), font=("Arial", 15))
            self.actualizar_cronometro_id = self.root.after(1000, self.actualizar_cronometro)

    def iniciar_cronometro(self):
        # Inicia el cronómetro
        self.actualizar_cronometro()

    def detener_cronometro(self):
        # Detiene el cronómetro
        self.root.after_cancel(self.actualizar_cronometro_id)

class JuegoBuscaminas:
    def __init__(self, ancho, alto, minas):
        # Inicializa el juego de Buscaminas con las dimensiones y minas especificadas
        self.ancho = ancho
        self.alto = alto
        self.minas = minas
        self.root = tk.Tk()
        self.tablero = None
        self.botones = None
        self.texto = None
        self.cronometro = None
        self.juego_en_progreso = False
        self.estado_juego = None
        self.boton_reinicio = None

    def iniciar_juego(self):
        # Inicia el juego creando el tablero, botones y otros elementos de la interfaz gráfica
        # También inicia el cronómetro y establece el juego como en progreso
        self.tablero = Tablero(self.ancho, self.alto, self.minas)
        self.botones = [[tk.Button(self.root, height=3, width=3, fg='black') for y in range(self.ancho)] for x in range(self.alto)]
        for x in range(self.alto):
            for y in range(self.ancho):
                self.botones[x][y].grid(row=x, column=y)
                self.botones[x][y].bind('<Button-1>', lambda e, x=x, y=y: self.click(x, y))
                self.botones[x][y].bind('<Button-3>', lambda e, x=x, y=y: self.marcar_banderas(x, y))

        self.root.grid_columnconfigure(self.ancho, minsize=150)

        self.texto = tk.Label(self.root, text="Buscaminas!", font=("Arial", 15))
        self.texto.grid(row=0, column=self.ancho)

        self.cronometro = Cronometro(self.root)
        self.juego_en_progreso = True

        self.estado_juego = tk.Label(self.root, text=" ")
        self.estado_juego.grid(row=2, column=self.ancho)

        self.boton_reinicio = tk.Button(self.root, text="R", command=self.reiniciar_juego, font=("Arial", 15))
        self.boton_reinicio.grid(row=3, column=self.ancho)

    def reiniciar_juego(self):
        # Reinicia el juego al presionar el botón de reinicio
        self.juego_en_progreso = False
        self.cronometro.detener_cronometro()  # Detiene el cronómetro

        # Elimina el mensaje de estado
        self.estado_juego.config(text=" ")

        # Reinicia el tablero y los botones
        for x in range(self.alto):
            for y in range(self.ancho):
                self.botones[x][y].config(text='', state='normal', bg=self.root.cget('bg'))

        # Reinicia la instancia del tablero
        self.tablero = Tablero(self.ancho, self.alto, self.minas)

        # Reinicia el cronómetro
        self.tiempo_inicio = time.time()
        self.cronometro.iniciar_cronometro()

        # Reinicia el estado del juego
        self.juego_en_progreso = True
        self.run()

    def marcar_banderas(self, x, y):
        # Maneja la marca de banderas en una casilla
        defaultbg = self.root.cget('bg')
        if self.tablero.casillas[x][y].marcada:
            return
        self.tablero.casillas[x][y].banderas = not self.tablero.casillas[x][y].banderas
        if self.tablero.casillas[x][y].banderas:
            self.botones[x][y].config(text='B', bg='tomato', fg='white')
        else:
            self.botones[x][y].config(text='', bg=defaultbg)

    def click(self, x, y):
        # Maneja el evento de clic en una casilla
        if self.tablero.casillas[x][y].tipo == TipoCasilla.Mina:
            self.botones[x][y].config(text='M', state='disabled', bg='firebrick1')
            self.game_over("Derrota")
        else:
            self.revelar_casilla(x, y)

    def revelar_casilla(self, x, y):
        bold_font = font.Font(weight="bold")
        if self.tablero.casillas[x][y].marcada:
            return
        
        self.tablero.casillas[x][y].marcada = True
        if self.tablero.casillas[x][y].tipo == TipoCasilla.Mina:
            return  # No revelar minas marcadas
        
        minas_cercanas = self.contar_minas(x, y)
        
        if minas_cercanas == 0:
            # Si es un espacio en blanco, revelar casillas vecinas
            self.botones[x][y].config(text='', state='disabled', bg='gray73')
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.tablero.alto and 0 <= ny < self.tablero.ancho
                            and not self.tablero.casillas[nx][ny].marcada
                            and not self.tablero.casillas[nx][ny].banderas):  # Verifica si no hay bandera
                        self.revelar_casilla(nx, ny)
        else:
            colores = {1: 'sky blue', 2: 'pale green', 3: 'khaki', 4: 'MediumPurple1', 5: 'salmon1', 6: 'aquamarine2',
                    7: 'plum4', 8: 'gray'}
            color = colores.get(minas_cercanas, 'black')
            self.botones[x][y].config(text=str(minas_cercanas), state='disabled', disabledforeground='black', bg=color)

            casillas_sin_bomba = sum(1 for fila in self.tablero.casillas for casilla in fila
                                    if casilla.tipo != TipoCasilla.Mina and casilla.marcada)
            total_casillas_sin_bomba = (self.tablero.ancho * self.tablero.alto) - self.tablero.minas
            if casillas_sin_bomba == total_casillas_sin_bomba:
                self.game_over("Victoria")


    def contar_minas(self, x, y):
        # Cuenta el número de minas alrededor de una casilla
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.tablero.alto and 0 <= ny < self.tablero.ancho
                        and self.tablero.casillas[nx][ny].tipo == TipoCasilla.Mina):
                    count += 1
        return count

    def game_over(self, estado):
        # Maneja el final del juego (victoria o derrota)
        self.juego_en_progreso = False
        self.cronometro.detener_cronometro()
        for x in range(self.tablero.alto):
            for y in range(self.tablero.ancho):
                self.botones[x][y].config(state='disabled')
                self.tablero.casillas[x][y].marcada = True
                if self.tablero.casillas[x][y].tipo == TipoCasilla.Mina:
                    self.botones[x][y].config(text='M', bg='firebrick1', disabledforeground='white')
        self.estado_juego.config(text=f"{estado}", font=("Arial", 20))

    def run(self):
        # Función principal que inicia el juego
        self.iniciar_juego()
        self.cronometro.iniciar_cronometro()
        self.root.mainloop()

if __name__ == "__main__":
    # Configuración inicial del juego
    alto = 15
    ancho = 15
    porcentaje_minas = 0.2
    minas = int((ancho * alto) * porcentaje_minas)
    juego = JuegoBuscaminas(alto, ancho, minas)
    juego.run()
