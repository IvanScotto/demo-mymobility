# -*- coding: utf-8 -*-

class BaseMymobilityMixin(models.AbstractModel):
    _name = 'base.mymobility.mixin'
    _description = "Mymobility base model mixin"

    mymob_update_api_date = fields.Datetime('Date de mise à jour via API')