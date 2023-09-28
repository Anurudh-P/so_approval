# -*- coding: utf-8 -*-
from odoo import models, fields


class WarningWizard(models.TransientModel):
    """model for adding warning message """

    _name = 'warning.message.wizard'
    _description = "Show Message"

    message = fields.Text('Warning', required=True)

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}
