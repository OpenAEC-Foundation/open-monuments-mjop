"""Geplande achtergrondtaken voor de MJOP-module."""

import frappe


def herbereken_totaalkosten():
    """
    Dagelijkse taak: herberekent totale MJOP-kosten voor alle actieve plannen.
    Wordt getriggerd als een MjopRegel gewijzigd wordt buiten de normale flow.
    """
    plannen = frappe.get_all("Mjop", filters={"status": "Actief"}, fields=["name"])
    for plan in plannen:
        doc = frappe.get_doc("Mjop", plan["name"])
        doc.bereken_totaalkosten()
        doc.save(ignore_permissions=True)
    frappe.db.commit()
