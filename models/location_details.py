# -*- coding: utf-8 -*-

from openerp import models, fields, api

class location_details(models.Model):
    _inherit = 'stock.location'

    truck_reception = fields.One2many('truck.reception','location_id')
    truck_outlet = fields.One2many('truck.outlet','location_id')
    wagon_outlet = fields.One2many('wagon.outlet','location_id')
    truck_internal = fields.One2many('truck.internal','location_dest_id')

    total_tons_reception = fields.Float(compute="_compute_total_reception", store=False, readonly=True)
    total_tons_outlet = fields.Float(compute="_compute_total_outlet", store=False, readonly=True)
    total_tons_available = fields.Float(compute="_compute_total_available", store=False, readonly=True)

    percentage_quality_reception = fields.Float(compute="_compute_quality_reception", store=False, readonly=True) #humedad
    percentage_quality_damaged = fields.Float(compute="_compute_quality_damaged", store=False, readonly=True)
    percentage_quality_impurity = fields.Float(compute="_compute_quality_impurity", store=False, readonly=True)
    percentage_quality_break = fields.Float(compute="_compute_quality_break", store=False, readonly=True)

    wet_kilos_discount = fields.Float(compute="_compute_wet_kilos", store=False, readonly=True)   
    damaged_kilos_discount = fields.Float(compute="_compute_damaged_kilos", store=False, readonly=True)
    impure_kilos_discount = fields.Float(compute="_compute_impure_kilos", store=False, readonly=True)
    broken_kilos_discount = fields.Float(compute="_compute_broken_kilos", store=False, readonly=True)

    @api.one
    @api.depends('truck_reception')
    def _compute_total_reception(self):
        if len(self.truck_reception) > 0:
            tons = 0
            for record in self.truck_reception:
                tons += record.clean_kilos
            self.total_tons_reception = tons / 1000
        else:
            self.total_tons_reception = 0    

    @api.one
    @api.depends('truck_outlet','wagon_outlet')
    def _compute_total_outlet(self):
        if len(self.truck_outlet) > 0 or len(self.wagon_outlet) > 0:
            tons_truck = 0
            tons_wagon = 0
            for record in self.truck_outlet:
                tons_truck += record.raw_kilos
            for record in self.wagon_outlet:
                tons_wagon += record.raw_kilos
            self.total_tons_outlet = (tons_truck + tons_wagon) / 1000
        else:
            self.total_tons_outlet = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_quality_reception(self):
        if len(self.truck_reception) > 0:
            quantity = len(self.truck_reception)
            total_quality = 0
            for record in self.truck_reception:
                total_quality += record.humidity_rate
            self.percentage_quality_reception = float(total_quality / quantity)
        else:
            self.percentage_quality_reception = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_wet_kilos(self):
        if len(self.truck_reception) > 0:
            tons = 0
            for record in self.truck_reception:
                tons += record.humid_kilos
            self.wet_kilos_discount = tons / 1000
        else:
            self.wet_kilos_discount = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_damaged_kilos(self):
        if len(self.truck_reception) > 0:
            tons = 0
            for record in self.truck_reception:
                tons += record.damaged_kilos
            self.damaged_kilos_discount = tons / 1000
        else:
            self.damaged_kilos_discount = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_impure_kilos(self):
        if len(self.truck_reception) > 0:
            tons = 0
            for record in self.truck_reception:
                tons += record.impure_kilos
            self.impure_kilos_discount = tons / 1000
        else:
            self.impure_kilos_discount = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_broken_kilos(self):
        if len(self.truck_reception) > 0:
            tons = 0
            for record in self.truck_reception:
                tons += record.broken_kilos
            self.broken_kilos_discount = tons / 1000
        else:
            self.broken_kilos_discount = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_quality_damaged(self):
        if len(self.truck_reception) > 0:
            quantity = len(self.truck_reception)
            total_quality = 0
            for record in self.truck_reception:
                total_quality += record.damage_rate
            self.percentage_quality_damaged = float(total_quality / quantity)
        else:
            self.percentage_quality_damaged = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_quality_impurity(self):
        if len(self.truck_reception) > 0:
            quantity = len(self.truck_reception)
            total_quality = 0
            for record in self.truck_reception:
                total_quality += record.impurity_rate
            self.percentage_quality_impurity = float(total_quality / quantity)
        else:
            self.percentage_quality_impurity = 0

    @api.one
    @api.depends('truck_reception')
    def _compute_quality_break(self):
        if len(self.truck_reception) > 0:
            quantity = len(self.truck_reception)
            total_quality = 0
            for record in self.truck_reception:
                total_quality += record.break_rate
            self.percentage_quality_break = float(total_quality / quantity)
        else:
            self.percentage_quality_break = 0

    @api.one
    @api.depends('total_tons_reception','total_tons_outlet')
    def _compute_total_available(self):
        self.total_tons_available = self.total_tons_reception - self.total_tons_outlet
