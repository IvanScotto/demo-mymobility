# -*- coding: utf-8 -*-

class BaseMymobility(models.AbstractModel):
    _name = 'base.mymobility'
    _description = "Mymobility base model"

    mymob_update_api_date = fields.Datetime('Date de mise à jour via API')