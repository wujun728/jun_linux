"use strict";

var http = require('http');
var querystring=require("querystring"); 



function request_server(host, url,data,cookies,callback) {
	var contents=querystring.stringify(data); 
	var options = {
		host: host,
		path: url,
		method: 'POST',
		headers: {
			'Set-cookie':cookies,
			'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
			"Content-Length":contents.length,
			'Accept': 'text/xml;charset=utf-8',
			"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)" 
		}
	};

	var req = http.request(options, function(res) {
		res.setEncoding('utf8');
		var headers=res.headers;   
		var cookies = headers["set-cookie"];		
		res.on('data', function(chunk) {
			callback(chunk,cookies);
		});
		
	});
	req.write(contents);
	req.end();
}

exports.report = function(req, res, view, cache) {
	var data={
		"user.nickname":"",
		"user.password":base64_encode("")
	}
	var mycookies=[];
	request_server("","/login.do?method=login",data,mycookies,function(res,cookies){
			mycookies=cookies;
			console.log(res);
			var query_data={"sql":"select 1","db_id":"12"};
			request_server("","/queryData.do?method=initData",query_data,mycookies,function(res,cookies){
				mycookies=cookies;
				console.log(res);
			});

	});
	console.log("report");
}


function base64_encode(str) {return new Buffer(str).toString('base64');}