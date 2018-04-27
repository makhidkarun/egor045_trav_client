'''api_doc.py'''

import requests
from flask import current_app, request, render_template
from . import main


@main.route('/api_doc', methods=['GET'])
def api_doc():
    '''Render API documentation for endpoint (endpoint must be in routes)'''

    data = {}
    error_msg = None
    navbar_items = []
    label = 'Unknown'

    endpoint = request.args.get('endpoint')
    label = request.args.get('label')
    if label is None:
        label = endpoint
    current_app.logger.debug('endpoint = {}'.format(endpoint))
    current_app.logger.debug('label = {}'.format(label))
    if endpoint in current_app.config['KNOWN_API_ENDPOINTS']:
        navbar_items = current_app.config['KNOWN_API_ENDPOINTS'][endpoint]
        # Get API doc
        try:
            resp = requests.get(
                '{}/{}?doc=true'.format(
                    current_app.config['API_SERVER'],
                    endpoint
                )
            )
            if resp.status_code == 200:
                data = resp.json()
            else:
                error_msg = 'Received status {} from API endpoint'.format(
                    resp.status_code)
                current_app.logger.debug(error_msg)
        except requests.ConnectionError:
            current_app.logger.debug('Unable to connect to API endpoint')
            error_msg = 'Unable to connect to API server'

        current_app.logger.debug('data = %s', data)

    current_app.logger.debug('data = %s', data)
    current_app.logger.debug('error_msg = %s', error_msg)
    current_app.logger.debug('navbar_items = %s', navbar_items)
    current_app.logger.debug('label = %s', label)
    return render_template(
        'api_doc.html',
        data=data,
        error_msg=error_msg,
        navbar_items=navbar_items,
        label=label
    )
