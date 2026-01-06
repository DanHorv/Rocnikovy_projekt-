# Rocnikovy_projekt
Discord Bot na hru Blood of the clocktower

Můj ročnikový projekt se zabývá ohledně discord bota který pomáhá story tellerovi(ST) při rozdělování postav, obeznámení všech o postavách a co je jich cílem ve hře," ukádaní lidí do postelí na noc" a znovu potom dostaní lidí zpět do roomky, určování pauzy a opět vrácení všech do jedné roomky.

celý bot je napsaný v v pycharmu 

smysl hry je v podstatě vylepšené mestečko palermo s více pravidly, více postavami, hra je udělená pro 5-15 hráčů plus ST

Celý kód by měl být blbuvzdorný takže by bot nikdy neměl spadnout 

How to start:
1. Je potřeba si stáhnout "bot.py" (zde je celý bot) , "role_data.py" (zde jsou uložený role a rozdělí postav podle počtu)a "requirments.txt" ( bez tohohle by to nefungovalo ) 
2. Zapnete si terminal a stáhenete si requirtments ( je to nutné stáhnout protože čistý python tohle nedokáže spustit sám discord bota logicky...)
3. Vytvoříte si Soubor ".env" a dáte tam "DISCORD_TOKEN=(Zde zadáte svůj discord token)"

3.1 Pokud ještě nemáte discord bot token, zajdětě na stranku, https://discord.com/developers/, kde se přihlásíte a vytvoříte bota. Poté mu nastavte intensions(co by měl být schopný dělat), já jsem tam nastavil všechno aby mi to 100% fungovalo, a zadat permice které si role bota bude vyžadovat na serveru, osobně jsem zadal administratorské aby vše fungovalo abych to případně v budoucnu nemusel upravovat.

4. pozvětě bota na svůj Discord server

5. Připravte si svůj Discord server
  5.1 Co je potřeba:
   
   1x Hlavní Channel, v základu je pojmenovanej "Náměstí" ale to kdyžtak jde upravovat ( řádek 24 )
   Vytvořit roli "Storyteller"
   Pár vedlejších roomek aby se lidi mohli rozejít při dnu aby mohli zjistit informace ( počet podle vašeho uvážení )
  5.2 Optional věci
   
   Popsat do nějaké roomky pravidla a role ať lidi vědí co každá postava dělá 
6. Teď už stačí zapnout Bota a sehnat kamarády :D

Komandy : 

!Role ( dá ti roli storytellera, storyteller dokáže zapnout online hru )

!starthry !startgame !start ( zapne hru pro všechny lidi kteří jsou v hlavní channelu a rozděli je do vlastních roomek "postelí" přičemž jim zašle co jsou za roli, co dělají a jaký mají cíl hry ) 

!noc ( tento komand se používá když bylo už odhlasováno a už není co dělat přes den a přesune všechny do svých postelí ) 

!den !konecnoci !day ( tento komand přesune všechny z postalí ho hlavní roomky ) 

!volno {sekundy} ( storryteller po raním srazu určí volno při čemž se lidi můžou volně pohybovat a zjištovat informace ohledně ostatních, po uplynutí stanoveného času bot všechny přesune zpět do hlavního channelu ) 

!offline {počet hráčů) ( pokud kdokoliv zavolá tenhle komand, bot automaticky zašle rozdělení rolí hráči do PM a může si zahrát tuto hru i IRL se svými přateli ( pokud nějaký má xDDD) 

Minihra:
!cislo ( uhodni čislo od 1-5, toto jsem vytvořil protože proč ne xD) 

Jak probíhá hra: 

Sežeň kamarády ( minimálně 5 + ty )

Zapni hru ( !start) 

Všem hráčům přijde zpráva co jsou 

Tobě příjde do zprávy Grimoire ( seznam všech ), zjisti kdo potřebuje další informace ke svojí roli 

Poté zavolej !den všichni se proberou a můžeš vyslat všechny na !volno 

po volnu může začít hlasování, hlasuje se že když někdo chce někoho vyhodit tak musí říct že ho chce vyhodit a důvod potom ten který má být vyhozený řekně obhajobu, po obhajobě žačne hlasování, pokud dostane člověk dostane 50% a více hlasů tak je vyhozen, ale pokud tu bude druhé hlasování a ten druhý člověk dostane více hlasů jak ten první, je vyhozen on ( pozor: duch může taky hlasovat ale pouze jednou od smrti ) 

a takhle se to opakuje dokud nevyhraje jeden z týmů 



zdroje: 

Nápad jsem ukradl kamarádovi který vytvořil podobnou verzi tohoto bota, Dík Frankie xD

GEMINI

RAPPTZ. discord.py documentation [online]. [cit. 2025-05-22]. Dostupné z: https://discordpy.readthedocs.io/en/stable/


TECH WITH TIM. How to Build a Discord Bot With Python - Full Tutorial 2025+ [online video]. 22. dubna 2025 [cit. 2025-05-22]. Dostupné z: https://www.youtube.com/watch?v=YD_N6Ff

