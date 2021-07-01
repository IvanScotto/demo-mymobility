let open_map;
let open_maps = [];
odoo.define("odoo_map_widget.form_map", function (require) {
  "use strict";

  var formrender = require("web.FormRenderer");
  var ajax = require("web.ajax");
  var mvc = require("web.mvc");
  var Renderer = mvc.Renderer;
  var draw_openstreet_map = function (elements, i, lat, lng, record_id) {
    open_map = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM(),
        }),
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([lng, lat]),
        zoom: 6,
      }),
      target: "open_street_map_" + record_id,
    });

    var layer = new ol.layer.Vector({
      source: new ol.source.Vector({
        features: [
          new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([lng, lat])),
          }),
        ],
      }),
    });
    open_map.addLayer(layer);
    open_maps.push(open_map);
  };

  var render_openstreet_map = function () {
    let elements = document.querySelectorAll(".demo");
    for (let i = 0; i < elements.length; i++) {
      let record_id = elements[i].parentNode.getAttribute("data-record-id");

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
        let record_name = elements[i].getAttribute("data-field-name");
        draw_openstreet_map(elements, i, lat, lng, record_name);
      } else {
        draw_openstreet_map(elements, i, lat, lng, record_id);
      }
    }
  };

  formrender.include({
    events: _.extend({}, Renderer.prototype.events, {
      "click .js_delete_map": "_deleteMap",
      "click .js_add_map": "_addMap",
      "click .js_edit_map": "_editMap",
      "mouseover .o_form_sheet": "_activateMap",
      "click .map_btn_class": "_createPin",
    }),

    _createPin: function (ev) {
      var link = window.location.href;
      var link = link.replace(/#/g, "&");
      var data = _.object(
        link.split("&").map(function (p) {
          return p.split("=");
        })
      );
      var active_id = parseInt(data["id"]);
      var model_name = data["model"];
      var self = this;
      var context = { active_id: active_id, model_name: model_name };

      var is_active = $(ev.currentTarget).hasClass("text-success");

      if (!is_active) {
        if (!isNaN(active_id) && model_name.length != 0) {
          self
            ._rpc({
              model: "map_widget.map_widget",
              method: "create_map_container",
              args: [[], context],
              additional_context: {
                wk_active_id: active_id,
                model_name: model_name,
              },
            })
            .then(function () {
              window.location.reload();
              self.displayNotification({
                title: "Map Added",
                message: "The map has been added",
                sticky: true,
              });
            });
        }
      } else {
        self
          ._rpc({
            model: "map_widget.map_widget",
            method: "remove_map_container",
            args: [[], context],
          })
          .then(function () {
            window.location.reload();
          });
      }
    },

    _renderMapButton: function () {
      if ($(".map_btn_class").length == 0) {
        var button =
          "<div class='btn-group o_dropdown'><button name='map_btn' class='btn map_btn_class' title='Pin a new location'><i class='fa fa-map-marker' /></button></div>";
        $(".o_cp_action_menus .btn-group:first-child").before($(button));
      }

      if ($(".map_area .map_group").length > 0) {
        $(".map_btn_class").addClass("text-success");
      }
    },

    on_attach_callback: function () {
      this._super.apply(this, arguments);
      var self = this;
      self._renderMapButton();
      $(document).ready(function () {
        $(document).on("click", ".map_btn_class", function (ev) {
          self._createPin(ev);
        });
      });
      try {
        render_openstreet_map();
      } catch (e) {
        console.log(e);
      }
      if ($(".map_area .map_group").length > 0) {
        $(".map_btn_class").addClass("text-success");
      }
    },

    _activateMap: function (ev) {
      if ($(".open_street_map").length != 0) {
        let map_record;
        for (map_record of open_maps) {
          map_record.updateSize();
        }
      }
    },

    _addMap: function (ev) {
      var map_el = $(ev.currentTarget).closest(".map_group");
      var active_id = map_el.data("model-id");
      var model_name = map_el.data("model");

      var context = { active_id: active_id, model_name: model_name };

      this._rpc({
        model: "maps.maps",
        method: "create_map_data",
        args: [[], context],
      }).then(function () {
        window.location.reload();
      });
    },

    _editMap: function (ev) {
      var map_el = $(ev.currentTarget).closest(".map_group");
      var active_id = map_el.data("model-id");
      var model_name = map_el.data("model");

      this.do_action(
        {
          type: "ir.actions.act_window",
          res_model: "maps.maps",
          res_id: parseInt(map_el.data("record-id"), 10),
          views: [[false, "form"]],
          target: "new",
          context: {
            form_view_ref: "odoo_map_widget.wk_map_data_form_view",
            wk_active_id: active_id,
            model_name: model_name,
          },
        },
        {
          on_close: function () {
            window.location.reload();
          },
        }
      );
    },

    _deleteMap: function (ev) {
      var self = this;
      var map_el = $(ev.currentTarget).closest(".map_group");
      var answer = window.confirm("Are you sure want to delete record");
      if (answer) {
        self
          ._rpc({
            model: "maps.maps",
            method: "unlink",
            args: [parseInt(map_el.data("record-id"), 10)],
          })
          .then(function () {
            self.displayNotification({
              title: "Map Deleted",
              message: "The map has been deleted",
              sticky: true,
            });
            map_el.remove();
            if ($(".map_area .map_group").length == 0) {
              window.location.reload();
            }
          });
      }
    },

    _updateView: function ($newContent) {
      var self = this;
      self._super.apply(this, arguments);
      self._renderMapButton();
      try {
        render_openstreet_map();
      } catch (e) {
        console.log(e);
      }
    },

    _renderView: function () {
      var self = this;
      var vals = {};
      var active_id = false;
      var model = false;

      if (!isNaN(self.state.res_id)) {
        active_id = self.state.res_id;
        model = self.state.model;
      }

      if (!isNaN(self.state.context.wk_active_id)) {
        active_id = self.state.context.wk_active_id;
        model = self.state.context.model_name;
      }

      vals = { active_id: active_id, model_name: model };

      // render the form and evaluate the modifiers
      var defs = [];
      this.defs = defs;
      this.inactiveNotebooks = [];
      var $form = this._renderNode(this.arch).addClass(this.className);
      delete this.defs;

      var sticky = new Promise(function (resolve, reject) {
        if ($form.find(".o_notebook").length != 0) {
          $.get("/get/map/location", vals).then(function (data) {
            self.sticky_data = data;
            resolve(self.sticky_data);
          });
        } else {
          $.get("/get/map/notebook", vals).then(function (data) {
            self.sticky_data = data;
            resolve(self.sticky_data);
          });
        }
      });
      defs.push(sticky);

      return Promise.all(defs)
        .then(function () {
          if (!$($form.contents()[0]).hasClass("o_group")) {
            if (
              $form.find(".o_notebook").length != 0 &&
              $(self.sticky_data).find(".map_group").length != 0
            ) {
              var nav_btn =
                "<li class='nav-item'><a data-toggle='tab' disable_anchor='true' href='#gmap_widget_pane' class='nav-link' role='tab' aria-selected='false'>Maps</a></li>";
              $form.find(".o_notebook .nav-tabs").append($(nav_btn));
              $form.find(".o_notebook .tab-content").append(self.sticky_data);
            } else {
              if ($(self.sticky_data).find(".map_group").length != 0) {
                $form
                  .find(".o_form_sheet>div:last-child")
                  .append(self.sticky_data);
              }
            }
          }

          self._updateView($form.contents());
          if (self.state.res_id in self.alertFields) {
            self.displayTranslationAlert();
          }
        })
        .then(function () {
          if (self.lastActivatedFieldIndex >= 0) {
            self._activateNextFieldWidget(
              self.state,
              self.lastActivatedFieldIndex
            );
          }
        })
        .guardedCatch(function () {
          $form.remove();
        });
    },
  });
});
