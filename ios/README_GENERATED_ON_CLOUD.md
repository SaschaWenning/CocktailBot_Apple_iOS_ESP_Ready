# iOS-Projekt

Die eigentlichen Xcode-Dateien werden absichtlich auf dem macOS-Buildrechner erzeugt.
Das übernimmt `tool/prepare_ios.py` automatisch mit `flutter create --platforms=ios`.

Danach setzt das Skript:

- App-Name: **CocktailBot**
- Bundle-ID: aus `BUNDLE_ID` (Standard `de.cocktailbot.app`)
- `NSLocalNetworkUsageDescription` für die Verbindung zum ESP
- `NSAllowsLocalNetworking = true` für lokale HTTP-/`.local`-Verbindungen

So kann das Projekt von Windows aus gepflegt und auf Codemagic als iOS-App gebaut werden.
