fuse-netstorage
===============

FUSE-Treiber für NetStorage

Hinweise
--------

- Verzeichnis `mount` anlegen
- Debugging-Server in zweiter Shell starten (debug-server.py)
- Aufruf: `fusermount -u mount/ 2>/dev/null;python main.py mount/` (o.ä.)

Debugging
---------

- Kommunikation erfolgt über eine Pipe (mkfifo)
- Der Debugging-Server muss gestartet sein, andernfalls wird das Programm nicht laufen.
  - Der Server lauscht auf der Pipe nach eingehenden, durch Nullterminator (`\0`) getrennte Nachrichten.
  - Nachrichten werden mit Zeitstempel versehen ausgegeben.
  - Die Nachricht `###clear###` sorgt dafür, dass das Ausgabe-Terminal geleert wird
- Das Modul `debug.py` erledigt die folgenden Aufgaben:
  - `stdout` und `stderr` werden in die Pipe umgeleitet
  - Fehler werden über `sys.excepthook` abgefangen, formatiert und in die Pipe geschrieben
  - `debug.debug([...])` gibt den Inhalt aller Parameter über die Pipe weiter.
  - `debug.debug_exception()` formatiert die aktuelle Exception und gibt sie über die Pipe aus (zu verwenden im `try:…except:`-Block)
  - `debug.debug_stack()` formatiert den aktuellen Stack und gibt ihn über die Pipe aus (auch außerhalb eines `try:`-Blocks möglich)

