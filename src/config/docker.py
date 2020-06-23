"""Docker configs

"""
import os

DEBUG = False
APP_PORT = int(os.environ.get('DS_APP_PORT', 5050))
DS_STATIC_PATH = os.environ.get('DS_STATIC_PATH')
DS_LOG_DIR = os.environ.get('DS_LOG_DIR')
DS_TMP_DIR = os.environ.get('DS_TMP_DIR')
DS_WEB_LOG = os.path.join(DS_LOG_DIR, 'lan_nanny_web.log')

# End File: documenta-slacka/src/modules/config/docker.py
