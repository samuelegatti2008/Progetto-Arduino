# Sistema di Monitoraggio e Controllo Stufa via Serial
 
Questo progetto consiste in uno script Python sviluppato per interfacciarsi e comunicare in tempo reale con una scheda Arduino (o microcontrollore simile) tramite connessione seriale. Il sistema acquisisce i dati ambientali di temperatura e concentrazione di gas, applica una logica di controllo automatica per la sicurezza domestica e il comfort termico, e archivia lo storico delle letture in un file strutturato JSON.
 
---
 
## 🚀 Funzionalità
 
* **Monitoraggio in Tempo Reale:** Ascolto continuo della porta seriale per intercettare i dati inviati dai sensori.
* **Sicurezza Prioritaria:** Controllo istantaneo della concentrazione di gas con blocco di sicurezza immediato in caso di superamento della soglia critica.
* **Termostato Automatico:** Gestione intelligente dello stato della stufa (Accesa/Spenta) basata su intervalli di temperatura ideali.
* **Persistenza dei Dati:** Esportazione e aggiornamento continuo delle letture all'interno di un file JSON (`dati_stufa.json`) completo di contatore e timestamp.
* **Robustezza del Codice:** Gestione interna delle eccezioni per prevenire crash dovuti a stringhe seriali corrotte o errori di parsing.
* **Chiusura Sicura:** Rilascio controllato della porta seriale in caso di interruzione manuale da parte dell'utente.
 
---
 
## 📋 Requisiti e Prerequisiti
 
### Requisiti Software
Assicurati di avere installato **Python 3.x** sul tuo sistema. Il codice richiede inoltre la libreria esterna `pyserial`. Puoi installarla eseguendo dal terminale:
 
```bash
pip install pyserial
```
 
### Configurazione Hardware e Comunicazione
* **Porta Seriale Predefinita:** `COM3` (Velocità: `9600` baud). 
> *Nota: Se la tua scheda Arduino è collegata a una porta differente (es. `COM4` su Windows o `/dev/ttyUSB0` su Linux), ricordati di modificare la stringa di inizializzazione `serial.Serial('COM3', 9600)` all'interno del codice.*
* **Formato dei Dati:** Per consentire il corretto funzionamento dello script, l'Arduino deve stampare sulla porta seriale stringhe formattate esattamente come nel seguente esempio:
  `Temp: 23.5 | Gas: 180`
 
---
 
## 🛠️ Logica di Funzionamento
 
Ad ogni ciclo di lettura (cadenzato ogni secondo), il sistema analizza i dati ricevuti applicando una logica decisionale gerarchica:
 
1. **Controllo Gas (Priorità Massima):** Se il valore del gas supera la **SOGLIA_GAS** impostata a **400**, il sistema interrompe immediatamente il funzionamento termico impostando lo stato su `BLOCCATA_GAS`.
2. **Modalità Automatica (Gestione Temperatura):** Se i livelli di gas sono nella norma, subentra il controllo della temperatura:
   * **Sotto i 24°C:** La temperatura è considerata bassa → Stato stufa: `ACCESA`.
   * **Sopra i 27°C:** La temperatura è considerata alta → Stato stufa: `SPENTA`.
   * **Tra 24°C e 27°C:** Viene rilevata la temperatura ideale → Stato stufa: `SPENTA`.
 
---
 
## 📊 Struttura dei Dati Salvati
 
I dati elaborati vengono appesi a una lista e sovrascritti in modo leggibile (con indentazione a 4 spazi) nel file `dati_stufa.json`. Ogni record segue questa struttura:
 
```json
[
    {
        "Lettura_numero": 1,
        "Timestamp": "2026-05-20 12:30:15",
        "Temperatura": 22.5,
        "Gas": 150,
        "Stato_stufa": "ACCESA",
        "Messaggio": "Temperatura bassa - Stufa accesa"
    }
]
```
 
---
 
## 💻 Come Avviare il Progetto
 
1. Collega la scheda Arduino al computer tramite USB.
2. Verifica che il monitor seriale dell'IDE di Arduino sia chiuso (per evitare conflitti di occupazione della porta).
3. Posiziona il file `Codice 1.py` nella cartella in cui desideri generare il database JSON.
4. Apri il terminale e lancia lo script:
   ```bash
   python "Codice 1.py"
   ```
5. Per arrestare il monitoraggio e chiudere correttamente la connessione seriale senza corrompere i file, premi la combinazione di tasti **Ctrl + C** all'interno del terminale.
