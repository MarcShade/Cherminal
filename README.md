# Cherminal

Et terminalbaseret chatrum skrevet i Python, udviklet som eksamensprojekt i Programmering B.

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