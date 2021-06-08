# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class MapsMaps(models.Model):
    _name = 'maps.maps'
    
    longitude = fields.Float("Longitude",default="77.352671")
    latitude = fields.Float("Latitude",default="28.639579")
    record_id = fields.Integer("Record Id")

    def create_map_data(self,*args):
        record_id = args[0].get('active_id')
        model_name = args[0].get('model_name')
        map_vals = {'latitude':0.0,'longitude':0.0,'record_id':int(record_id)}
        map_record = self.env["map_widget.map_widget"].search([('model_name','=',model_name)],limit=1)#('record_id','=',int(record_id)),
        maps_data = self.env['maps.maps'].with_context(pin_location=True).create(map_vals)
        if map_record and maps_data:
            map_record.map_id = [(6,0,maps_data.ids+map_record.map_id.ids)]

        return True

    @api.model
    def create(self,vals):
        record_id = self._context.get("wk_active_id",False)
        call_from_js = self._context.get("pin_location",False)
        if not call_from_js:
            vals.update({"record_id":record_id})
        
        if record_id or call_from_js:
            res = super(MapsMaps,self).create(vals)
            return res
        
        else:
            raise UserError(_("There is error in storing map location due to invalid record id"))



class WkMapWidget(models.Model):
    _name = 'map_widget.map_widget'

    longitude = fields.Float("Longitude",default="0")
    latitude = fields.Float("Latitude",default="0")
    record_id = fields.Integer("Record Id") #to remove
    map_id = fields.Many2many(comodel_name="maps.maps",string="Map Id")
    model_name = fields.Char("Model Name")
    is_active = fields.Boolean("Active")

    def remove_map_container(self,*args):
        model_name = args[0].get('model_name')
        map_id = self.env["map_widget.map_widget"].search([('model_name','=',model_name)],limit=1)#('record_id','=',int(record_id)),
        map_id.is_active = False
        return True  
        

    def create_map_container(self,*args):
        record_id = args[0].get('active_id')
        model_name = args[0].get('model_name')

        map_id = self.env["map_widget.map_widget"].search([('model_name','=',model_name)],limit=1)#('record_id','=',int(record_id)),

        if map_id:
            map_id.is_active = True
        else:
            map_vals = {'latitude':0.0,'longitude':0.0,'record_id':int(record_id)}
            maps_data = self.env['maps.maps'].with_context(pin_location=True).create(map_vals)
            vals = {'latitude':0.0,'longitude':0.0,'record_id':int(record_id),'model_name':model_name,"is_active":True}
            if record_id and model_name:
                widget_record = self.env['map_widget.map_widget'].with_context(pin_location=True).create(vals)
                widget_record.map_id = [(6,0,maps_data.ids)]
        return True

    @api.model
    def create(self,vals):
        model_name = self._context.get("model_name",False)
        record_id = self._context.get("wk_active_id",False)
        call_from_js = self._context.get("pin_location",False)

        if not call_from_js:
            vals.update({"model_name":model_name,"record_id":record_id})
        
        if model_name and record_id or call_from_js:
            res = super(WkMapWidget,self).create(vals)
            return res
        
        else:
            raise UserError(_("There is error in storing map location due to invalid record id"))
