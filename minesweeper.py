import tkinter as tk
import random
from tkinter import font
import time


class Casilla:
    def __init__(self):
        self.valor = 0
        self.marcada = False
        self.banderas = False

class Tablero:
    def __init__(self, ancho, alto, minas):
        self.ancho = ancho
        self.alto = alto
        self.minas = minas
        self.casillas = [[Casilla() for _ in range(ancho)] for _ in range(alto)]
        self.generar_minas()

    def generar_minas(self):
        posiciones = [(x, y) for x in range(self.ancho) for y in range(self.alto)]
        minas_pos = random.sample(posiciones, self.minas)
        for x, y in minas_pos:
            self.casillas[x][y].valor = 'M'


class JuegoBuscaminas:
    def __init__(self, ancho, alto, minas):
        self.root = tk.Tk()
        self.tablero = Tablero(ancho, alto, minas)
        self.botones = [[tk.Button(self.root, height=3, width=3, fg='black') 
                         for y in range(ancho)] for x in range(alto)]
        for x in range(alto):
            for y in range(ancho):
                self.botones[x][y].grid(row=x, column=y)
                self.botones[x][y].bind('<Button-1>', lambda e, x=x, y=y: self.click(x, y))
                self.botones[x][y].bind('<Button-3>', lambda e, x=x, y=y: self.marcar_banderas(x, y))

        self.root.grid_columnconfigure(ancho, minsize=150)

        self.texto = tk.Label(self.root, text="Buscaminas!", font=("Arial", 15))
        self.texto.grid(row=0, column=ancho)

        self.cronometro = tk.Label(self.root, text="")
        self.cronometro.grid(row=1, column=ancho)
        self.juego_en_progreso = True

        self.estado_juego = tk.Label(self.root, text=" ")
        self.estado_juego.grid(row=2, column=ancho)

        self.tiempo_inicio = time.time()
        self.actualizar_cronometro_id = self.root.after(1000, self.actualizar_cronometro)

        self.boton_reinicio = tk.Button(self.root, text="R", command=self.reiniciar_juego, font=("Arial", 15))
        self.boton_reinicio.grid(row=3, column=ancho)

    def actualizar_cronometro(self):
        if self.juego_en_progreso:
            tiempo_transcurrido = time.time() - self.tiempo_inicio
            minutos, segundos = divmod(tiempo_transcurrido, 60)
            horas, minutos = divmod(minutos, 60)
            self.cronometro.config(text="%02d:%02d:%02d" % (horas, minutos, segundos), font=("Arial", 15))
            self.actualizar_cronometro_id = self.root.after(1000, self.actualizar_cronometro)

    def game_over(self, estado):
        self.juego_en_progreso = False
        self.root.after_cancel(self.actualizar_cronometro_id)
        for x in range(self.tablero.alto):
            for y in range(self.tablero.ancho):
                self.botones[x][y].config(state='disabled')
                self.tablero.casillas[x][y].marcada = True
                if self.tablero.casillas[x][y].valor == 'M':
                    self.botones[x][y].config(text='M', bg='firebrick1', disabledforeground='white')
        self.estado_juego.config(text=f"{estado}", font=("Arial", 20))

    def reiniciar_juego(self):
        # Reinicia el juego al presionar el botón de reinicio
        self.juego_en_progreso = False
        self.root.after_cancel(self.actualizar_cronometro_id)  # Cancela la actualización del cronómetro
        self.root.destroy()
        juego = JuegoBuscaminas(alto, ancho, minas)
        juego.run()

    def marcar_banderas(self, x, y):
        defaultbg = self.root.cget('bg')
        if self.tablero.casillas[x][y].marcada:
            return
        self.tablero.casillas[x][y].banderas = not self.tablero.casillas[x][y].banderas
        if self.tablero.casillas[x][y].banderas:
            self.botones[x][y].config(text='B', bg='tomato', fg='white')
        else:
            self.botones[x][y].config(text='', bg=defaultbg)


    def click(self, x, y):
        if self.tablero.casillas[x][y].valor == 'M':
            self.botones[x][y].config(text='M', state='disabled', bg='firebrick1')
            self.game_over("Derrota")
        else:
            self.revelar_casilla(x, y)

    def revelar_casilla(self, x, y):
        bold_font = font.Font(weight="bold")
        if self.tablero.casillas[x][y].marcada:
            return
        self.tablero.casillas[x][y].marcada = True
        minas_cercanas = self.contar_minas(x, y)
        if minas_cercanas == 0:
            self.botones[x][y].config(text='', state='disabled', bg='gray73')
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.tablero.alto and 0 <= ny < self.tablero.ancho
                        and not self.tablero.casillas[nx][ny].marcada):
                        self.revelar_casilla(nx, ny)
        else:
            colores = {1: 'sky blue', 2: 'pale green', 3: 'khaki', 4: 'MediumPurple1', 5: 'salmon1', 6: 'aquamarine2', 7: 'plum4', 8: 'gray'}
            color = colores.get(minas_cercanas, 'black')
            self.botones[x][y].config(text=str(minas_cercanas), state='disabled', disabledforeground='black', bg=color)

            casillas_sin_bomba = sum(1 for fila in self.tablero.casillas for casilla in fila if casilla.valor != 'M' and casilla.marcada)
            total_casillas_sin_bomba = (self.tablero.ancho * self.tablero.alto) - self.tablero.minas
            if casillas_sin_bomba == total_casillas_sin_bomba:
                self.game_over("Victoria")


    def contar_minas(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.tablero.alto and 0 <= ny < self.tablero.ancho
                    and self.tablero.casillas[nx][ny].valor == 'M'):
                    count += 1
        return count

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    alto = 15
    ancho = 15
    porcentaje_minas = 0.2
    minas = int((ancho*alto)* porcentaje_minas)
    juego = JuegoBuscaminas(alto, ancho, minas)
    juego.run()
