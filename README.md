# Microservice-alapú alkalmazás

Itt a fejlesztési és üzemeltetési platformhoz készülő microservice architektúra alapú demo alkalmazás tervei és később forrásfájljai találhatóak.

## Az alkalmazás

Az alkalmazás jelenlegi képességei:

* Központi adattárolóban terméknyilvántartás vezetése és kezelése
* A tárolt termékek webes felületen való megjelenítése
* Termékrendelések leadásának biztosítása és adminisztrálása

Az alkalmazés komponensei:

### Event Store

Event sourcing megvalósítása. (_A kifejezett technológia még kérdéses._)

### Order Manager

A rendelések leadását teszi lehetővé. Felelősségi köre a _rendelések_.

### Inventory

A Product Catalog elemek mennyiségének nyilvántartása. Felelősségi köre az _elemek mennyisége_.

### Product Catalog

Az áruház által kínált termékek adatait tárolja. Felelősségi köre a _termékek_.


## Design

Az alkalmazás design terve készítés alatt áll. A jelenleg aktív verzió elemei:

### Komponens diagram

![Komponens diagram](/pictures/ArchitectureDiagram.png)

## Use case-ek

### Use case 1

**Felhasználó lead egy rendelést**

A felhasználó kiválasztja a megrendelendő termékeket és a mennyiséget megadva leadja a rendelését. Az Order Manager ellenőrzi a rendelés helyességét, elküld egy rendelés hozzáadva eseményt. Az értesítést megkapja az Inventory. Az ellenőrzi az általa nyílvántartott termékeket, és ha elegendő van raktáron, elküld egy elemmennyiség csökkentve eseményt. Az Order Manager - amennyiben minden termék el lett fogadva - elküld egy rendelés elfogadva eseményt.

**Alternatív lefutások**

#### Alternatív 1

_Az Inventory-ban nincsen annyi termék, mint amennyit rendeltek_

Az Inventory ellenőrzi az általa tárolt mennyiséget, de az kevesebb, mint a megrendelt elem mennyisége. Elküld egy elemrendelés elutasítva eseményt. Az Order Manager erre elküld egy rendelés visszautasítva tombstone eseményt.

### Use case 2

**Felhasználó töröl egy már leadott rendelést**

?Rendelés törlése, de a mennyiség már levonásra került?
?Rendelés törlése, de még nem lett levonva?
?rendelés törlése, de már elfogadták?

### Use case 3

**A Product Catalog-ban új terméket regisztrálunk**

Az adminisztrátor új terméket akar felvenni a rendszerbe. A Product Catalog küld egy termék létrehozva eseményt. Ezt megkapja az Inventory, ami erre küld egy raktárelem létrehozva eseményt 0 elemmennyiséggel.

### Use case 4

**A Product Catalog-ban egy terméket törlünk**

Az adminisztrátor törölni szeretne egy terméket. A Product Catalog elküld egy termék törölve eseményt. Erre az Inventory elküld egy raktárelem törölve tombstone eseményt. 
