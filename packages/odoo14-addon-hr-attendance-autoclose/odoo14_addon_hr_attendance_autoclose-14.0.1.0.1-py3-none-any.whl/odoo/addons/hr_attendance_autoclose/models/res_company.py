# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    attendance_maximum_hours_per_day = fields.Float(
        string="Attendance Maximum Hours Per Day", digits=(2, 2), default=11.0
    )
