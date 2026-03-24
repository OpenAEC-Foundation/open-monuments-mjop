app_name = "mjop"
app_title = "Open-Monuments MJOP"
app_publisher = "OpenAEC Foundation"
app_description = "Meerjarenonderhoudsplan: berekening, planning en export van onderhoudsprogramma's voor monumenten."
app_email = "info@openaec.org"
app_license = "lgpl-3.0"
app_version = "0.1.0"

required_apps = ["frappe", "erpnext", "monuments_core"]

# DocTypes waarvoor de standaard Frappe Desk-weergave verborgen wordt
# (we gebruiken een headless React-frontend, zie D009)
hide_in_desk = 1

# Custom roles — worden aangemaakt bij installatie
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Mjop"]],
    },
]

# Whitelisted API-methoden toegankelijk voor de React-frontend
override_whitelisted_methods = {}

# Documentatie-URL
app_documentation = "https://github.com/OpenAEC-Foundation/Open-Monuments/tree/main/apps/mjop"
