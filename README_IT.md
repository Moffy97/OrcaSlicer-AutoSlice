# OrcaSlicer AutoSlice

[English](README.md) · [Italiano](README_IT.md)

**Versione 0.2.0 preview: Auto Slice integrato nell'interfaccia di Orca, con installer Windows x64.** Stampanti FFF normali, un ugello e un filamento; nessuna dipendenza da INDX o KlipperScreen.

## Utilizzo

Scarica l'EXE dagli [Assets della release](https://github.com/Moffy97/OrcaSlicer-AutoSlice/releases). Si installa separatamente in `%LOCALAPPDATA%\Programs\OrcaSlicer-AutoSlice`. Al primo avvio scegli la tua stampante nella procedura guidata oppure importa i tuoi profili. Non viene selezionato un profilo universale inventato. Le altre versioni e i loro dati restano separati; non viene effettuata un'importazione automatica. L'aggiornamento e la disinstallazione conservano la cartella `dati`.

1. Seleziona un profilo a ugello singolo, un filamento e importa il modello. Controlla min/max layer e portata volumetrica del filo. Rimuovi eventuali impostazioni locali di struttura/layer e il profilo di altezza variabile.
2. Premi **Auto Slice**, accanto a **Elabora piatto**. Scegli **Uso quotidiano**, **Finitura e dettagli**, **Pezzo sollecitato** o **Minor tempo possibile**.
3. Il confronto parte automaticamente. Le schede **Dettaglio / Equilibrato / Veloce** mostrano tempo nativo, grammi, layer totali, altezza pareti/superfici e riempimento ogni N strati al massimo.
4. Premi una scheda e conferma: si apre il G-code memorizzato nell'anteprima nativa, senza rifare lo slicing. L'operazione non invia una stampa.
5. **Annulla e ripristina** riporta al processo iniziale, comprese modifiche non salvate. Durante un calcolo attende il finalista in corso. Per le impostazioni manuali continua a usare Elabora piatto.

## Logica

Lo scopo sceglie pareti, Gyroid, densità, spessore e numero di strati pieni. Il layer cambia entro i limiti del nozzle del profilo, mentre il riempimento può combinare più strati anche con lo stesso ugello. La dicitura «ogni N strati al massimo» è un limite: superfici, ponti e geometrie particolari possono richiedere riempimento a ogni strato. Il primo layer resta quello configurato, entro i limiti della macchina.

Prima si confrontano stime geometriche economiche, poi si eseguono al massimo **3 finalisti per modalità**. Le configurazioni identiche riusano lo stesso risultato anche tra modalità. Selezionare e confermare non avvia un nuovo calcolo. Cambiare scopo avvia un nuovo confronto. Durante il confronto il progetto resta bloccato per garantire che i risultati corrispondano agli input. Le tre modalità possono avere lo stesso vincitore.

Restano temperature, accelerazioni, limiti macchina, calibrazioni, portata, G-code personalizzato e larghezze linea del profilo. L'automatismo sceglie il layer; lo slicing ordinario conserva il vincolo manuale. Non assume la meccanica Z della SV08 Max. Non esegue flash, sincronizzazione o comandi alla stampante.

È una preview non ufficiale e non firmata. Il confronto non prova la resistenza e non esplora ogni soluzione possibile. Controlla sempre l'anteprima e valida il pezzo reale. Attualmente servono un solo ugello fisico e un solo filamento: altre configurazioni e override locali sono spiegati e rifiutati, anziché dare stime ingannevoli.

## Sorgenti

Licenza AGPL-3.0. La patch completa e UPSTREAM.json permettono di ricostruire il sorgente corrispondente: esegui `python prepare_source.py` e segui le istruzioni di compilazione ufficiali Orca. Il motore è condiviso con il fork INDX, ma i controlli INDX restano nascosti sui profili normali. Per questo alcuni metadati interni riportano ancora 2.5.0-indx; VERSION.json identifica questa distribuzione. La guida inglese contiene dettagli CLI, limiti, progetto correlati e ricompilazione. WINDOWS_INSTALLER.md documenta installazione e dati.
