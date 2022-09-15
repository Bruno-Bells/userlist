# -*- coding: utf-8 -*-
from config.settings import SERVER_PORT

# bind = 'unix:armone.sock'
bind = f'0.0.0.0:{SERVER_PORT}'
accesslog = '-'
timeout = 600
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'
