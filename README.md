# Cherminal
Cherminal (née Черминаль) er et terminal-baseret chatroom udviklet af M. S. Sørensen og M. H. Kokholm som eksamensprojekt i Programmering B.

## Hvordan det er lavet
**Brugt tech:** Python samt diverse biblioteker som socket, threading og curses.

For at kargløre programmet skal du skrive ```git clone https://github.com/MarcShade/Cherminal``` og installer de nødvendige dependencies ved ```pip install -r requirements.txt```. Sikrer dig, at en server er startet ved at køre server.py på en maskine på samme netværk og kør derefter en eller flere klienter i terminalen ved at skrive ```python client.py```. Det er vigtigt at bemærke, at ```SERVER_ADDRESS```-variablen i ```client.py``` skal være IPV4-addressen af maskinen som kører serveren.

## Hvad har vi lært?
Projektet har givet et godt indblik i hvordan netværk fungerer.