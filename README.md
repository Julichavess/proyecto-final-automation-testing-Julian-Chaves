# Proyecto de Automatización QA — SauceDemo + ReqRes
# Talencho Tech - Julian Chaves

Framework de automatización de pruebas con **Python + Pytest + Selenium** (UI) y **Requests** (API),
implementada con el patrón **Page Object Model**.

## Estructura del proyecto

```
qa_automation_project/
├── pages/              # Page Objects (LoginPage, InventoryPage, CartPage)
├── tests/               # Casos de prueba (UI y API)
├── utils/               # Utilidades (logger)
├── data/                # Datos externos para parametrización (JSON)
├── conftest.py           # Fixtures compartidas + screenshots
├── pytest.ini            # Configuración de pytest y reporte HTML
└── requirements.txt
```

## Instalación

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

También necesitás tener **Google Chrome** y el **ChromeDriver** correspondiente
en el PATH (o usar `webdriver-manager` si preferís que se gestione solo).


## Ejecutar los tests

```bash
pytest
```

Esto corre toda la suite y genera un reporte HTML en `reports/report.html`
con capturas de pantalla automáticas de los tests que fallen.

Para correr solo UI o solo API:

```bash
pytest tests/test_login.py tests/test_inventory.py tests/test_cart.py   # UI
pytest tests/test_api.py                                                 # API
```

## Logs

Cada corrida genera un log detallado en `logs/YYYYMMDD.log` con los pasos
clave de cada test, útil para depurar fallas sin tener que reproducirlas.

## Clonar Repositorio

git clone + https://github.com/Julichavess/proyecto-final-automation-testing-Julian-Chaves.git
