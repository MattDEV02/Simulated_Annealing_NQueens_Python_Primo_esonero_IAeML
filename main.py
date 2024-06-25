import random
import numpy as np
import math


def tweak(stato):
    
    stato_copy = np.copy(stato)
    
    # scegli random due colonne distinte
    x = random.randint(0, DIMENSIONE - 1)
    y = random.randint(0, DIMENSIONE - 1)
    while x == y:
        y = random.randint(0, DIMENSIONE - 1)
        
    # scambia le due colonne
    stato_copy[x], stato_copy[y] = stato_copy[y], stato_copy[x] 
    
    return stato_copy

def inizializza(stato):
    # shake 
    for _ in range(0, DIMENSIONE - 1):
        stato = tweak(stato)
    return stato


def energia(stato):
    # definizione della scacchiera N x N
    board  = [[0] * DIMENSIONE for _ in range(DIMENSIONE)] 
    
    # inserimento delle regine ('Q') nelle loro posizioni sulla scacchiera
    for i in range(0, DIMENSIONE):
        board[stato[i]][i] ='Q'
        
    # spostamenti possibili sulla scacchiera
    dx = [-1, 1, -1, 1]
    dy = [-1, 1, 1, -1]
    
    # inizializzazione numero di attacchi (diretti o indiretti)
    conflitti = 0

    for i in range(0, DIMENSIONE):       
        x = stato[i]
        y = i
        
        # verifica attacchi sulle diagonali       
        for j in range(0, 4):
            tempx = x
            tempy = y
            while True:
                tempx += dx[j]           # spostamento sull'asse x
                tempy += dy[j]           # spostamento sull'asse y
                if ((tempx < 0) or 
                    (tempx >= DIMENSIONE) or
                    (tempy < 0) or 
                    (tempy >= DIMENSIONE)):
                    break                       # si esce se lo spostamento va fuori la scacchiera
                if (board[tempx][tempy] == 'Q'):
                    conflitti += 1   # aggiornamento numero di attacchi
    return conflitti

def stampa(stato):
    
    board = [[0] * DIMENSIONE for _ in range(DIMENSIONE)] 

    for i in range(DIMENSIONE):
        board[stato[i]][i] = 'Q'
    print("\nSCACCHIERA:", '\n')
    for i in range(0, DIMENSIONE):
        for j in range(0, DIMENSIONE):
            if(board[i][j] == 'Q'):
                print("Q   ", end = ''),
            else:
                print(".   ", end = ''),
        print("\n")
    print("\n\n")

def simulated_annealing():
    
    # impostazione dello stato iniziale
    current = inizializza(range(0, DIMENSIONE))
    current_energy = energia(current)
    stampa(current)

    # inizializzazione best
    best = current
    best_energy = current_energy

    temperature = TEMPERATURA_INIZIALE

    while (temperature > TEMPERATURA_FINALE and best_energy != 0):
        print("TEMPERATURA: ", end = ''),    
        print(temperature)
        for _ in range(STEPS_PER_CHANGE):
            useNew = False
            next = tweak(current)                # scelta random dello stato successore nel neighbourhood
            next_energy = energia(next)    # valutazione dell'energia dello stato successore
    
            if (next_energy < current_energy):   # se il successore è migliore lo accettiamo
                useNew = True
            else:
                delta = next_energy - current_energy
                metropolis = math.exp(-delta / temperature)  # calcolo probabilità di accettazione
                if (random.random() < metropolis):                # se il numero random è minore della probabilità ...
                    useNew = True                      # ... accettiamo il nuovo stato 
                    
            # se abbiamo deciso di accettare il nuovo stato:   
            if (useNew):
                # impostalo come stato ed energia correnti
                current = next
                current_energy = next_energy
            
                # se è anche il migliore segna il record
                if (current_energy < best_energy):
                    best = current
                    best_energy = current_energy

        print("best_energy = ", end = ''),
        print(best_energy)  
        
        # diminuisci la temperatura, senza mai arrivare a zero
        temperature = temperature * ALFA
        
    return best

# Impostazione parametri

TEMPERATURA_INIZIALE = 30
TEMPERATURA_FINALE = 0.2
ALFA = 0.99 # r * T
STEPS_PER_CHANGE = 100 # Kt

DIMENSIONE = 8   # dimensione dei lati della scacchiera N x N (dove N è la DIMENSIONE)

soluzione = simulated_annealing()

stampa(soluzione)