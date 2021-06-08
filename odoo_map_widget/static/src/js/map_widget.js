let map;

function draw_map(elements, i, lat, lng) {
  map = new google.maps.Map(elements[i], {
    center: { lat: lat, lng: lng },
    zoom: 8,
  });
  var marker = new google.maps.Marker({
    position: { lat: lat, lng: lng },
    map: map,
  });

  return true;
}

function initMap() {
  let elements = document.querySelectorAll(".demo");
  for (i = 0; i < elements.length; i++) {
    // populated when called from marker pin
    var lat = parseFloat(elements[i].getAttribute("data-lat"));
    var lng = parseFloat(elements[i].getAttribute("data-lng"));

    // populated when called from widget
    var field_lat = elements[i].getAttribute("data-field-lat");
    var field_lng = elements[i].getAttribute("data-field-lng");

    if (field_lat != null && field_lng != null) {
      if ($("input[name=" + field_lat + "]").val()) {
        lat = parseFloat($("input[name=" + field_lat + "]").val());
      } else {
        if ($("span[name=" + field_lat + "]").text()) {
          lat = parseFloat($("span[name=" + field_lat + "]").text());
        } else {
          lat = 0.0;
        }
      }
      if ($("input[name=" + field_lng + "]").val()) {
        lng = parseFloat($("input[name=" + field_lng + "]").val());
      } else {
        if ($("span[name=" + field_lng + "]").text()) {
          lng = parseFloat($("span[name=" + field_lng + "]").text());
        } else {
          lng = 0.0;
        }
      }
      draw_map(elements, i, lat, lng);
    } else {
      draw_map(elements, i, lat, lng);
    }
  }
}

odoo.define("wk_gmap_widget.widget", function (require) {
  "use strict";

  var core = require("web.core");
  var field_registry = require("web.field_registry");
  var AbstractField = require("web.AbstractField");
  let script_loaded = false;

  var _t = core._t;

  var GmapFieldWidget = AbstractField.extend({
    className: "gmap_field",

    _LoadMap: function () {
      var self = this;
      var defs = [];
      if (window.google && window.google.maps) {
        script_loaded = true;
      }

      //--extracting lat and long from field---
      var vals = {
        field_lat: self.attrs.lat,
        field_lng: self.attrs.lng,
        name: self.attrs.name,
        script_loaded: script_loaded,
        lat: self.attrs.latitude,
        lng: self.attrs.longitude,
      };
      name = self.attrs.name;
      //--------------------------------

      //----getting map template-----------------
      var map = new Promise(function (resolve, reject) {
        $.get("/get/map/template", vals).then(function (data) {
          self.map_data = data;
          resolve(self.map_data);
        });
      });
      //-----------------------------------------------------

      defs.push(map);

      //---------------ensuring map will load first before rendering form view---------
      return Promise.all(defs).then(function () {
        self.$el.append(self.map_data);
      });
      //---------------------------------------------------------------------------------
    },

    _render: function () {
      var self = this;
      var _super = this._super.bind(this);
      return new Promise(function (resolve, reject) {
        resolve(self._LoadMap());
      }).then(function () {
        return _super.apply(self, arguments);
      });
    },
  });

  field_registry.add("gmap_widget", GmapFieldWidget);
});
