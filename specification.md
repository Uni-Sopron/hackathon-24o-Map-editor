# Program specifikáció

    24o-hackatoon játékához készült pálya generáló GUI.
    Tkinter felhasználásával készült, codespace-ben nem működik(nincs GUI).
    (Visual Studio Code, Windows 10 rendszer)

# Program működése, funkciók:

    Program futtatásakor egy ablak jelenik meg, ahol felhasználó testre szabhatja a pályát.
    Először a pálya méretének a megadása szükséges, amely sorokból és oszlopokból áll.
    Miután létrejött az alap pálya méret, a mezőkre kattintva "falak" helyezhetőek el.
    Ezek a "falak" eltávolithatóak.
    Van lehetőség véletlenszerű falak elhelyezésére.
    Ennek a maximális értéke a pálya mezőinek száma osztva 2-vel maradék nélkül.
    Véletlenszerű generálás végrehajtása nincs limitálva.
    Ilyenkor mindig egy új "pálya" jön létre.
    Generálást követően is módosithatóak a falak(hozzáadás, törlés).
    A pálya mérete bármikor módositható.
    Ebben az esetben a korábbi pálya törlésre kerül.

# Hiányzó funkciók:

    Pálya kimentése a szervernek megfelelő formátumba
    Pálya betöltése utólagos módositásra
    Pálya extra módositások (türközés, forgatás, adott rész másolás)