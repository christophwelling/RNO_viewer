
import dash_html_components as html
import dash
from NuRadioReco.detector.detector_browser import detector_map
from NuRadioReco.detector.detector_browser import station_info
from NuRadioReco.detector.detector_browser import channel_info
from NuRadioReco.detector.detector_browser import hardware_response

import NuRadioReco.detector.detector_browser.detector_provider
from flask import send_file, send_from_directory
from NuRadioReco.detector.detector_browser.app import app
import json
import os

app.title = 'Radio Neutrino Observatory in Greenland'

app.layout = html.Div([
    html.Div('', id='output-dummy', style={'display': 'inline'}),
    html.Div('', id='load-dummy', style={'display': 'none'}),
    html.Div([
        html.Div(
            [
                html.A(
                    [
                        html.Button('Download JSON', className='btn btn-primary')
                    ],
                    href='/dash/rno-station',
                    download='true'
                ),
                station_info.layout,
                channel_info.layout
            ],
            style={'flex': '1'}
        ),
        html.Div([
            detector_map.layout,
            hardware_response.layout
        ], style={'flex': '2'})
    ], style={'display': 'flex'})
])


@app.server.route('/dash/rno-station')
def download_json():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        filename='detector_description/RNO_detector.json'
    )


if __name__ == '__main__':
    if int(dash.__version__.split('.')[0]) <= 1:
        if int(dash.__version__.split('.')[1]) < 0:
            print('WARNING: Dash version 0.39.0 or newer is required, you are running version {}. Please update.'.format(dash.__version__))
    detector_provider = NuRadioReco.detector.detector_browser.detector_provider.DetectorProvider()
    detector_provider.set_generic_detector('detector_description/RNO_detector.json', 101, 3, False, False)
    detector_json = json.load(open('detector_description/RNO_detector.json', 'r'))
    app.run_server()


