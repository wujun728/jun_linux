"use strict";
var zookeeper = require("node-zookeeper-client");
var fs = require('fs');

exports.index=function(req,res,view,cache){
	console.log("zookeeper-admin");
	return {};
}

exports.directory=function(req,res,view,cache){
	var path=req.body.path?req.body.path:"/";	
	var client = zookeeper.createClient('localhost:2181');	
	function listChildren(client, path) {
		client.getChildren(
			path,
			function (error, children, stat) {
				if (error) {
					console.log(
						'Failed to list children of %s due to: %s.',
						path,
						error
					);
					return;
				}

				console.log('Children of %s are: %j.%s', path, children,children.length);
				res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
				var data=[];
				for(var index in children){
					var child=children[index];
					console.log("child:"+child);
					var childPath=path+"/"+child;
					if(path=="/"){
						childPath="/"+child;
					}
					data[index]={"name":child,"id":childPath,"path":childPath,"isParent":"true"};
				}	
				
				var str = JSON.stringify(data);
				console.log(str);
				res.write(str); 
				res.end();
				client.close();
				
			}
		);
	}
	
	client.once('connected', function () {
		console.log('Connected to ZooKeeper.');
		listChildren(client, path);
	});

	client.connect();
}

exports.data=function(req,res,view,cache){
	var path=req.body.path?req.body.path:"/";
	var client = zookeeper.createClient('localhost:2181');	
	console.log('Node: %s ', path);
	function data(client,path){
		client.exists(path, function (error, stat) {
			if (error) {
				console.log(error.stack);
				return;
			}
			if (stat) {
				client.getData(
					path,
					function (event) {
						console.log('Got event: %s.', event);
					},
					function (error, data, stat) {
						if (error) {
							console.log(error.stack);
							return;
						}
						var msg=data.toString('utf8');
						console.log('Got data: %s',msg);
						res.writeHead(200, {'Content-Type': 'text/html;charset=utf-8' });  
						res.write(msg); 
						res.end();
						client.close();
					}
				);
			} else {
				console.log('Node does not exist.');
			}
		});
	}
	client.once('connected', function () {
		data(client, path);
	});
	client.connect();
}

exports.set_data=function(req,res,view,cache){
	var path=req.body.path?req.body.path:"/";
	var data=new Buffer(req.body.data?req.body.data:"");
	var client = zookeeper.createClient('localhost:2181');	
	
	function set_data(client,path,data){
		client.exists(path, function (error, stat) {
			if (error) {
				console.log(error.stack);
				return;
			}
			if (stat) {
				client.setData(path, data, -1, function (error, stat) {
					if (error) {
						console.log(error.stack);
						var success={success:false};
						res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
						res.write(JSON.stringify(success)); 
						res.end();
						client.close();
						return;
					}
					var success={success:true};
					res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
					res.write(JSON.stringify(success)); 
					res.end();
					client.close();
				});
			} else {
				console.log('Node does not exist.');
			}
		});
	}
	client.once('connected', function () {
		set_data(client, path,data);
	});
	client.connect();
}

exports.delete_node=function(req,res,view,cache){
	var path=req.body.path?req.body.path:"/";

	var client = zookeeper.createClient('localhost:2181');	
	
	function delete_node(client,path){
		client.remove(path, -1, function (error) {
			if (error) {
				console.log(error.stack);
				var success={success:false};
				res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
				res.write(JSON.stringify(success)); 
				res.end();
				client.close();
				return;
			}

			var success={success:true};
			res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
			res.write(JSON.stringify(success)); 
			res.end();
			client.close();
		});
	}
	client.once('connected', function () {
		delete_node(client, path);
	});
	client.connect();
}

exports.create=function(req,res,view,cache){
	var path=req.body.path?req.body.path:"/";	
	var data=req.body.data?req.body.data:"";	
	var client = zookeeper.createClient('localhost:2181');	
	
	function create(client, path,data) {
		client.create(
			path,
			new Buffer(data),
			
			function (error, path) {
				if (error) {
					console.log(error.stack);
					return;
					var success={success:false};
					res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
					res.write(JSON.stringify(success)); 
					res.end();
					client.close();
				}

				console.log('Node: %s is created.', path);
				res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' });  
				var data={};
				data.success=true;
				var str = JSON.stringify(data);
				console.log(str);				
				res.write(str); 
				res.end();
				client.close();
			}
		);
	}
	
	client.once('connected', function () {
		console.log('Connected to ZooKeeper.');
		create(client, path,data);
	});

	client.connect();
}

