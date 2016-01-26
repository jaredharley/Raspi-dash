import os
from app import app
from flask import render_template, flash, redirect, url_for, request, g
from stats import Stats
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	s = Stats()
	o = {
	'ip_address':s.get_ip_address(),
	'memory':s.get_memory(),
	'temp_f':s.get_temperature('f'),
	'temp_c':s.get_temperature('c'),
	'raw_uptime':s.get_uptime(),
	'uptime':"%dd %dh %0dm" % (s.get_uptime()['days'], s.get_uptime()['hours'], s.get_uptime()['minutes']),
	'last_boot':s.get_last_boot(),
	'filesystem':s.get_filesystem(),
	'cpu':s.get_cpu(),
	'network':s.get_network(),
	'name':os.uname(),
	'time':datetime.now()
	}
	return render_template('index.html',stats=o)
