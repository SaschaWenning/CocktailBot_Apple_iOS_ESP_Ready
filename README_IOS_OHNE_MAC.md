# CocktailBot für iPhone/iPad – ohne eigenen Mac

Dieses Paket enthält die bestehende Flutter-App inklusive der vorhandenen Maschinen-/Pumpensteuerung. Die HTTP-API (`/api/status`, `/api/command` usw.) wurde nicht ersetzt. Für iOS wurden die native Netzwerkbehandlung und der Cloud-Build ergänzt.

## Was angepasst wurde

- Native iOS-App kann den ESP über seine IP-Adresse bzw. seinen Hostnamen ansprechen.
- Wenn auf iOS/Android noch keine ESP-Adresse eingetragen ist, zeigt die App jetzt eine klare Meldung statt einen ungültigen Same-Origin-Aufruf zu versuchen.
- iOS erhält automatisch die Apple-Datenschutzbeschreibung für den Zugriff auf das lokale Netzwerk.
- Lokale HTTP-/`.local`-Verbindungen werden über `NSAllowsLocalNetworking` ermöglicht, ohne den gesamten App Transport Security-Schutz abzuschalten.
- Die Pumpen-, Status- und LED-Befehle bleiben in `lib/main.dart` enthalten.
- `codemagic.yaml` enthält einen unsignierten Prüfbuild und einen signierten IPA-Build.

## ESP in der App

Auf dem iPhone/iPad unter **Einstellungen → Verbindung** die ESP-Adresse eintragen, zum Beispiel:

- `192.168.4.1`
- `192.168.178.50`
- `cocktailbot.local`
- oder eine vollständige URL wie `http://192.168.4.1`

Die App hängt die vorhandenen API-Pfade automatisch an. ESP und iPhone müssen sich im passenden lokalen Netzwerk befinden. Beim ersten Zugriff fragt iOS nach der Berechtigung **Lokales Netzwerk** – diese erlauben.

## Build ohne Mac mit Codemagic

1. Den kompletten Inhalt dieses Ordners in ein GitHub-Repository hochladen.
2. Bei Codemagic das GitHub-Repository verbinden.
3. Codemagic erkennt die Datei `codemagic.yaml`.
4. Zuerst Workflow **CocktailBot iOS Check (ohne Signierung)** starten. Dafür ist noch keine Apple-Signierung nötig.
5. Für eine installierbare/TestFlight-IPA im Apple Developer Portal die Bundle-ID `de.cocktailbot.app` anlegen. Falls sie nicht verfügbar ist, in `codemagic.yaml` beide Vorkommen von `de.cocktailbot.app` durch deine eigene eindeutige Bundle-ID ersetzen.
6. In Codemagic die Apple-Signing-Zertifikate und das passende App-Store-Provisioning-Profil hinterlegen bzw. über App Store Connect beziehen.
7. Workflow **CocktailBot iOS IPA (signiert)** starten.
8. Die fertige `.ipa` erscheint bei den Build-Artefakten. Für TestFlight kann sie anschließend zu App Store Connect hochgeladen werden.

## Wichtige Dateien

- `lib/main.dart` – komplette CocktailBot-App und ESP-Steuerlogik
- `tool/prepare_ios.py` – erzeugt das fehlende Xcode/iOS-Projekt auf dem Cloud-Mac und setzt die iOS-Netzwerkrechte
- `codemagic.yaml` – Cloud-Builds
- `ios/README_GENERATED_ON_CLOUD.md` – Erklärung zum dynamisch erzeugten iOS-Unterbau

## Android

Die bestehende API-Struktur und die Steuerbefehle wurden nicht auf eine neue Technik umgestellt. Die Änderung an der Host-Auflösung betrifft native Apps nur dann, wenn noch keine ESP-Adresse konfiguriert wurde; bei einer gespeicherten ESP-Adresse wird dieselbe HTTP-Steuerung wie bisher verwendet.
