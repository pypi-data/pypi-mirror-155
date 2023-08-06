from odoo import fields, models, api, _

class SubscriptionRequest(models.Model):

    _inherit = ["subscription.request"]

    gender = fields.Selection(
        [
            ("male", _("Male")),
            ("female", _("Female")),
            ("other", _("Other")),
            ("no_answer", _("No answer"))
        ],
        string="Gender",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    discovery_channel = fields.Selection(
        [
            ('boca', _('Boca-orella')),
            ('fulleto', _('Fulletó')),
            ('radio', _('Ràdio')),
            ('tv', _('TV')),
            ('premsa', _('Premsa')),
            ('xarxes', _('Xarxes socials')),
            ('web', _('WEB')),
            ('buscador', _('Buscador d’internet')),
            ('socia', _('Sòcia ecoopirativa/estrella')),
            ('altres', _('Altres'))
        ],
        help = 'How people find us.',
        string = 'Discovery channel',
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    newsletter_approved = fields.Boolean(
        string='Newsletter approved',
        default=False,
    )
    sepa_approved = fields.Boolean(
        string='SEPA approved',
        required=True,
        default=False,
    )
    ref = fields.Char(string='Internal Reference', index=True)

    def get_partner_vals(self):
        partner_vals = super().get_partner_vals()
        partner_vals['ref'] = self.ref
        return partner_vals

    def get_invoice_vals(self, partner):
        vals = super().get_invoice_vals(partner)
        usense = self.env['operating.unit'].search([('code','=','USense')])
        vals['operating_unit_id'] = usense.id
        return vals

    @api.multi
    def validate_subscription_request(self):
        invoice = super().validate_subscription_request()
        if self.ref:
            self.partner_id.ref = self.ref
        return invoice
