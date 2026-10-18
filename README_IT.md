# OrcaSlicer AutoSlice

[English](README.md) · Italiano

Prototipo generico per stampanti con **un solo ugello**, indipendente da INDX e KlipperScreen. Scegli l'uso del pezzo; il pianificatore propone pareti, top/bottom, densita e altezze con riempimento combinato. Valuta le alternative con una stima rapida e fa slicerare a Orca solo pochi finalisti.

**Stato attuale: strumento Python da riga di comando funzionante; l'interfaccia integrata in Orca e l'installer Windows sono ancora da sviluppare.**

Servono Python 3.10+, un file STL e profili JSON completi di macchina, processo e filamento. Il profilo macchina deve specificare ugello e limiti layer; il filamento deve avere una portata volumetrica positiva. Nessun limite meccanico della SV08 Max viene imposto ad altre stampanti.

```sh
python autoslice.py --machine macchina.json --process processo.json --filament filamento.json --model pezzo.stl --output risultati --purpose everyday
```

Le priorita sono `everyday` (uso quotidiano), `finish` (finitura), `strong` (piu materiale/spessori) e `draft` (bozza veloce). Aggiungi `--orca` con il percorso dell'eseguibile per ottenere lo slicing reale dei finalisti. Senza `--orca` genera soltanto le proposte. Il budget predefinito e tre finalisti per modalita; `--budget` accetta da 1 a 5.

`comparison.json` riporta tempi nativi, layer totali, G-code migliori ed eventuali errori. I candidati identici condividono il calcolo. Controlla il G-code in Orca prima di stamparlo. Il programma non si collega alla stampante e non invia stampe.

La stima preliminare usa ingombro, portata e lunghezze approssimate: non conosce ogni dettaglio geometrico e puo scartare una variante migliore. Il riempimento combinato vale solo dove la geometria lo consente. La priorita strutturale non certifica la resistenza del pezzo. Vedi [README inglese](README.md) per limiti, progetti correlati e sviluppo.

Native validation: a 10 mm single-nozzle cube produced all three modes from 15 logical candidates and 7 distinct native jobs (duplicates reused). Detail 4m42s/55 layers, balanced 3m39s/42 layers, fast 2m54s/32 layers. Test-specific estimates only. STL coordinates must already fit the selected bed; the prototype deliberately preserves positioning and does not auto-arrange.
