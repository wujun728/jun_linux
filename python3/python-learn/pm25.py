#!/usr/bin/env python
#-*-encoding=utf-8-*-

import json, urllib

def _print_data( l ):
	aqi		= l['aqi']
	position_name 	= l['position_name']
	quality 	= l['quality'].encode('utf-8')
	pm2_5		= l['pm2_5']
	pm2_5_24h	= l['pm2_5_24h']
	time_point	= l['time_point'].encode('utf-8')
	station_code	= l['station_code']
	primary_pollutant = l['primary_pollutant']

	if station_code is None:
		station_code = '未知代码'
	else:
		station_code = station_code.encode('utf-8')

	if primary_pollutant is None:
		primary_pollutant = '未知代码'
	else:
		primary_pollutant = primary_pollutant.encode('utf-8')
		
	if position_name is None:
		position_name = '未知检测点'
	else:
		position_name = position_name.encode('utf-8')
		
	print "检测点:[%s]\n检测点代码:[%s]\n空气指数:[%d]\n空气质量:[%s]\n颗粒物:[%d]\n颗粒物(24小时):[%d]\n统计时间:[%s]\n" % ( position_name, station_code, aqi, quality, pm2_5, pm2_5_24h, time_point)

def _test():
	url = 'http://pm25.in/api/querys/pm2_5.json?token=5j1znBVAsnSf5xQyNQyq&city=wulumuqi'
	data = unicode(urllib.urlopen( url ).read())
	obj = json.loads( data )
	for i in range(len(obj)):
		_print_data( obj[i] )

def parse_pm25():
    url = 'http://pm25.in/api/querys/pm2_5.json?token=5j1znBVAsnSf5xQyNQyq&city=wulumuqi'
    s = urllib.urlopen(url).read()
    #print s
    try:
        obj = json.loads(s)
    except ValueError, e:
        print e.message
        sys.exit(-1)
    pass

if __name__ == '__main__':
	parse_pm25()
