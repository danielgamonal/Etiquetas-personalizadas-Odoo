# @author: Daniel Gamonal (daniel.gamonal@frindtsa.cl)
# @author: Esteban Almonacid (esteban.almonacid@gfrindtsa.cl)

from odoo import api, fields, models, _
from odoo.exceptions import UserError


# transientmodel es un modelo de tabla usada para elementos temporales
class PrintProductLabel(models.TransientModel):
    # Nombre del Modelo Temporal
    _name = "print.product.label"
    _description = 'Wizard para Imprimir Etiquetas'

    # metodo para conseguir datos de la tabla para uso temporal
    @api.model
    def _get_products(self):
        res = []
        if self._context.get('active_model') == 'product.template':
            products = self.env[self._context.get('active_model')].browse(
                self._context.get('default_product_ids'))
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.product_variant_id.id,
                })
        elif self._context.get('active_model') == 'product.product':
            products = self.env[self._context.get('active_model')].browse(
                self._context.get('default_products_id'))
            for product in products:
                label = self.env['print.product.label.line'].create({
                    'product_id': product.id,
                })
                res.append(label.id)
        return res

   # productos/nombre_producto/Imprimir Etiquetas de Producto
    name = fields.Char(
        'Nombre',
        default='Imprimir Etiquetas de Producto'
    )

    # mensaje
    message = fields.Char(
        'Mensaje',
        readonly=True,
    )

    # check de formato salida a PDF
    output = fields.Selection(
        selection=[('pdf', 'PDF')],
        string="Imprimir a ",
        default='pdf',
    )

    # abrir:Etiquetas para Productos
    label_ids = fields.One2many(
        comodel_name='print.product.label.line',
        inverse_name='wizard_id',
        string='Etiquetas Para Productos',
        default=_get_products,
    )

    # Plantilla de Etiqueta
    template = fields.Selection(
        selection=[
        ('frindtsa_product_label.report_product_label_A4_57x35','Etiqueta Amarilla'),
        ('frindtsa_product_label.report_product_label_30x30','Etiqueta Blanca sin Precio')
        ],
        string='Plantilla de Etiqueta',
        default='frindtsa_product_label.report_product_label_A4_57x35',
    )

    # cantidad de etiquetas por Producto
    qty_per_product = fields.Integer(
        string='Cantidad de Etiquetas por Producto',
        default=1
    )

    # opciones
    humanreadable = fields.Boolean(
        string='Imprimir codigo digital de codigo de Barras',
        default=False
    )
    withoutprice = fields.Boolean(
        string='No Imprimir Precio',
        default=False
    )

    # accion Imprimir
    def action_print(self):
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise UserError(
                _('Nada para impimir, Ingrese la cantidad de Etiquetas'))
        return self.env.ref(self.template).with_context(discard_logo_check=True).report_action(labels)
    
    #vista previa
    def action_preview(self):
        self.ensure_one()
        labels = self.label_ids.filtered('selected').mapped('id')
        if not labels:
            raise UserError(_('Seleccione Etiquetas para conseguir una vista previa'))
        return self.env.ref('%s_preview' % self.template).with_context(
            discard_logo_check=True).report_action(labels)
    
    #establecer Cantidad
    def action_set_qty(self):
        self.ensure_one()
        self.label_ids.write({'Cant': self.qty_per_product})

    #Restaurar Cantidad Inicial
    def action_restore_initial_qty(self):
        self.ensure_one()
        for label in self.label_ids:
            if label.qty_initial:
                label.update({'Cant': label.qty_initial})