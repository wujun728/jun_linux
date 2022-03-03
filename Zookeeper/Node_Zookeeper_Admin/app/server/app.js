var express = require('express');//引用express
var fs=require('fs');
var app = express();//创建服务器
var cache={};//创建服务器缓存
app.engine('html', require('ejs').renderFile);

app.configure(function(){
  app.set('view engine', 'ejs');
  app.set('action', __dirname);
  app.set('views', __dirname );
  app.set('plugin', __dirname+'/plugin');
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});
app.configure('development', function(){
  app.use(express.errorHandler());
});  

//初始路由 
app_route={
	plugins:{},
	init_plugin:function(){
		var plugin_file=__dirname+'/plugin.json';
		if(!fs.existsSync(plugin_file)){
			console.log("插件配置文件不存在,不配置插件:"+plugin_file);		
			return;
		}
		var plugins=JSON.parse(fs.readFileSync(plugin_file,'utf8'));
		this.plugins=plugins;
		for(plugin in plugins){ 	
			console.log("正在加载插件:"+plugin);		
			var route_file=__dirname+"/plugin"+plugin+'/route.json';
			var routes=app_route.load_route(route_file);
			if(routes!=null){
				console.log("加载%s插件路由成功",plugin);		
				console.log("路由:"+route_file);		
				app.use(express.static(app.get('plugin')+plugin+"/public"));
				//注册路径信息
				app_route.register_route(routes,plugin);
			}else{
				console.log("加载插件路由失败:"+route_file);		
			}
			
		}
	},
	init_default_plugin:function(){
		var route_file=__dirname+'/route.json';
		var routes=app_route.load_route(route_file);
		//注册路径信息
		app_route.register_route(routes);
	},
	init:function(){ 
		this.init_plugin();
		this.init_default_plugin();
		//注册404
		//app_route.register_route_404();
	},
	load_route:function(route_path){
		if(!fs.existsSync(route_path)){
			return null;
		}
		var routes=JSON.parse(fs.readFileSync(route_path,'utf8'));
		return routes;
	},
	register_route_404:function(){
		app.get('/*', function(req, res){
			res.render('404/index.html',{message:'你访问的页面不存在'});
		})
	},
	register_route:function(routes,plugin){
		var plugin_path="";
		if(plugin!=null){
			plugin_path=app.get('plugin')+plugin+"/";
		}else{
			plugin_path="./";
		}
		for(path in routes){ 		
			function execute(){
				var method=routes[path].method;	
				var view=plugin_path+"view/"+routes[path].view;	
				var action=plugin_path+"action/"+routes[path].action;
				var request_method=routes[path].request==null?"get":"post";	
				console.log("正在注册路径:"+path);	
				console.log("正在注册action:"+action);				
				console.log("正在注册路径方法:"+method);
				if(request_method=="post"){ 
					app.post(path, function(req, res){			
						app_route.execute_action(req, res,view,action,method);
					});
				}else{
					app.get(path, function(req, res){			
						app_route.execute_action(req, res,view,action,method);
					});
				}	
			}
			execute();
		}		
	},
	execute_action:function(req, res,view,action,method){
		var actionEngine=require(action);
		var data=eval("require(action)."+method+"(req, res,view,cache)");
		if(typeof(data)=="string"){
			res.redirect(data);
		}else if(data!=null){
			res.render(view, data);
		}
	}
}

app_route.init();

app.listen(3000);//监听端口