"use strict";

var fs = require('fs');

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : ''
});

function sql(executesql,callback){
	connection = mysql.createConnection(connection.config);  
	connection.connect();
	connection.query(executesql, function(err, rows, fields) {
	  if (err) throw err;
	  callback(rows);

	});
	connection.end();
}

exports.index=function(req,res,view,cache){
	sql("show databases",function(rows){
		console.log(rows);
		var data={"username":"nofeng","rows":rows};
		res.render(view,data);
	});
	console.log("sql-admin");
}

exports.tables=function(req,res,view,cache){
	res.writeHead(200, {'Content-Type': 'text/json;charset=utf-8' }); 
	var table=req.body.table?req.body.table:"";
	var database=req.body.database?req.body.database:"";
	console.log(table);
	console.log(database);
	if(table!=""){
		var columns_sql="SELECT * FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='"+database+"' and table_name='"+table+"'";
		console.log(columns_sql);
		sql(columns_sql,function(rows){
			var data=[];
			for(var index in rows){
				var row=rows[index];
				var column_name=row["COLUMN_NAME"];
				console.log(column_name);
				data[index]={"name":column_name,"column_name":column_name,"table":table,"database":database,"isParent":"false"};
			}	
			var str = JSON.stringify(data);
			//console.log(str);
			res.write(str); 
			res.end();
			return;
		});
	}else{
		var tables_sql="select table_name from information_schema.tables where table_schema='"+database+"'";
		sql(tables_sql,function(rows){
			var data=[];
			for(var index in rows){
				var row=rows[index];
				var tableName=row["table_name"];
				data[index]={"name":tableName,"table":tableName,"database":database,"isParent":"true"};
			}	
			var str = JSON.stringify(data);
			//console.log(str);
			res.write(str); 
			res.end();
		});
	}
}


