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

Die vorhandene HTTP-Steuerung der App bleibt bestehen. Auf dem iPhone muss der Zugriff auf das lokale Netzwerk erlaubt werden. Anschließend wird in der App die IP bzw. der Hostname des ESP verwendet.

## Apple-Datenschutzhinweise (Build 7+)

Das iOS-Vorbereitungsskript setzt automatisch die von Apple verlangten Zweckbeschreibungen für lokales Netzwerk, Fotomediathek und Kamera. Diese Einträge werden bei jedem Codemagic-Build neu in `ios/Runner/Info.plist` geschrieben.

## v5: Bilder vollständig lokal auf dem Mobilgerät

Eigene Rezeptbilder werden nicht mehr an den ESP gesendet. Die App wählt die Bilddatei lokal aus, komprimiert sie auf dem Gerät zu JPEG und speichert sie anschließend als Base64 zusammen mit den lokalen App-Daten. Dadurch ist zum Auswählen oder Anzeigen eigener Rezeptbilder keine ESP-Verbindung erforderlich.

Hinweis: Lokal auf einem Gerät hinzugefügte Bilder werden nicht automatisch auf ein anderes Gerät übertragen. Jedes Gerät hat seinen eigenen lokalen App-Speicher.

## Standard-IP des ESP
Auf unterstützten Mobilgeräten wird bei einer noch nicht gespeicherten ESP-Adresse automatisch `192.168.4.1` verwendet und im Verbindungsfeld angezeigt. In der Web-Version bleibt weiterhin Same-Origin möglich.

## Änderungen v7

- iOS-Homescreen-App-Icon aus dem CocktailBot-Logo wird beim CI-Build automatisch in `AppIcon.appiconset` installiert.
- Gewerbelizenz: Geräte-ID wird weiterhin vom CocktailBot-ESP gelesen (nicht vom iPhone), jetzt mit kompatibler Erkennung mehrerer Feldnamen und Fallback über `/api/status`, `/api/info` und `/api/device`.
- Bei fehlender Controller-ID zeigt die App einen klaren Verbindungs-/ESP-Hinweis statt dauerhaft nur „Wird ermittelt …“.
- `NSLocationWhenInUseUsageDescription` und `ITSAppUsesNonExemptEncryption=false` werden für Apple automatisch gesetzt.


## v8 – App-Store-Icon

Das iOS-App-Icon wurde durch ein finales CocktailBot-Branding (dunkler Hintergrund, neongrünes Cocktailglas) ersetzt, damit Apple es nicht mehr als Platzhalter einstuft.


## v9 – App-Icon wie Startbildschirm

Das iOS-App-Icon verwendet jetzt das gleiche CocktailBot-Logo wie der Startbildschirm der App. Das vollständige Logo wird auf weißem Hintergrund als quadratisches iOS-App-Icon ausgegeben.

## v11 – Cocktailbilder bei Updates reparieren

Die eingebauten Cocktailbilder werden beim Laden der App anhand der Rezept-ID automatisch wieder dem korrekten Asset unter `assets/drinks/cocktailbot/` zugeordnet, wenn ein lokal gespeicherter Rezeptdatensatz einen leeren oder veralteten Asset-Pfad enthält. Eigene lokal gewählte Bilder (`data:image/...`) werden nicht überschrieben. Codemagic prüft vor dem Build zusätzlich, ob die Cocktailbild-Assets vorhanden und in `pubspec.yaml` eingebunden sind.


## v12 – App-Review 2.3.10

Alle sichtbaren und dokumentarischen Hinweise auf andere mobile Plattformen wurden aus dieser iOS-Ausgabe entfernt. Der Codemagic-Workflow prüft zusätzlich `lib/` und `assets/` und bricht ab, falls dort entsprechende Plattformnamen auftauchen.


## v14 – App-Icon zuverlässig für App Store Connect

Das iOS-App-Icon verwendet jetzt Apples aktuellen Single-1024-Asset-Catalog-Ansatz. Der Xcode-Build wird explizit auf `AppIcon` gesetzt. Nach dem IPA-Build prüft Codemagic zusätzlich das signierte App-Bundle: `Assets.car` muss vorhanden sein und `CFBundlePrimaryIcon/CFBundleIconName` muss `AppIcon` enthalten. Ein Build ohne korrekt registriertes App-Icon wird dadurch vor dem Upload gestoppt.


## v15 – Cocktailbilder dauerhaft repariert

Für mitgelieferte Cocktails wird das Bild jetzt direkt über die feste Rezept-ID dem bekannten Asset in `assets/drinks/cocktailbot/` zugeordnet. Alte, leere oder fehlerhafte `imagePath`-Werte aus SharedPreferences können die Bilder dadurch nicht mehr ausblenden. Selbst ausgewählte lokale Bilder (`data:image/...`) haben weiterhin Vorrang. Zusätzlich prüft Codemagic das fertige signierte IPA und bricht den Build ab, falls die Cocktailbild-Assets nicht physisch im App-Bundle enthalten sind.
