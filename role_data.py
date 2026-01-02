

# --- KNIHOVNA ROLÍ (TROUBLE BREWING) ---

ROLE_DETAIL_GRIMOIRE = {

    "Pradlena": "První noc zjistíš, kdo z jedné dvojice hráčů je jeden konkrétní Měšťan, a jakou má roli.",
    "Knihovník": "První noc zjistíš, který hráč je jeden konkrétní Outsider, a jakou má roli (nebo že Outsider ve hře není).",
    "Vyšetřovatel": "První noc zjistíš, který hráč je jeden konkrétní Pohůnek, a jakou má roli (nebo že Pohůnek ve hře není).",
    "Kuchař": "Na začátku hry zjistíš, kolik párů zlých hráčů sedí vedle sebe (max 3).",
    "Empatik": "Každou noc zjistíš, kolik zlých hráčů sedí vedle tebe (0, 1 nebo 2).",
    "Vědma": "Každou noc zvolíš 2 hráče; zjistíš, zda je mezi nimi Démon ('Ano'/'Ne'). (Jedna role je pro tebe Falešná stopa).",
    "Hrobař": "Každou noc, po popravě, zjistíš, jakou roli měl hráč, který byl popraven předchozí den.",
    "Mnich": "Každou noc chráníš jednoho hráče před Démonovým útokem (nemůžeš chránit sebe).",
    "Hlídač havranů": "Pokud jsi zabit Démonem, následující ráno zjistíš roli jednoho konkrétního hráče.",
    "Panna": "Pokud tě Měšťan nominuje k popravě, okamžitě zemřeš a nominující Měšťan je v daném dnu imunní vůči popravě.",
    "Zabiják": "Jednou za hru můžeš zvolit hráče; pokud je to Démon, ten okamžitě zemře.",
    "Voják": "Nemůžeš být zabit Démonem.",
    "Starosta": "Pokud tě Měšťané popraví, tvoje poprava selže a přežiješ.",


    "Komorník": "Každou noc zvolíš hráče; následující den ho musíš nominovat k popravě (jinak nemůžeš hlasovat).",
    "Opilec": "Považuješ se za Měšťana, ale nemáš žádnou skutečnou schopnost a všechny tvé informace jsou falešné.",
    "Poustevník": "Občas se některým schopnostem (např. Vědmě) jevíš jako Démon nebo Pohůnek (jsi Falešná stopa).",
    "Svatý": "Pokud jsi popraven, celá Dobrá strana okamžitě prohrává.",


    "Travič": "Každou noc otrávíš jednoho hráče; jeho schopnost je nefunkční a informace jsou falešné.",
    "Špión": "Každou noc vidíš role všech hráčů. Pro ostatní role se můžeš jevit jako jakákoli jiná role (Falešná stopa).",
    "Šarlatánka": "Pokud je Démon popraven, stáváš se novým Démonem.",
    "Baron": "Ve hře jsou o 2 Outsideri více a o 2 Měšťané méně. **(POZOR: Bot tuto změnu neřeší automaticky, ST to musí zohlednit při tvorbě skriptu)**",


    "Skřet": "Každou noc zabiješ jednoho hráče. Můžeš se nechat popravit a vybrat, kdo se stane novým Démonem."
}


ROCNIK_TROUBLE_BREWING = {
    "townsfolk": list(ROLE_DETAIL_GRIMOIRE.keys())[:13],
    "outsiders": list(ROLE_DETAIL_GRIMOIRE.keys())[13:17],
    "minions": list(ROLE_DETAIL_GRIMOIRE.keys())[17:21],
    "demons": list(ROLE_DETAIL_GRIMOIRE.keys())[21:]
}

NASTAVENI_PODLE_HRACU = {
    5: (3, 0, 1, 1),
    6: (3, 1, 1, 1),
    7: (5, 0, 1, 1),
    8: (5, 1, 1, 1),
    9: (5, 2, 1, 1),
    10: (7, 0, 2, 1),
    11: (7, 1, 2, 1),
    12: (7, 2, 2, 1),
    13: (9, 0, 3, 1),
    14: (9, 1, 3, 1),
    15: (9, 2, 3, 1),
}