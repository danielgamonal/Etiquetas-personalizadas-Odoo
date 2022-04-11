# @author: Daniel Gamonal (daniel.gamonal@frindtsa.cl)
# @author: Esteban Almonacid (esteban.almonacid@gfrindtsa.cl)

from odoo import api, fields, models

class PrintProductLabelLine(models.TransientModel):
    _name="print.product.label.line"
    _description= 'linea con datos de la etiqueta de producto'

    selected = fields.Boolean(
        string='Print',
        compute='_compute_selected',
        readonly=True,
    )
    wizard_id = fields.Many2one('print.product.label', 'Print Wizard')
    product_id =fields.Many2one('product.product', 'Producto', required= True)
    barcode = fields.Char('Codigo de Barras', related='product_id.barcode')
    qty_initial = fields.Integer('Cantidad inicial', default=1)
    qty= fields.Integer('Cantidad de Etiquetas', default=1)

    #condicional immprimir etiquetas seleccionadas
    @api.depends('qty')
    def _compute_selected(self):
        for record in self:
            if record.qty > 0:
                record.update({'selected': True})
            else:
                record.update({'selected': False})
    
    #aumentar cantidad
    def action_plus_qty(self):
        for record in self:
            record.update({'qty': record.qty + 1})
    
    #reducir cantidad
    def action_minus_qty(self):
        for record in self:
            if record.qty > 0:
                record.update({'qty': record.qty - 1})