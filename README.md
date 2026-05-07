# Cherminal
Cherminal (née Черминаль) er et terminal-baseret chatroom udviklet af M. S. Sørensen og M. H. Kokholm som eksamensprojekt i Programmering B.

## Features

- Offentlig chat mellem flere brugere
- Private beskeder via `/pm [brugernavn]`
- Kryds og bolle via `/ttt [brugernavn]`
- Simpelt terminal-GUI via curses

## Installation

```bash
git clone https://github.com/MarcShade/Cherminal
cd Cherminal
pip install -r requirements.txt
```

## Brug

Start serveren:
```bash
python server.py
```

Start klienten (i en separat terminal):
```bash
python client.py
```
Det er vigtigt at bemærke, at ```SERVER_ADDRESS```-variablen i ```client.py``` skal være IPV4-addressen af maskinen som kører serveren.

## Kommandoer

| Kommando | Beskrivelse |
|---|---|
| `/pm [brugernavn]` | Send en privat besked-invitation |
| `/ttt [brugernavn]` | Send en kryds og bolle-invitation |
| `/accept` | Acceptér en invitation |
| `/decline` | Afvis en invitation |
| `/leave` | Forlad en session |
| `/help` | Vis tilgængelige kommandoer |
| `/quit` | Afslut programmet |

## Teknologier

Python · socket · threading · curses
