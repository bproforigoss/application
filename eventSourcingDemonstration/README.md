# Demonstrációs program

Ez a mappa tartalmazza az Event Sourcing tervezési mintát bevezető szinten demonstráló program fájljait.

*Az utasítások alapján újrajátszható az alábbi felhasználói élmény:*

* Termékek hozzáadása és kivétele a vásárlói kosárból
* Rendelés leadása
* Rendelés törlése (jelen esetben az üzleti logika tiltja)
* Az elmentett események alapján egy új Aggregate objektum felépítése

*A demonstráció futtatásához szükséges:*

* Python 3.8 (a fejlesztéshez használt referencia, f-string támogatása)
* Requests könyvtár (adott környezetben: pip install requests)
* Docker
* EventStoreDB képfájl (legfrissebb vagy 20.6.0.1)

*A futtatás lépései:*

* A mappa és a EventStoreDB képfájl letöltése (docker pull eventstore/eventstore)
* Az EventStoreDB futtatása konténerben az alábbi paranccsal:
docker run --name eventstore-node -it -p 2113:2113 -p 1113:1113 eventstore/eventstore --insecure --enable-atom-pub-over-http (Magyarázat: az --insecure kapcsoló lehetővé teszi, hogy tanúsítványok nélkül kommunikáljunk az EventStoreDB-vel, míg az --enable-atom-pub-over-http kapcsoló lehetővé teszi a HTTP üzenetek használatát)
* A main.py futtatása és a képernyőn megjelenő lépések léptetése Enterrel. Az események kezelésének követése a http://127.0.0.1:2113 oldalon található Admin felületen a Stream Browser alatt található helyeken.
