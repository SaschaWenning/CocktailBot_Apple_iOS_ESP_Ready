CocktailBot – Flutter-App mit ESP-Steuerung und iOS-Cloud-Build

Enthalten:
- lib/main.dart (vollständige App- und ESP-Steuerlogik)
- pubspec.yaml
- Cocktailbilder und Logo
- codemagic.yaml für iOS-Cloud-Builds
- tool/prepare_ios.py für den automatisch erzeugten Apple/Xcode-Unterbau
- README_IOS_OHNE_MAC.md mit der Schritt-für-Schritt-Anleitung

Android:
Die bestehende HTTP-Steuerung bleibt erhalten. Wenn du dieses Paket in dein bereits
funktionierendes Android-Flutter-Projekt übernimmst, lib/, assets/ und pubspec.yaml
wie bisher zusammenführen/ersetzen und anschließend flutter pub get ausführen.

ESP-Verbindung:
Auf nativen Geräten (Android/iPhone/iPad) unter Einstellungen > Verbindung die
IP-Adresse oder den Hostnamen des ESP eintragen, zum Beispiel 192.168.4.1 oder
cocktailbot.local. Die API-Pfade /api/status und /api/command bleiben unverändert.

iPhone/iPad ohne eigenen Mac:
Siehe README_IOS_OHNE_MAC.md. Codemagic erzeugt das fehlende Xcode-Projekt auf
einem Cloud-Mac, setzt die Apple-Berechtigung für das lokale Netzwerk und kann
eine signierte IPA erzeugen.

Aktuelle Standard-Pumpenzuordnung:
1 Wodka
2 Brauner Rum
3 Malibu
4 Pfirsichlikör
5 Tequila
6 Triple Sec
7 Blue Curaçao
8 Gin
9 Limettensaft
10 Grenadine
11 Vanillesirup
12 Orangensaft
13 Ananassaft
14 Maracujasaft
15 Mandelsirup
16 Kokossirup
17 Pitu
18 Rohrzucker
