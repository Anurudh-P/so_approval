# -*- coding: utf-8 -*-
from odoo import models, fields, _


class SaleOrder(models.Model):
    """model for adding merge order line function """
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'To approve'), ("sent",)])
    is_approved = fields.Boolean(default=False)

    def action_confirm(self):
        """when clicking the confirm button satisfy the condition of
        price therefore supered the action confirm """

        if self.is_approved == False:
            for line in self.order_line:
                if line.price_unit != line.product_id.lst_price:
                    if self.env.user.has_group('so_approval.group_sale_manager'):
                        super().action_confirm()

                    else:
                        # self.is_bool = True
                        self.state = 'to_approve'
                        message_id = self.env['warning.message.wizard'].create(
                            {'message': 'Please take approval from manager'})
                        return {
                            'name': 'Message',
                            'type': 'ir.actions.act_window',
                            'view_mode': 'form',
                            'res_model': 'warning.message.wizard',
                            'res_id': message_id.id,
                            'target': 'new'
                        }
                else:
                    super().action_confirm()
        else:
            super().action_confirm()

    def action_disapprove(self):
        """when clicking the button disapprove the
         state will change to draft"""
        self.state = 'draft'
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Warning'),
                'type': 'warning',
                'message': 'You rejected this sale order',
                'sticky': True,
            }
        }
        return notification


class MailComposeMessage(models.TransientModel):
    """the model mail compose message is inherited for sending the mail
      to the customer and changing the state"""
    _inherit = 'mail.compose.message'

    def _action_send_mail(self, auto_commit=False):
        active_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse([active_id])
        if sale_order.state == 'to_approve':
            sale_order.state = 'sent'
            sale_order.is_approved = True
        return super(MailComposeMessage, self)._action_send_mail(auto_commit=auto_commit)
