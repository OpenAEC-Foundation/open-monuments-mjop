"""Frappe DocType controller voor Mjop (Meerjarenonderhoudsplan).

Verantwoordelijk voor:
- Validatie van looptijd en regels (F006)
- Automatische kostenberekening (F007)
- Export-gereedheid controleren (F022)
"""

import frappe
from frappe.model.document import Document


class Mjop(Document):
    def validate(self) -> None:
        self._valideer_looptijd()
        self.bereken_totaalkosten()

    def _valideer_looptijd(self) -> None:
        """Controleert dat eindjaar na beginjaar ligt en looptijd redelijk is."""
        if self.looptijd_eind <= self.looptijd_start:
            frappe.throw("Eindjaar moet na beginjaar liggen.")
        looptijd = self.looptijd_eind - self.looptijd_start
        if looptijd > 30:
            frappe.throw("Looptijd mag maximaal 30 jaar zijn.")

    def bereken_totaalkosten(self) -> None:
        """Herberekent totaalkosten en gemiddelde jaarkosten op basis van alle regels."""
        totaal = sum(float(r.kosten_eur or 0) for r in (self.regels or []))
        self.totaalkosten_eur = totaal

        looptijd = max(1, (self.looptijd_eind or 0) - (self.looptijd_start or 0))
        self.gem_kosten_per_jaar_eur = round(totaal / looptijd, 2)

    @frappe.whitelist()
    def genereer_regels_vanuit_inspecties(self) -> dict:
        """
        Genereert MjopRegels op basis van openstaande gebreken uit het meest recente
        inspectieformulier van dit monument (F006 — MJOP generatie).

        Retourneert een dict met het aantal gegenereerde regels.
        """
        if not self.monument:
            frappe.throw("Sla het MJOP eerst op met een gekoppeld monument.")

        # Haal laatste inspectie op
        inspecties = frappe.get_all(
            "Inspectie",
            filters={"monument": self.monument},
            fields=["name", "datum"],
            order_by="datum desc",
            limit=1,
        )
        if not inspecties:
            frappe.msgprint("Geen inspecties gevonden voor dit monument.")
            return {"gegenereerd": 0}

        inspectie_naam = inspecties[0]["name"]
        gebreken = frappe.get_all(
            "Bevinding",
            filters={"inspectie": inspectie_naam},
            fields=["name", "bouwdeel", "element_naam", "tekst", "hersteladvies"],
        )

        aangemaakt = 0
        for gebrek in gebreken:
            # Bepaal urgentiejaar op basis van ernst (NEN 2767 logica)
            urgentie_offset = {
                "Kritiek": 0,
                "Ernstig": 1,
                "Matig": 2,
                "Gering": 5,
            }.get(gebrek.get("ernst", "Matig"), 3)

            urgentiejaar = min(
                self.looptijd_start + urgentie_offset,
                self.looptijd_eind,
            )

            self.append("regels", {
                "bouwdeel": gebrek.get("bouwdeel"),
                "maatregel": gebrek.get("omschrijving", "Herstel gebrek"),
                "jaar": urgentiejaar,
                "kosten_eur": gebrek.get("herstelkosten_eur", 0),
                "prioriteit": gebrek.get("ernst", "Matig"),
                "tijdcategorie": "Regulier onderhoud",
                "gebrek_ref": gebrek.get("name"),
            })
            aangemaakt += 1

        self.bereken_totaalkosten()
        self.save()
        return {"gegenereerd": aangemaakt}
