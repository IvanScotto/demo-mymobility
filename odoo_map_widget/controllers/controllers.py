# -*- coding: utf-8 -*-
from odoo import http,tools,api, _
from odoo.http import request
import logging 
_logger = logging.getLogger(__name__)

class WkMapWidget(http.Controller):
    @http.route(['/get/map/template'], type='http', auth="public", website=True, sitemap=False)
    def get_map_template(self, **post):
        name = post.get("name",False)
        lat = post.get("lat",False)
        _long = post.get("lng",False)
        field_lat = post.get("field_lat",False)
        field_lng = post.get("field_lng",False)
        script_loaded = post.get("script_loaded",False)
        provider_id = request.env['ir.config_parameter'].sudo().get_param('base_geolocalize.geo_provider')
        provider = request.env['base.geo_provider'].browse(int(provider_id))
        
        try:
            vals = {'name':name,"script_loaded":script_loaded,"lat":lat,"lng":_long,"field_lat":field_lat,"field_lng":field_lng}
            if provider.tech_name == 'openstreetmap':
                return request.render("odoo_map_widget.wk_openstreet_map",vals)

            return request.render("odoo_map_widget.wk_google_map",vals)
        except Exception as e:
            _logger.info("error %r",e)
    
    @http.route(['/get/map/location'], type='http', auth="public", website=True, sitemap=False)
    def get_form_map_tempalte(self, **post):
        record_id = post.get("active_id",False)
        model_name = post.get("model_name",False)
        provider_id = request.env['ir.config_parameter'].sudo().get_param('base_geolocalize.geo_provider')
        provider = request.env['base.geo_provider'].browse(int(provider_id))

        try:
            search_domain = [('model_name','=',model_name),('is_active','=',True)]
            location_data = request.env["map_widget.map_widget"].search(search_domain,limit=1)
            map_data = location_data.map_id.filtered(lambda map_id: map_id.record_id == int(record_id))
            vals = {'location_data':location_data,"map_data":map_data,"is_active":location_data.is_active,"record_id":record_id,"model_name":model_name}
            
            if provider.tech_name == 'openstreetmap':
                return request.render("odoo_map_widget.openstreet_map",vals)
                
            return request.render("odoo_map_widget.google_map_widget",vals)
        except Exception as e:
            _logger.info("error %r",e)
    
    @http.route(['/get/map/notebook'], type='http', auth="public", website=True, sitemap=False)
    def get_form_map_tempalte_with_notebook(self, **post):
        record_id = post.get("active_id",False)
        model_name = post.get("model_name",False)
        provider_id = request.env['ir.config_parameter'].sudo().get_param('base_geolocalize.geo_provider')
        provider = request.env['base.geo_provider'].browse(int(provider_id))

        try:
            search_domain = [('model_name','=',model_name),('is_active','=',True)]
            location_data = request.env["map_widget.map_widget"].search(search_domain,limit=1)
            map_data = location_data.map_id.filtered(lambda map_id: map_id.record_id == int(record_id))
            vals = {'location_data':location_data,"map_data":map_data,"is_active":location_data.is_active,"record_id":record_id,"model_name":model_name}
            if provider.tech_name == 'openstreetmap':
                return request.render("odoo_map_widget.openstreet_map_with_notebook",vals)
                
            return request.render("odoo_map_widget.google_map_widget_with_notebook",vals)
        except Exception as e:
            _logger.info("error %r",e)
