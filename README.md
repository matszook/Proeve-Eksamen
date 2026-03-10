# Flask Auth App 🔐

Backend Python Dev med autentisering og rollebaserte tillatelser.

## Kom i gang

### 1. Installer Flask
```bash
pip install flask
```

### 2. Kjør appen
```bash
python app.py
```

### 3. Åpne i nettleseren
Gå til: **http://localhost:5000**

---

## Demo-kontoer

| Brukernavn | Passord    | Rolle  | Tilgang                          |
|------------|------------|--------|----------------------------------|
| admin      | admin123   | admin  | Alt (dashboard, brukerpanel, admin-panel) |
| bruker     | bruker123  | user   | Dashboard + brukerpanel          |
| gjest      | gjest123   | guest  | Kun dashboard                    |

---

## Prosjektstruktur

```
flask_auth_app/
├── app.py                  # Hoved Flask-app med routes og autentisering
├── requirements.txt        # Python-avhengigheter
└── templates/
    ├── base.html           # Base-template med nav og felles CSS
    ├── login.html          # Innloggingsside
    ├── dashboard.html      # Dashboard (alle innloggede)
    ├── admin.html          # Admin-panel (kun admin)
    └── user_panel.html     # Brukerpanel (user + admin)
```

---

## Slik fungerer det

### Autentisering
- Passord hashes med SHA-256 (bruk `bcrypt` i ekte prosjekter!)
- Innloggingsstatus lagres i Flask `session` (server-side cookie)
- Utlogging sletter session

### Rollebaserte tillatelser
To dekoratorer beskytter routes:

```python
@login_required          # Krever at bruker er logget inn
@role_required('admin')  # Krever spesifikk rolle
```

### Legge til en ny bruker
I `app.py`, legg til i `USERS`-dict:
```python
'nybruker': {
    'password': hash_password('passord123'),
    'role': 'user',
    'name': 'Ny Bruker'
}
```

---

## Teknologier
- **Python** + **Flask** — Backend og routing
- **Jinja2** — HTML-templates (inkludert i Flask)
- **HTML + CSS** — Frontend med eget design
- **JavaScript** — (ingen JS brukt her, men enkelt å legge til)
- **Sessions** — Autentisering uten database
