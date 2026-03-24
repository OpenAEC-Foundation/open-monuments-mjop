from . import __version__ as app_version

app_name = "mjop"
app_title = "Open-Monuments MJOP"
app_publisher = "OpenAEC Foundation"
app_description = "Meerjarenonderhoudsplan: berekening, planning en export van onderhoudsprogramma's voor monumenten."
app_email = "info@openaec.org"
app_license = "lgpl-3.0"

required_apps = ["frappe", "erpnext", "monuments_core"]

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Mjop"]],
    },
]
