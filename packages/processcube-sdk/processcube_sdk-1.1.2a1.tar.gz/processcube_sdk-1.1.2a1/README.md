# SDK für den ProcessCube

Werkzeuge und Tools für die Entwicklung mit dem ProcessCube

## Unterstützung

Moduleliste:
- processcube_sdk.configuration: Umgang mit Konfigurationsdateien
- processcube_sdk.database: Datenbankzugriffe mit SQLAlchemy und Pandas handeln
- processcube_sdk.external_tasks: External-Tasks-Basis-Klassen und generische Umsetzung (z.B. Prüfen von Instanzen eines Models)
- processcube_sdk.fastapi: fastapi-Auth-Module für den Umgang mit Google-Authentifizierung
- processcube_sdk.jupyter: Vereinfachung der automatischen Ausführung von Jupyter-Notebooks und Ergebnissen, die als Resultat ermittelt werden sollen


## Verwendung
### processcube_sdk.external_tasks

Die External-Tasks haben für die direkte Verwendung eine Möglichekeit als Module direkt gestartet zu werden.

Das Starten erfolgt wie nachfolgende beschrieben:

```shell
python -m pip install processcube_sdk


CONFIG_FILE=`pwd`/config.dev.json PYTHONPATH=. python -m processcube_sdk.external_tasks
```

Die Konfigurationsdatei, sollte dabei folgende Elemente enthalten:
```json
{
    "engine": 
    {
        "url": "http://192.168.178.125:56100"
    },
    "logging": 
    {
        "level": "info"
    }
}
```
#### Verwendung mit Docker

Die Verwendung mit Docker ist unter docs/README.Dockerfile.md beschrieben.


