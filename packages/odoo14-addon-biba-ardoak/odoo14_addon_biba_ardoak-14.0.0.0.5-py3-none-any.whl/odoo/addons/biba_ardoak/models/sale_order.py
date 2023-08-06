from odoo import models
from odoo.tools import float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _check_package(self):
        default_uom = self.product_id.uom_id
        pack = self.product_packaging
        qty = self.product_uom_qty
        q = default_uom._compute_quantity(pack.qty, self.product_uom)
        # We do not use the modulo operator to check if qty is a
        # mltiple of q. Indeed the quantity
        # per package might be a float, leading to incorrect results.
        # For example:
        # 8 % 1.6 = 1.5999999999999996
        # 5.4 % 1.8 = 2.220446049250313e-16
        if (
            qty
            and q
            and float_compare(
                qty / q,
                float_round(qty / q, precision_rounding=1.0),
                precision_rounding=0.001,
            )
            != 0
        ):
            newqty = qty - (qty % q) + q
            self.product_uom_qty = newqty
        return {}
