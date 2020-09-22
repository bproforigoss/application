# Microservice-alapú alkalmazás

Itt a fejlesztési és üzemeltetési platformhoz készülő microservice architektúra alapú demo alkalmazás tervei és később forrásfájljai találhatóak.

## Az alkalmazás

Az alkalmazás jelenlegi képességei:

* Központi adattárolóban terméknyilvántartás vezetése és kezelése
* A tárolt termékek webes felületen való megjelenítése
* Termékrendelések leadásának biztosítása és adminisztrálása

Az alkalmazés komponensei:

### Event Store

Messaging alkalmazás az event sourcing megvalósítására. Az architektúrában a kommunikáció legnagyobb része rajta keresztül zajlik. A rendszer minden változását event-ként eltárolja. (_A kifejezett technológia még kérdéses._)

### Order Manager

Feladata a rendelésekhez kötött személyes információk és a megrendelt elemek mennyiségének az eltárolása. A felelősségi köre csak annyira terjed ki, amennyire el kell tudnunk tárolni adatokat a rendszerben leadott rendelésekről. Az egyéb tényeket, mint a rendelés sikeressége vagy a megrendelt elem konkrét adatai, más szolgáltatás teszi elérhetővé.

### Inventory

A rendszerben regisztrált termékek tárolását szolgálja. Egyedül a termékek raktáron lévő mennyiségének a nyilvántartásáért felelős. (_Az adatbázis módosításait jelenleg direkt módon végezzük._)

### Product Catalog

Az áruház által kínált termékek adatait tárolja.

### Web UI

Az alkalmazás frontendje, ahol a felhasználó megtekintheti a kínált termékeket és rendeléseket adhat le.

## Design

Az alkalmazás design terve készítés alatt áll. A jelenleg aktív verzió elemei:

### Komponens diagram

![Komponens diagram](/pictures/ArchitectureDiagram.png)

### Adatbázis séma

![Adatbázis séma terve](/pictures/AppSchema.png)

## Use case-ek

### Use case 1

**Felhasználó lead egy rendelést**

A felhasználó kiválasztja a megrendelendő termékeket és a mennyiséget megadva, a személyes adatait hozzáfűzve leadja a rendelését. Ekkor a Web UI átadja a rendelést az Order Manager-nek. Az Order Manager eltárolja a rendelés adatait értesíti az Event Store-t, hogy egy rendelés leadásra került. Az Event Store létrehoz egy eseményt, amiben megadja az esemény adatait és a státuszát "PENDING"-re állítja. Ekkor értesíti az Inventory-t a rendelés esemény létrejöttéről. Az Inventory az esemény hatására ellenőrzi az általa nyílvántartott termékeket, és ha elegendő van raktáron, levonja a mennyiséget az általa tárolt mennyiségből. Ekkor az Inventory értesíti az Event Store-t, hogy a rendelés mennyisége levonásra került, így az Event Store a rendelés státuszát "ORDERED" állapotra váltja. Ezután értesíti a Web UI-t, hogy a rendelés "ORDERED" állapotba került, ami megjeleníti az információt a felhasználónak.

**Alternatív lefutások**

#### Alternatív 1

_Az Inventory-ban nincsen annyi termék, mint amennyit rendeltek_

Az Inventory a rendelés létrehozva esemény hatására ellenőrzi az általa tárolt mennyiséget, de az kevesebb, mint a megrendelt elem mennyisége. Az Event Store-t értesíti arról, hogy a rendelést nem tudta levonni a raktári mennyiségből. Az Event Store erre a rendelés állapotát "REJECTED_NOT_ENOUGH_STOCK" állapotra állítja és értesíti a Web UI-t és az Order Manager-t. A Web UI erre megjeleníti a felhasználónak a rendelés sikertelenségét és az okot. Az Order Manager törli a megrendelés adatait.

### Use case 2

**Felhasználó töröl egy már leadott rendelést**

A felhasználó törölni szeretné az általa leadott rendelést. A Web UI értesíti az Event Store-t erről. Az Event Store ellenőrzi a rendelés állapotát. A rendelés "ORDERED" státutszban van, ezért a megrendelt elemek adataival értesíti az Inventory-t, hogy az adott mennyiségek megrendelése törlésre került. Az Inventory visszatölti a termékek raktári mennyiségét és értesíti az Event Store-t arról, hogy visszaállította az eredeti állapotot. Az Event Store a rendelés státuszát "ITEMS_RECLAIMED" állapotba állítja. Ezután értesíti az Order Manager komponenst, hogy törölje a megrendelés adatait. Az Order Manager törli a rendelést és értesíti az Event Store-t. Erre az Event Store "REVOKED" státuszba helyezi a rendelést. Erről értesíti a Web UI-t, ami megjeleníti a művelet eredményét.

**Alternatív lefutások**

#### Alternatív 1

_A rendelés állapota "PENDING"_

A rendelés "PENDING" státuszban van. Az Event Store értesíti a Web UI-t a törlés sikertelenségéről és okáról. A Web UI megjeleníti az eredményt és az okot, felkéri a felhasználót a visszajelzés megvárására.

### Use case 3

**A felhasználó megnyitja a weboldalt**

A felhasználó betölti a Web UI-t. A Web UI lekéri a Product Catalog-tól a rendelkezésre álló termékek listáját és megjeleníti. Szintén lekéri az Order Manager-től a saját rendeléseinek a listáját.
