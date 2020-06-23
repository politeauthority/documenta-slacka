"""Listener
Web application entry point.

"""

import os
import sys

from flask import Flask, jsonify, render_template, current_app

app = Flask(__name__)
if os.environ.get('DS_CONFIG'):
    app.config.from_object('config.%s' % os.environ.get('DS_CONFIG'))
else:
    app.config.from_object('config.default')


@app.errorhandler(404)
def page_not_found(e: str):
    """404 Error page."""
    return render_template('errors/404.html', error=e), 404


@app.route('/')
def index() -> str:
    """App dashboard for authenticated users."""
    # conn, cursor = db.connect_mysql(app.config['DROP_ZONE_DB'])
    data = {}
    return jsonify(data)


if __name__ == '__main__':
    port = app.config['APP_PORT']
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.secret_key = 'super secret key'
    app.run(host="0.0.0.0", port=port, debug=False)


# End File: documenta-slack/src/listener.py
