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

## Domain Event-ek

### Inventory

* Item Order Rejected
* Item Amount Increased
* Item Amount Decreased
* Item Stock Created
* Item Stock Deleted

### Product Catalog

* Product Created
* Product Deleted

### Order Manager

* Order Item Added
* Order Item Removed
* Order Submitted
* Order Accepted
* Order Rejected
* Order Cancelled

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

Amennyiben a felhasználó törölni szeretne egy rendelést, és a rendelés elérte az elfogadott állapotot, a rendelés törlésre kerül. Az Order Manager elküld egy rendelés törölve eseményt, amire az inventory egy elemmennyiség növelve eseménnyel kompenzál.

#### Alternatív 1

_A rendelés nincsen minimum elfogadott állapotban_

A törölni kívánt rendelés nincsen olyan állapotban, ahol biztonsággal törölni lehet. Az Order Manager megtiltja a cselekményt.

### Use case 3

**A Product Catalog-ban új terméket regisztrálunk**

Az adminisztrátor új terméket akar felvenni a rendszerbe. A Product Catalog küld egy termék létrehozva eseményt. Ezt megkapja az Inventory, ami erre küld egy raktárelem létrehozva eseményt 0 elemmennyiséggel.

### Use case 4

**A Product Catalog-ban egy terméket törlünk**

Az adminisztrátor törölni szeretne egy terméket. A Product Catalog elküld egy termék törölve eseményt. Erre az Inventory elküld egy raktárelem törölve tombstone eseményt. 
