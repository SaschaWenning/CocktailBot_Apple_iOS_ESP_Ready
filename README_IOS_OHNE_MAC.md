# CocktailBot für iPhone/iPad ohne eigenen Mac

Dieses Paket enthält die vorhandene Flutter-App samt ESP-Steuerlogik und eine Codemagic-Konfiguration, die das fehlende native iOS/Xcode-Projekt erst auf dem Cloud-Mac erzeugt.

## Wichtig: Codemagic als YAML-Workflow starten

Die Datei `codemagic.yaml` muss im **Hauptverzeichnis des GitHub-Repositories** liegen und mit hochgeladen/committed werden.

In Codemagic:

1. Repository/Branch aktualisieren, damit diese neue Version wirklich enthalten ist.
2. Bei der App den Branch auswählen und **Check for configuration file** / `codemagic.yaml` verwenden.
3. Als ersten Test den Workflow **CocktailBot iOS Check (ohne Signierung)** starten.
4. Nicht den automatisch eingerichteten iOS-Workflow aus dem Flutter Workflow Editor verwenden. Dieser versucht das Xcode-Projekt zu finden, bevor unser Erzeugungsschritt läuft.

## Warum der frühere Build fehlgeschlagen ist

Im alten Paket existierte ein Ordner `ios/`, der nur eine README enthielt. Codemagic erkannte dadurch eine iOS-Struktur, fand aber `ios/Runner.xcodeproj` nicht. Das führte zu:

`Did not find xcodeproj from /Users/builder/clone/ios`

In dieser korrigierten Version gibt es **keinen leeren ios-Platzhalter** mehr. Der erste Codemagic-Schritt führt `tool/prepare_ios.py` aus. Das Skript:

- entfernt ein eventuell unvollständiges `ios/` automatisch,
- führt `flutter create --platforms=ios ...` aus,
- prüft explizit, dass `ios/Runner.xcodeproj/project.pbxproj` erzeugt wurde,
- ergänzt die iOS-Berechtigung für das lokale Netzwerk,
- erlaubt lokalen Netzwerkverkehr zum ESP,
- setzt den Bundle Identifier,
- verändert die bestehende Dart-/ESP-Steuerlogik nicht.

## Erster Build

Starte zuerst:

**CocktailBot iOS Check (ohne Signierung)**

Im Log sollte früh erscheinen:

- `iOS Xcode project is ready.`
- `Verified: ios/Runner.xcodeproj/project.pbxproj`
- `Verified: ios/Runner/Info.plist`

Erst wenn dieser Workflow erfolgreich ist, den signierten Workflow **CocktailBot iOS IPA (signiert)** konfigurieren/starten.

## ESP-Verbindung

Die vorhandene HTTP-Steuerung der App bleibt bestehen. Auf dem iPhone muss der Zugriff auf das lokale Netzwerk erlaubt werden. Anschließend wird in der App wie unter Android die IP/der Hostname des ESP verwendet.
