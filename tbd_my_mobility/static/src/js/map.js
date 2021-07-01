odoo.define('tbd_my_mobility.maps', function (require) {

    var formrender = require("web.FormRenderer");
    var rpc = require('web.rpc')

    formrender.include({
        on_attach_callback: function () {
            this._super.apply(this, arguments);
            var self = this;
            var elements = $(".open_street_map_lot, .o_form_button_save");
            elements.on('click', function (evt) {
                if (open_maps.length > 0) {
                    _delete_map();
                }
                start_draw_map_project_project(self);
            });
        },
    })

    _delete_map = function () {
        open_maps.pop();
        $(".odoo_map_anchor").empty();
    }

    function start_draw_map_project_project(self) {
        rpc.query({
            model: 'project.project',
            method: 'search_read',
            fields: ['mymob_student', 'mymob_school'],
            domain: [['id', '=', self.state.data.id]],
        }).then(function (data) {
            if (!data[0].mymob_school || !data[0].mymob_student) {
                return false
            }
            list_id = data[0].mymob_school.concat(data[0].mymob_student)
            rpc.query({
                model: 'res.partner',
                method: 'search_read',
                fields: ['id', 'mymob_partner_type', 'name', 'mymob_school', 'partner_latitude', 'partner_longitude', 'contact_address_complete'],
                domain: [['id', 'in', list_id]]
            }).then(function (data_res_partner) {
                get_assigned_segment(self.state.data.id, data_res_partner)
            })
        })
    }

    function get_assigned_segment(lot_id, data_res_partner) {
        rpc.query({
            model: 'project.task',
            method: 'search_read',
            fields: ['mymob_student'],
            domain: [['project_id', '=', lot_id]],
        }).then(function (data_project_task) {
            let elements = document.querySelectorAll(".odoo_map_anchor");
            draw_openstreet_map(elements, 0, data_res_partner, data_project_task, get_barycentre(data_res_partner))
        })
    }

    function get_barycentre(data_res_partner) {
        var lat = []
        var lng = []
        for (i = 0; i < data_res_partner.length; i++) {
            lat.push(data_res_partner[i].partner_latitude)
            lng.push(data_res_partner[i].partner_longitude)
        }
        var barycentre = [(Math.max(...lng) + Math.min(...lng)) / 2.0, (Math.max(...lat) + Math.min(...lat)) / 2.0]
        return barycentre
    }

    function is_assigned_segment(id, data_project_task) {
        for (i = 0; i < data_project_task.length; i++) {
            if (data_project_task[i].mymob_student[0] == id) {
                return true
            }
        }
        return false
    }

    //
    function get_address_school_content(student, data_res_partner) {
        for (i = 0; i < data_res_partner.length; i++) {
            if (data_res_partner[i].id == student.mymob_school[0] && data_res_partner[i].mymob_partner_type == 'school') {
                return student.name + ',<br>' + data_res_partner[i].contact_address_complete
            }
        }
        return student.name
    }

    //
    function get_popup_address_school_content(data_res_partner, current) {
        if (current.mymob_partner_type == 'student') {
            if (current.mymob_school) {
                return get_address_school_content(current, data_res_partner)
            } else {
                return current.name
            }
        } else {
            return current.name + ',<br>' + current.contact_address_complete
        }
    }

    // Use for Open StreetMap
    function draw_openstreet_map(elements, i, data_res_partner, data_project_task, barycentre) {
        // Creation base openstreet map
        open_map = new ol.Map({
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM(),
                }),
            ],
            view: new ol.View({
                center: ol.proj.fromLonLat(barycentre),
                zoom: 6,
            }),
            // selector usr/tbd_my_mobility/views/project_project_view.xml:45
            target: "open_street_map_tbd",
        });

        let studentFeatures = [];
        let schoolFeatures = [];
        for (i = 0; i < data_res_partner.length; i++) {
            var icon = {};
            var point = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([data_res_partner[i].partner_longitude, data_res_partner[i].partner_latitude])),
                name: get_popup_address_school_content(data_res_partner, data_res_partner[i])
            });
            if (data_res_partner[i].mymob_partner_type == 'student') {
                if (is_assigned_segment(data_res_partner[i].id, data_project_task)) {
                    // Icon Verte
                    icon.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CgogPGc+CiAgPHRpdGxlPmJhY2tncm91bmQ8L3RpdGxlPgogIDxyZWN0IGZpbGw9Im5vbmUiIGlkPSJjYW52YXNfYmFja2dyb3VuZCIgaGVpZ2h0PSIyNiIgd2lkdGg9IjI2IiB5PSItMSIgeD0iLTEiLz4KIDwvZz4KIDxnPgogIDx0aXRsZT5MYXllciAxPC90aXRsZT4KICA8cGF0aCBzdHJva2U9Im51bGwiIGZpbGw9IiMzZjdmMDAiIGlkPSJzdmdfMiIgZD0ibTIxLjA3Nzc0LDkuMzMwMDc3YzAsLTUuMDI4MzU2IC00LjA0OTM4NCwtOS4wNzc3MzkgLTkuMDc3NzM5LC05LjA3NzczOWMtNS4wMjgzNTYsMCAtOS4wNzc3MzksNC4wNDkzODQgLTkuMDc3NzM5LDkuMDc3NzM5YzAsNS4wMjgzNTYgOS4wNzc3MzksMTQuNDE3NTg2IDkuMDc3NzM5LDE0LjQxNzU4NnM5LjA3NzczOSwtOS4zODkyMyA5LjA3NzczOSwtMTQuNDE3NTg2em0tMTMuMzA1MTE4LC0wLjE3Nzk5NWMwLC0yLjMxMzkzNCAxLjkxMzQ0NSwtNC4yMjczNzkgNC4yMjczNzksLTQuMjI3Mzc5YzIuMzEzOTM0LDAgNC4yMjczNzksMS44Njg5NDYgNC4yMjczNzksNC4yMjczNzljMCwyLjMxMzkzNCAtMS44Njg5NDYsNC4yMjczNzkgLTQuMjI3Mzc5LDQuMjI3Mzc5Yy0yLjMxMzkzNCwwIC00LjIyNzM3OSwtMS45MTM0NDUgLTQuMjI3Mzc5LC00LjIyNzM3OXoiLz4KIDwvZz4KPC9zdmc+';
                } else {
                    // Icon Rouge
                    icon.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CgogPGc+CiAgPHRpdGxlPmJhY2tncm91bmQ8L3RpdGxlPgogIDxyZWN0IGZpbGw9Im5vbmUiIGlkPSJjYW52YXNfYmFja2dyb3VuZCIgaGVpZ2h0PSIyNiIgd2lkdGg9IjI2IiB5PSItMSIgeD0iLTEiLz4KIDwvZz4KIDxnPgogIDx0aXRsZT5MYXllciAxPC90aXRsZT4KICA8cGF0aCBzdHJva2U9Im51bGwiIGZpbGw9IiNmZjAwMDAiIGlkPSJzdmdfMiIgZD0ibTIxLjA3Nzc0LDkuMzMwMDc3YzAsLTUuMDI4MzU2IC00LjA0OTM4NCwtOS4wNzc3MzkgLTkuMDc3NzM5LC05LjA3NzczOWMtNS4wMjgzNTYsMCAtOS4wNzc3MzksNC4wNDkzODQgLTkuMDc3NzM5LDkuMDc3NzM5YzAsNS4wMjgzNTYgOS4wNzc3MzksMTQuNDE3NTg2IDkuMDc3NzM5LDE0LjQxNzU4NnM5LjA3NzczOSwtOS4zODkyMyA5LjA3NzczOSwtMTQuNDE3NTg2em0tMTMuMzA1MTE4LC0wLjE3Nzk5NWMwLC0yLjMxMzkzNCAxLjkxMzQ0NSwtNC4yMjczNzkgNC4yMjczNzksLTQuMjI3Mzc5YzIuMzEzOTM0LDAgNC4yMjczNzksMS44Njg5NDYgNC4yMjczNzksNC4yMjczNzljMCwyLjMxMzkzNCAtMS44Njg5NDYsNC4yMjczNzkgLTQuMjI3Mzc5LDQuMjI3Mzc5Yy0yLjMxMzkzNCwwIC00LjIyNzM3OSwtMS45MTM0NDUgLTQuMjI3Mzc5LC00LjIyNzM3OXoiLz4KIDwvZz4KPC9zdmc+';
                }

                point.setStyle(new ol.style.Style({
                    image: new ol.style.Icon(icon)
                }));
                studentFeatures.push(point);
            } else {
                // Icon Bleu
                icon.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiA8dGl0bGUvPgoKIDxnPgogIDx0aXRsZT5iYWNrZ3JvdW5kPC90aXRsZT4KICA8cmVjdCBmaWxsPSJub25lIiBpZD0iY2FudmFzX2JhY2tncm91bmQiIGhlaWdodD0iNDAyIiB3aWR0aD0iNTgyIiB5PSItMSIgeD0iLTEiLz4KIDwvZz4KIDxnPgogIDx0aXRsZT5MYXllciAxPC90aXRsZT4KICA8cGF0aCBpZD0ic3ZnXzEiIGQ9Im0xMi41LDEzbC0xLDBhMSwxIDAgMCAwIDAsMmwxLDBhMSwxIDAgMCAwIDAsLTJ6Ii8+CiAgPHBhdGggaWQ9InN2Z18yIiBkPSJtMTIuNSw5bC0xLDBhMSwxIDAgMCAwIDAsMmwxLDBhMSwxIDAgMCAwIDAsLTJ6Ii8+CiAgPHBhdGggaWQ9InN2Z18zIiBkPSJtMTIuNSw1bC0xLDBhMSwxIDAgMCAwIDAsMmwxLDBhMSwxIDAgMCAwIDAsLTJ6Ii8+CiAgPHBhdGggaWQ9InN2Z180IiBkPSJtOC41LDEzbC0xLDBhMSwxIDAgMCAwIDAsMmwxLDBhMSwxIDAgMCAwIDAsLTJ6Ii8+CiAgPHBhdGggaWQ9InN2Z181IiBkPSJtOC41LDlsLTEsMGExLDEgMCAwIDAgMCwybDEsMGExLDEgMCAwIDAgMCwtMnoiLz4KICA8cGF0aCBpZD0ic3ZnXzYiIGQ9Im04LjUsNWwtMSwwYTEsMSAwIDAgMCAwLDJsMSwwYTEsMSAwIDAgMCAwLC0yeiIvPgogIDxwYXRoIGlkPSJzdmdfNyIgZD0ibTE2LjUsMTNsLTEsMGExLDEgMCAwIDAgMCwybDEsMGExLDEgMCAwIDAgMCwtMnoiLz4KICA8cGF0aCBpZD0ic3ZnXzgiIGQ9Im0xNi41LDlsLTEsMGExLDEgMCAwIDAgMCwybDEsMGExLDEgMCAwIDAgMCwtMnoiLz4KICA8cGF0aCBpZD0ic3ZnXzkiIGQ9Im0xNi41LDVsLTEsMGExLDEgMCAwIDAgMCwybDEsMGExLDEgMCAwIDAgMCwtMnoiLz4KICA8cGF0aCBzdHJva2U9Im51bGwiIGlkPSJzdmdfMTAiIGQ9Im0yMiwyMWwtMSwwbDAsLTE5YTEsMSAwIDAgMCAtMSwtMWwtMTYsMGExLDEgMCAwIDAgLTEsMWwwLDE5bC0xLDBhMSwxIDAgMCAwIDAsMmwyMCwwYTEsMSAwIDAgMCAwLC0yem0tMTIsMGwwLC0ybDQsMGwwLDJsLTQsMHptMTAsMGwwLC0zYTEsMSAwIDAgMCAtMSwtMWwtMTAsMGExLDEgMCAwIDAgLTEsMWwwLDNsLTMsMGwwLC0xOGwxNCwwbDAsMThsMSwweiIvPgogPC9nPgo8L3N2Zz4=';
                point.setStyle(new ol.style.Style({
                    image: new ol.style.Icon(icon),
                }));
                schoolFeatures.push(point);
            }
        }

        //--> Ajout des students
        let studentLayer = new ol.layer.Vector({
            title: 'Students',
            source: new ol.source.Vector({features: studentFeatures})
        });
        open_map.addLayer(studentLayer);

        //--> Ajout des schools
        let schoolLayer = new ol.layer.Vector({
            title: 'Schools',
            source: new ol.source.Vector({features: schoolFeatures})
        });
        open_map.addLayer(schoolLayer);

        // Gestion Popup
        var element = document.getElementById('popup_map_description');
        $(element).popover({
            animation: false,
            placement: 'top',
            html: true,
            content: "Undefined marker data"
        });

        var popup = new ol.Overlay({
            element: element,
            positioning: 'bottom-center',
            stopEvent: false,
            offset: [0, -10],
        });
        open_map.addOverlay(popup)
        // display popup on click
        open_map.on('click', function (evt) {
            var feature = open_map.forEachFeatureAtPixel(evt.pixel, function (feature) {
                return feature;
            });

            if (feature) {
                var coordinates = feature.getGeometry().getCoordinates();
                popup.setPosition(coordinates);

                $(element).data('bs.popover').config.content = feature.values_.name;

                $(element).popover('show');
            } else {
                $(element).popover('hide');
            }
        });
        // push map complete
        open_maps.push(open_map);
    }


    // Use for Google map
    function draw_google_map(elements, i, lat, lng) {
        map = new google.maps.Map(elements[i], {
            center: {lat: lat, lng: lng},
            zoom: 8,
        });
        return map;
    }

    function draw_google_marker(map, lat, lng) {
        var marker = new google.maps.Marker({
            position: {lat: lat, lng: lng},
            map: map,
        });
    }

    // let elements = document.querySelectorAll(".demo");
    // let google_maps = draw_google_map(elements, 0, 48.866667, 2.333333)
    // let open_map = draw_openstreet_map(elements, 0, data)
    // for (let i = 0; i < data.length; i++) {
    // draw_google_marker(google_maps, data[i].partner_latitude, data[i].partner_longitude)
    // draw_openstreet_marker(open_map, data[i].partner_latitude, data[i].partner_longitude)
    // }
})
