# See LICENSE file for full copyright and licensing details.

import calendar
import re

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.translate import _


class TransportDepartures(models.Model):
    """Define the departure schedule"""

    _name = "transport.departure"
    _description = "Transport Departure"
    _order = "date_exp_departure"

    container_id = fields.Many2one(
        "transport.truck",
        "Container",
        help="""The planned container for this departure""",
    )
    urgent_part = fields.Boolean(
        "Urgent part ?",
        help="Is the truck will transport some urgent part ?",
    )
    fdp_id = fields.Many2one(
        "transport.fdp",
        "Final Destination",
        required=True,
        help="The final delivery point",
    )
    date_exp_departure = fields.Date(
        "Expected Departure Date", required=True, help="Expected Date of departure"
    )
    date_departure = fields.Date(
        "Departure Date", help="The real Departure Date"
    )
    status = fields.Selection([('draft', 'Draft'), ('planned', 'Planned')
                                  , ('on_site', 'On site')
                                  , ('loading', 'Loading...'), ('departed', 'Departed')
                                  , ('departed_issue', 'Departed with remark')
                                  , ('cancelled', 'Cancelled'), ('delay', 'Delay')]
                              , required=True,
                              readonly=True, copy=False,
                              tracking=True, default='draft',
                              help="Status")

    def name_get(self):
        return [(rec.id, rec.container_id.container_plate + " / " + rec.fdp_id.name) for rec in self]
