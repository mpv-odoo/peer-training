# -*- coding:utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
   _inherit = 'product.template'

   pairs_per_case = fields.Integer(
      string='Number of shoe pairs per case'
   )
   price_per_pair = fields.Float(
      string='Price per pair of shoes'
   )
   '''
   list_price already exists in product.template, 
   but I am changing it so that it can be computed
   '''
   list_price = fields.Float(
      string='Sales Price',
      compute='_compute_sales_price',
      inverse='_inverse_sales_price',
      readonly= False
   )

   @api.depends('pairs_per_case', 'price_per_pair')
   def _compute_sales_price(self):
      for product in self:
         product.list_price = product.price_per_pair * product.pairs_per_case

   '''
   Since list_price is read only whenever price_per_pair
   or pairs_per_price is > 0, there is no need to have 
   the inverse function actually do any calculations
   '''
   def _inverse_sales_price(self):
      pass

   '''
   Make sure that the number of pairs is positive
   '''
   @api.onchange('pairs_per_case')
   def _onchange_verify_pairs(self):
      if self.pairs_per_case < 0:
         self.price_per_pair = self._origin.pairs_per_case
         raise UserError('Number of shoe pairs cannot be negative')

   '''
   Make sure that the price per pair is positive
   '''
   @api.onchange('price_per_pair')
   def _onchange_verify_price(self):
      if self.price_per_pair < 0:
         self.price_per_pair = self._origin.price_per_pair
         raise UserError('Price per pair cannot be negative')

