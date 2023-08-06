certbot-dns-rockenstein
=======================

rockenstein DNS Authenticator plugin für Certbot

Dieses Plugin hilft bei der Automatisierung der Erstellung und Verlängerung von Let's Encrypt-Zertifikaten in Verbindung mit Certbot.

Im Rahmen des ``dns-01`` Verfahrens werden automatisch TXT-Records der entsprechenden Domain hinzugefügt und entfernt.

Installation
------------

    pip install certbot-dns-rockenstein

Named Arguments
---------------

Um den Certbot in Verbindung mit der RoxApi der rockenstein AG zu verwenden, fügen Sie folgende Argumente Ihrem Certbot-Aufruf hinzu:



**Required**
```
--authenticator certbot-dns-rockenstein
```

Legt fest, dass dieses Plugin verwendet werden soll.

**Required**
```
--certbot-dns-rockenstein-token <token>
```

Dieser Parameter übergibt das Token zur Authentifzierung an der rockenstein RoxApi. Der Token kann im Service-Portal der rockenstein AG generiert werden.

Bei Fragen hierzu wenden Sie sich bitte an unseren Support.

**Optional**
```
--certbot-dns-rockenstein-url <url>
```

Legt eine alternative URL der rockenstein RoxApi fest. Im Normalfall muss hier nichts angegeben werden.

**Optional**
```
--certbot-dns-rockenstein-ignore-ssl
```
Deaktiviert die Überprüfung des SSL-Zertifikats der rockenstein RoxApi. Dies dient nur zum Einsatz in Verbindung mit einer lokalen API-Entwicklungsumgebung und ist für den normalen Einsatz nicht relevant.

Beispiele
---------

Ein typischer Aufruf zum Erstellen von einem neuen SSL-Zertifkat ist:

```
certbot certonly --authenticator certbot-dns-rockenstein --certbot-dns-rockenstein-token <token> -m <admin-email-adresse> --agree-tos -d <fully-qualified-domain-name>
```

