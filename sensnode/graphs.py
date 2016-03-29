#!/usr/bin/python2
# -*- coding: utf-8 -*-
import store
import logging
import logs
import jsontree
from datetime import datetime
from config import config
import numpy as np
from bokeh.plotting import *
from bokeh.embed import components

"""
__TODO__:
- generowanie obrazu png HQ lub kodu HTML+JS
- Schemat nazwy generowanego obrazu:
    * odzielnie na kazdy sensor
        _node_-_sensor_-_period_.png
        np:.
            outnode-temp-day.png
            artekroom-humi-week.png
    * lub grupowo na node:
        _node_-_period_.png
            np:.
            outnode-day.png
            salon-week.png
- cyliczne generowanie statystyk(wykresów) w tle:
    * roczne(year) raz na tydzieñ
    * miesiêczne(mounth) co 24h
    * tygodniowe(week) co 12h
    * dzienne(day) na bie¿¹co z przegl¹darki
    * godzinne(1h) na bie¿¹co z przegl¹darki
- przechowywanie plików w 'static/img/graphs'
- dodanie ignora do githuba dla katalogu z wykresami
- dodaæ timestamp do generowanego obrazu
- do generowania mo¿na wykorzytaæ 'https://github.com/rholder/retrying'
"""

default_graph_config = {
        "width": 1200,
        "height": 700
        }


class Graphs(object):
    """Generate graph image for selected nodes"""
    def __init__(self, history, debug=True):
        self._logger = logging.getLogger(__name__)
        self.debug = True
        self.history = history
        self.nodescfg = jsontree.clone(config().getConfig('nodes'))


    def generate_graph(self, nodename, sensor, timerange='1h'):
        """Generate graphs for selected node, sensor and time range"""

        _data = self.history.select(nodename, sensor, timerange)
        _title = self.nodescfg[nodename].title
        _desc = self.nodescfg[nodename].sensors[sensor].desc

        graph_data = ColumnDataSource(
            data=dict(
                sensor_timstamps=[datetime.fromtimestamp(int(d[0])) for d in _data],
                sensor_data=[float(d[1])) for d in _data],
                )
        )

        graph = figure(width=default_graph_config['width'],
                        height=default_graph_config['height'],
                        x_axis_type = "datetime",
                        title=_title

        )
        graph.xaxis.axis_label = "Czas"
        graph.yaxis.axis_label = _desc
        graph.ygrid.minor_grid_line_color = 'black'
        graph.ygrid.minor_grid_line_alpha = 0.1
        graph.background_fill_color = "#2f4f4f"
        graph.background_fill_alpha = 0.1

        graph.line("sensor_timstamps", "sensor_data",
                        source=graph_data,
                        color='red',
                        alpha=0.5,
                        line_width=2.5
        )

        script, div = components(graph)
        return (script, div)
