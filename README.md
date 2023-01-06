# Vurderingsoppgave grunnleggende 2ITA Dokumentasjon
1. Formål, bruksområde og ansvarlige:

    0.1. Hva skal systemet brukes til?
        Dette systemet blir brukt for å spille et quiz spill
	
    0.2. Hvordan det fungerer.
        Funsjonaliteten for systemet ligger i at spilleren skal starte spillet og bruke mus og input for å velge riktig svar til spørsmål som blir stilt på skjermen. Det er også en timer som teller ned samtidig som quiz-spillet pågår, hvis spiller svarer riktig på et svar så får spilleren +5 sekunder på timeren, men hvis spiller svarer feil så får de -5 sekunder på timeren.
	
    0.3. Hvilke andre systemer løsningen jobber med. Inndata og utdata
        Dette programmet bruker hovedsaklig MySql og Python for å kjøres, innenfor Python så blir forskjellige funsjonaliteter impotert som Pygame, tkinter og flere.

2. Rammer:

    0.1. Hvilke lover og forskrifter løsningen skal forholde seg til.
      	Dette programmet har en database, men den lagrer ikke personlig data om spilleren, dette vil si at programmet ikke krever å knytte seg til personverns-lover. (GDPR, Datatilsyn)

3. Systembeskrivelse:

    0.1. Versjon.
        Versjonen er 'commit: 598dd30'
	
    0.2. En beskrivelse av grensesnitt mot andre IT-systemer, manuelle eller maskinelle, som angir type, format og på import- og eksportdata.
        Programmet kommuniserer med MySql databasen for å sende 'Intiger' og 'String' verdier, også kjent som 'int' og 'str' verdier.
	
    0.3. En beskrivelse av IT-systemets oppbygging med programmer, registre, tabeller, database, inndata og utdata, metadata, samt avhengigheter og dataflyt mellom disse. Dersom det er en database, bør både den fysiske og logiske strukturen beskrives.
        Som sagt så kommuniserer programmet ved å gi data/informasjon om spillerens poengsum. MySql databasen mottar denne dataen fra programmet og oppretter en tabell med diverse kolonner, denne dataen som blir satt i kolonner innerholder: 'Navn', 'Score' og 'Tid'.
	
    0.4. En beskrivelse av IT-systemets funksjoner med angivelse av hensikt/bruksområde, inndata, behandlingsregler, innebygd ”arbeidsflyt”, feilmeldinger og utdata. Beskrivelsen omfatter også oppdatering av registre/tabeller.
        Dataen lagres til MySql databasen, denne databasen oppdateres med nye tabeller hver gang en spiller har konkludert en runde. 
	
    0.5. Programmeringsspråk og versjon.
        Programmeringsspråket brukt er 'Python', og versjonen er '3.11'. Jeg brukte også programmet 'MySQL', som var på versjon '8.0.31'

4. Kontroller i og rundt IT-systemet:

    0.1. Enkel risikovurdering av IT-systemets konfidensialitet, integritet og tilgjengelighet.
        Som sagt så er det ingen punkt i programmet hvor persjonlig data/informasjon om spilleren blir lagret, sendt, brukt eller gitt tilgang til.

5. Driftsmessige krav og ressurser:

    0.1. Maskinvare.
	    Minumum kravet for å kunne kjøre dette programmet er en: Raspberry Pi 1.

6. Systembenyttede standarder:

    0.1. Verktøystandarder
        Dette ville vært 'Python 3.11'
	
    0.2. Brukergrensesnitt. (En beskrivelse av regler for oppbygging av skjermbilde og meny, hva en kommando utfører, standard betydning av tastene på tastaturet, fellestrekk ved dialogene etc.)
        Spilleren tar bruk av Pygame sin UserInterface, Pygame har forskjellige inputs man kan bruke, noen av disse som ble brukt i programmet mit var 'MOUSEBUTTONDOWN', 'SPACE' og 'ESC'.
	
    0.3. Navnestandarder variabler.
        Standarden for kodespråk og variabler i Python er å lage et navn uten understreker og mellomrom. 
	
    0.4. Avvik, begrunnelse for avvik fra gjeldende standard(er).
        Det er ingen avvik for dette i mitt program.

7. Programdokumentasjon:
    0.1. Vi må alltid huske å ha et stadig bruk av kommentarer gjennom koden din. Dette øker forståelse av koden din for andre. Du må minst forklare behandlinger, funksjoner, variabler i programmet og hvordan denne koden virker sammen med program som Pygame eller TKinter
    Det er viktig med flittig bruk av kommentarer i programkoden for å gjøre denne lettere å forstå. Et minimum er å forklare programmets funksjon, variabler, behandlingsregler og avhengighet av/ påvirkning på andre programmer.

8. Kjente feil og mangler:

    0.1. Det er viktig å vite om FAQ, kjente feil og mangler, som er godt beskrivd med mulige løsninger.
        Det er forskjellige måter jeg hentet informasjonen som trengtes for dette spillet. Når det kommer til spiller navnet så låser jeg spillet bak en TKinter 'popup' som spør om navnet til spilleren, spilleren kan ikke fortsette til de har satt in et navn eller kanselert 'popupen', hvis kanselert blir spilleren til 'Anon', som er en forkotelse for 'Anonymous'. 

 SQL kobling:
 
	0.1. Først så må du laste ned MySql, etter dette så skal du laste ned 'MySql Connector for Python'.
	
	0.2. Etter MySql og MySql Connector er lastet ned så må du lage en tabel i databasen, dette skal ha verdiene brukt for lagring i programmet mitt.
	
	0.3. Det neste steger er å importere mysql.connector til Python.
	
	0.4. Det fjerde du skal gjøre er å lage en connection med databasen, vi bruker mysql.connector.connect for å oppnå dette. Du må passe på at denne funskjonen spesifiserer variablene som trengs, i dette eksempelet er dette host, user, passord og database). Pass på at du lagrer alt dette som en variabel.
	
	0.5. Sist så bruker du 'cursor' funksjonen til å kunne filtrere og navigere gjennom den spesifikke databasen.

ERD (Entity Relationship Diagram)

    https://gyazo.com/9e92e82c68c4bedd9f8c2c26772dfb80
