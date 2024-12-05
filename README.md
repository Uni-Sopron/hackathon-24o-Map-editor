# Program specifikáció

    A programunk egy játékpályát generáló alkalmazás amit a Python Tkinter moduljával készítettünk. 
    A Tkinter grafikus felhasználói felületet biztosít.
    Az alkalmazásban a felhasználók saját pályákat generálhatnak, falakat jelölhetnek ki,
    vagy random pályákat hozhatnak létre amelyeket tükrözni és forgatni is lehet.
    A pályákat oszlop illetve sor megadásával is generálhatjuk,
    de akár egy külső szerverről vagy egy txt-be mentett fájlból is betölthetjük.


# Program működése, funkciók:

    Pálya méretének megadása: 
    User megadja a pálya sorainak és oszlopainak számát a szövegmezőben
    Létrehozás gombbal létrejön az üres pálya rács szerkezete
    Interakciók: 
    User blokkokat jelölhet ki, vagy random generálhat, amelyeket a program akadályként, falként kezel
    Pálya módosítási funkciók: 
    Függőleges vagy vízszintes tükrözés, forgatás 90 fokban
    A pálya kimenthető fájlba és vissza is tölthető az alkalmazásba.

# Főbb tkinter elemek:

    Label: szövegek megjelenítésére
    Entry: szövegmező, adatok megadása pl. pályaméret
    Button:  interaktív gomb, műveletek végrehajtása
    Canvas:  a pálya vizuális megjelenítése itt történik
    FileDialog: fájlok betöltése és mentése

# GameBoard osztály bemutatása:

    Ez az osztály az alkalmazás központi eleme, tartalmazza a játék logikáját GUI felépítését.

    self.root: fő ablak, gyökérelem
    self.canvas: vizuális „rajzfelületért” felelős
    self.grid: kétdimenziós lista, pálya állapotát tárolja 0 üres 1 akadály, ezt tároljuk txt-ben
    self.board_size: pálya mérete
    self.cell_size: cellák mérete pixelben
    self.obstacle_color: akadályok megjelenítésére használt szín

# GameBoard osztály függvényei:

    __init__ : alapvető elemek, pályaméret szövegmezők, beviteli mezők, gombok, canvas
    create_board(): üres pálya létrehozása megadott méretek alapján: 
    Sor és oszlop alapján tölti a self.grid-et, új canvas object megjelenítéshez
    create_table(): pálya aktuális állapotának megjelenítése a canvason, 
    végigiterál a rács minden celláján és megrajzolja a megfelelő téglalpot
    reverse_block(): egy cella állapotának megváltoztatása, 0 üres vagy 1 akadály
    add_random_walls(): véletlenszerű akadályok létrehozása, aktuális grid törlése
    save_board(): aktuális pályaállapot kimentése txt-be, filedialog mentés hely választás
    load_board_file(): txt-be mentett pálya betöltése
    load_board_file(): szerverről betöltött pálya HTTP kéréssel
    mirror_vertical, horizontal, rotate90 a függvények a tükrözések, forgatás
