"""Frappe DocType controller voor Mjop Regel (child table van Mjop).

Een MjopRegel beschrijft één onderhoudsmaatregel: welk bouwdeel, welke maatregel,
in welk jaar, voor welke kosten en met welke prioriteit.
"""

import frappe
from frappe.model.document import Document


class MjopRegel(Document):
    def validate(self) -> None:
        self._valideer_jaar()

    def _valideer_jaar(self) -> None:
        """Controleert dat het uitvoeringsjaar binnen de looptijd van het MJOP valt."""
        if not self.parent:
            return
        mjop = frappe.get_doc("Mjop", self.parent)
        if not (mjop.looptijd_start <= self.jaar <= mjop.looptijd_eind):
            frappe.throw(
                f"Jaar {self.jaar} valt buiten de MJOP-looptijd "
                f"({mjop.looptijd_start}–{mjop.looptijd_eind})."
            )
