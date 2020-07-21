dialogOpen = function(opt){
	var defaults = {
		id : 'layerForm',
		type:2,
		title : '',
		width: '',
		height: '',
		url : null,
		scroll : false,
		content:'',
		data : {},
		btn: ['确定', '取消'],
		success: function(){},
		yes: function(){}
	}
	var option = $.extend({}, defaults, opt);
	if(option.content===""){
		if(option.scroll){
			content = [option.url]
		}else{
			content = [option.url, 'no']
		}
	}else{
		option.type = 1;
	}
	top.layer.open({
	  	type : option.type,
	  	id : option.id,
		title : option.title,
		closeBtn : 1,
		anim: -1,
		isOutAnim: false,
		shadeClose : false,
		shade : 0.3,
		area : [option.width, option.height],
		content : option.content,
		btn: option.btn,
		success: function(){
			option.success(option.id);
		},
		yes: function(){
			option.yes(option.id);
		}
    });
}
//角色判断
function hasRole(role) {
	if (isNullOrEmpty(window.parent.role)) {
		return false;
	}
	if (window.parent.role.indexOf(role) > -1) {
		return true;
	} else {
		return false;
	}
}
isNullOrEmpty = function(obj) {
	if ((typeof (obj) == "string" && obj == "") || obj == null || obj == undefined) {
		return true;
	} else {
		return false;
	}
}

tabiframeId = function() {
	var iframeId = top.$(".DP_iframe:visible").attr("id");
	return iframeId;
}

$.currentIframe = function() {
	var tabId = tabiframeId();
	if (isNullOrEmpty(tabId)) {// 单页iframe嵌套
		return $(window.parent.document).contents().find('#main')[0].contentWindow;
	}
	return $(window.parent.document).contents().find('#' + tabiframeId())[0].contentWindow;// 多层tab页嵌套
}
/**
 * 场景一 如果后台以一个Map参数 @RequestBody Map<String, Object> params 传输  JSON.stringify(options.param) 
 * 场景二 如果后台以多个参数 String username, String password 直接调用即可 手动设置 json : true
 */
$.SaveForm = function(options) {
	var defaults = {
		url : "",
		param : {},
		type : "post",
		async :true,
		dataType : "json",
		contentType : 'application/json',
		jsonType:'application/x-www-form-urlencoded; charset=UTF-8',
		success : null,
		close : true,
		json : false,
		success : true
	};
	var options = $.extend(defaults, options);
	window.setTimeout(function() {
		$.ajax({
			url : options.url,
			data : options.json?options.param:JSON.stringify(options.param),
			type : options.type,
			async :options.async,
			dataType : options.dataType,
			contentType : options.json?options.jsonType:options.contentType,
			success : function(data) {
				if (data.code == '500') {
					pop.error(data.msg);
				} else {
					options.success(data);
				}
				dialogClose();
			},
			error : function(XMLHttpRequest, textStatus, errorThrown) {
				pop.error("系统异常，请稍后再试");
			}
		});
	}, 500);
}
$.SetForm = function(options) {
	var defaults = {
		url : "",
		param : {},
		type : "post",
		async :true,
		dataType : "json",
		contentType : 'application/json',
		jsonType:'application/x-www-form-urlencoded; charset=UTF-8',
		success : null,
		close : true,
		json : false,
		loadingShow:true
	};
	var options = $.extend(defaults, options);
	$.ajax({
		url : options.url,
		data : options.json?options.param:JSON.stringify(options.param),
		type : options.type,
		async :options.async,
		dataType : options.dataType,
		contentType : options.json?options.jsonType:options.contentType,
		success : function(data) {
			if (data.code == '500') {
				pop.error(data.msg);
			} else {
				options.success(data.rows);
			}
		},
		error : function(XMLHttpRequest, textStatus, errorThrown) {
			pop.error(errorThrown);
		}
	});
}
dialogClose = function() {
	var index = top.layer.getFrameIndex(window.name); // 先得到当前iframe层的索引
	top.layer.close(index); // 再执行关闭
}
/**
 * 显示加载框
 * @param message
 */
function loading(){
	layer.load(1, {
		  shade: [0.1,'#fff'] 
		});
}
var pop={};

/**
 * 消息提示
 */
pop.info=function(message){
	showMsg(message,"info");
}

/**
 * 成功提示
 */
pop.success=function(message){
	showMsg(message,"success");
}

/**
 * 错误提示
 */
pop.error=function(message){
	showMsg(message,"error");
}
/**
 * 显示提示框
 */
function showMsg(message,type,closed,timeout){
	var $layer = getLayer();
	var iconType;
	//如果type为函数，则后面的参数往前移
	if (typeof type == 'function') {
		closed=type;
	}else if(type=="info"){
		iconType=0;
	}else if(type=="success"){
		iconType=1;
	}else if(type=="error"){
		iconType=2;
	}else if(type=="question"){
		iconType=3;
	}else if(type=="lock"){
		iconType=4;
	}else if(type=="cry"){
		iconType=5;
	}else if(type=="smile"){
		iconType=6;
	}
	//如果closed不是函数，则后面的参数往前移
	if (typeof closed != 'function') {
		timeout=closed;
	}
	if(iconType!=""&&timeout!=""){
		$layer.msg(message, {icon: iconType,time: timeout}, function(){
			if (typeof closed == 'function') {
				closed();
			}
		});   
	}else if(iconType!=""){
		$layer.msg(message, {icon: iconType}, function(){
			if (typeof closed == 'function') {
				closed();
			}
		});   
	}else{
		$layer.msg(message,{icon: 0});
	}
}
/**
 * 获得layer对话框对象
 */
function getLayer(){
	var $layer = undefined;
	if (top.layer){
		$layer = top.layer;
	}else if (parent.layer){
		$layer = parent.layer;
	}else if (layer){
		$layer = layer;
	}
	return $layer;
}
//时间格式化
function formatDate (date, fmt) {
	  var  o = {
		    'M+': date.getMonth() + 1, // 月份
		    'd+': date.getDate(), // 日
		    'h+': date.getHours(), // 小时
		    'm+': date.getMinutes(), // 分
		    's+': date.getSeconds(), // 秒
		    'S': date.getMilliseconds() // 毫秒
	  }
	  if (/(y+)/.test(fmt)) {
	      fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
	  }
	  for (var k in o) {
	      if (new RegExp('(' + k + ')').test(fmt)) {
	          fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
	      }
	  }
	  return fmt
}