# Libreria che serve per cominicare con la porta seriale a cui è collegato arduino
import serial
import json
import time
import os
os.chdir(os.path.dirname(__file__))

# Inizializza la porta corretta e la velocità di comunicazione
ser = serial.Serial('COM3', 9600)

file_name = "dati_stufa.json"
# Lista vuota che conterrà i dati
letture = []
contatore = 1
# Soglia di sicurezza del gas
SOGLIA_GAS = 400
# Loop infinito per leggere continuamente i dati dalla porta seriale, con gestione degli erroti e controllo dei dati ricevuti
try:
    while True:
        # Controlla che ci siano dati disponibili
        if ser.in_waiting > 0:
            # Legge la riga dalla porta seriale, decodifica e rimuove spazi bianchi
            linea = ser.readline().decode('utf-8').strip()
            print("Ricevuto:", linea)
            # Controlla che la riga contenga dati validi
            if "Temp:" in linea and "Gas:" in linea:
                try:
                    # Sistema i dati ricevuti
                    parti = linea.split("|")
                    # Prende il dato temperatura e lo converte in float
                    temp = float(parti[0].split(":")[1].strip())
                    # Prende il dato gas e lo converte in int
                    gas = int(parti[1].split(":")[1].strip())
                    auto = 1  # valore di default
                    # Valori iniziali
                    stato_stufa = "SPENTA"
                    messaggio = "Sistema normale"
                    # Controllo GAS (priorità massima)
                    if gas > SOGLIA_GAS:
                        stato_stufa = "BLOCCATA_GAS"
                        messaggio = "Valore gas troppo elevato - Stufa spenta per sicurezza"
                    # Modalità automatica
                    elif auto == 1:
                        if temp < 24:
                            stato_stufa = "ACCESA"
                            messaggio = "Temperatura bassa - Stufa accesa"
                        elif temp > 27:
                            stato_stufa = "SPENTA"
                            messaggio = "Temperatura alta - Stufa spenta"
                        else:
                            stato_stufa = "SPENTA"
                            messaggio = "Temperatura ideale - Stufa spenta"
                    # Creazione dizionario
                    dato = {
                        "Lettura_numero": contatore,
                        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Temperatura": temp,
                        "Gas": gas,
                        "Stato_stufa": stato_stufa,
                        "Messaggio": messaggio
                    }
                    # Aggiunge il dato ricavato
                    letture.append(dato)
                    # Scrittura su file JSON
                    with open(file_name, "w") as f:
                        json.dump(letture, f, indent=4)
                    contatore += 1
                except Exception as e: # Gestione degli errori di parsing dei dati
                    print("Errore riscontrato:", e)
        time.sleep(1)
# Interruzione da parte dell'utente, chiusura della porta seriale tramite ctrl+c
except KeyboardInterrupt:
    print("Interrotto dall'utente")
    ser.close()