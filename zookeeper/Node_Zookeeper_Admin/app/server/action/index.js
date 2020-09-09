"use strict";
var async = require("async");
var fs = require('fs');
exports.execute=function(req,res,view,cache){

	fs.exists('c:/passwd', function (exists) {
		  var existMsg=exists ? "存在" : "不存在";
			cache.isExists=existMsg;
			res.render(view, {title: cache.isExists});
		});


}

exports.children=function(req,res,view,cache){
	console.log("req:"+JSON.stringify(req.body)); 
	res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
	var data=[{"name":"text","id":"node_139575876789282","isParent":"true"},{"name":"text2","id":"node_13957587678928222"}];
	var str = JSON.stringify(data);
	res.write(str); 
	res.end();

}

exports.home=function(){
console.log("home");
	return {title: '标题是必须的home'};
}

exports.back=function(){
	return "/";
}