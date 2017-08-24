# -*- coding: utf-8 -*-
import pandas as pd

import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import numpy as np
from flask import Flask

df_jobs = pd.read_csv('nyt_255_ces.csv')
df_wages = pd.read_csv('nyt_255_wages.csv')


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
