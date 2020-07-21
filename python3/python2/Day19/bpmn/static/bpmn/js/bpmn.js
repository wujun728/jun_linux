 var bpmnModeler = new BpmnJS({
        container: '#canvas',
        keyboard: {
          bindTo: window
        }
      });
      /**
       * Save diagram contents and print them to the console.
       */
      function exportDiagram() {
	        bpmnModeler.saveXML({ format: true }, function(err, xml) {
	          if (err) {
	          	  return console.error('could not save BPMN 2.0 diagram', err);
	          }
	          var modelName = $.trim($("#modelName").val());
	          if(modelName==""){
	        	  pop.info("请输入流程名称");
	        	  return;
	          }
	          // 如果浏览器支持msSaveOrOpenBlob方法（也就是使用IE浏览器的时候）
	          if (window.navigator.msSaveOrOpenBlob) {
	        	      var blob = new Blob([xml],{type : 'text/plain'});
		              window.navigator.msSaveOrOpenBlob(blob, modelName+'.bpmn');
	          } else {
	        	    var eleLink = document.createElement('a');
	        	    eleLink.download = modelName+".bpmn";
	        	    eleLink.style.display = 'none';
	        	    var blob = new Blob([xml]);  // 字符内容转变成blob地址
	        	    eleLink.href = URL.createObjectURL(blob);
	        	    document.body.appendChild(eleLink);  // 触发点击
	        	    eleLink.click();
	        	    document.body.removeChild(eleLink);   // 然后移除
	          } 
//	          var mySvg = document.querySelector("svg");
//	     	  var svgXml = $('svg').prop("outerHTML"); IE下有问题
	          var _canvas = document.querySelector('svg');
	          var w = parseInt(window.getComputedStyle(_canvas).width);
	          var h = parseInt(window.getComputedStyle(_canvas).height);
	          var svgXml = $('svg').html();
	          var base = '<svg width="'+w+'px" height="'+h+'px" style="touch-action: none; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);" data-element-id="Process_1" class="">'
	          svgXml = base + svgXml +"</svg>";
	          var canvas = document.createElement('canvas');  //准备空画布
	     	  canvg(canvas, svgXml);
	     	  bpmnImage = canvas.toDataURL('image/png');
	          $.SaveForm({
					url :  "/bpmn/save",
					param : {"bpmnXml":xml,"modelName":modelName,"id":bpmnId,"bpmnImage":bpmnImage},
					json:true,
					success : function(result) {
						var id = result.msg;
						pop.success("保存成功");
						$('.sidebar-menu', parent.document).find("li[data-src='bpmn/index.shtml']").trigger("click");
					}
				});
	        });
      }
      /**
       * Open diagram in our modeler instance.
       * @param {String} bpmnXML diagram to display
       */
      function openDiagram(bpmnXML) {
    	   if(bpmnXML===""||bpmnXML===null){
				  bpmnXML='<?xml version="1.0" encoding="UTF-8"?>\n' +
				'<bpmn2:definitions xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:bpmn2="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xsi:schemaLocation="http://www.omg.org/spec/BPMN/20100524/MODEL BPMN20.xsd" id="sample-diagram" targetNamespace="http://bpmn.io/schema/bpmn">\n' +
				'  <bpmn2:process id="Process_1">\n' +
				'    <bpmn2:startEvent id="StartEvent_1"/>\n' +
				'  </bpmn2:process>\n' +
				'  <bpmndi:BPMNDiagram id="BPMNDiagram_1">\n' +
				'    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">\n' +
				'      <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1">\n' +
				'        <dc:Bounds height="36.0" width="36.0" x="412.0" y="240.0"/>\n' +
				'      </bpmndi:BPMNShape>\n' +
				'    </bpmndi:BPMNPlane>\n' +
				'  </bpmndi:BPMNDiagram>\n' +
				'</bpmn2:definitions>'; //BPMN 2.0 xml
    	   }
	        // import diagram
	        bpmnModeler.importXML(bpmnXML, function(err) {
		          if (err) {
		            return console.error('could not import BPMN 2.0 diagram', err);
		          }
	        });
}
openDiagram("");
$('#fullscreen').click(function() {
	var screen = isFull();
	if (screen) {
		exitScreen();
	} else {
		fullScreen();
	}
});
// 网页全屏代码
function fullScreen() {
	// ie10以下全屏模式
	if (window.ActiveXObject) {
		var wscript = new ActiveXObject("WScript.Shell");
		if (wscript) {
			wscript.SendKeys("{F11}");
			return;
		} else {
			console.log('用户拒接或者加载插件失败');
		}
	};
	// 判断各种浏览器，找到正确的方法
	function fullScreen(obj) {
		if (obj.requestFullscreen) {
			obj.requestFullscreen();
		} else if (obj.mozRequestFullScreen) {
			obj.mozRequestFullScreen();
		} else if (obj.webkitRequestFullscreen) {
			obj.webkitRequestFullscreen();
		} else if (obj.msRequestFullscreen) {
			obj.msRequestFullscreen();
		} else {
			console.log('该浏览器不支持全屏，请升级最新版本');
		}
	};
	// 启动全屏
	fullScreen($('html').get(0)); // 整个网页
	// fullScreen(document.getElementById("videoElement")); //某个页面元素
};

// 退出全屏代码
function exitScreen() {
	// ie10以下全屏模式
	if (window.ActiveXObject) {
		var wscript = new ActiveXObject("WScript.Shell");
		if (wscript) {
			wscript.SendKeys("{F11}");
			return;
		}
	};
	// 判断浏览器种类
	function exit() {
		if (document.exitFullscreen) {
			document.exitFullscreen();
		} else if (document.mozCancelFullScreen) {
			document.mozCancelFullScreen();
		} else if (document.webkitExitFullscreen) {
			document.webkitExitFullscreen();
		} else if (document.msExitFullscreen) {
			document.msExitFullscreen();
		}
	};
	// 退出全屏模式!
	exit();
};
// 判断是否全屏
function isFull() {
	var explorer = window.navigator.userAgent.toLowerCase();
	var full;
	if (explorer.indexOf('chrome') > 0) {// chrome
		if (document.body.scrollHeight == window.screen.height
				&& document.body.scrollWidth == window.screen.width) {
			full = true;
		} else {
			full = false;
		}
	} else {// IE 9+ fireFox
		if (window.outerHeight == window.screen.height
				&& window.outerWidth == window.screen.width) {
			full = true;
		} else {
			full = false;
		}
	};
	return full;
};
$('#keybindings').click(function() {
	$("#help").show();
});
//创建一个新的
function createNew(){
	layer.confirm('确定要重新创建一个BPMN？', {
		btn : [ '确定', '取消' ]
	// 按钮
	}, function() {
		layer.closeAll()
		openDiagram("")
	}, function() {
		
	});
}
//打开本地BPMN
function openLocal(){
	document.getElementById("btn_file").click(); 
}
//展示BPMN
function showBPMN(){
	file = document.getElementById('btn_file').files[0];
    var URL = window.URL || window.webkitURL;
    var imgURL = URL.createObjectURL(file);
    $.get(imgURL,function(xmlDoc,textStatus){
          openDiagram(xmlDoc);
    });
}
//下载SVG
function downloadSVG(){
	 var modelName = $.trim($("#modelName").val());
     if(modelName==""){
	   	  pop.info("请输入流程名称");
	   	  return;
     }
     var _canvas = document.querySelector('svg');
     var w = parseInt(window.getComputedStyle(_canvas).width);
     var h = parseInt(window.getComputedStyle(_canvas).height);
     var svgXml = $('svg').html();
     var base = '<svg width="'+w+'px" height="'+h+'px" style="touch-action: none; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0);" data-element-id="Process_1" class="">'
     svgXml = base + svgXml +"</svg>";
     var canvas = document.createElement('canvas');  //准备空画布
	 canvg(canvas, svgXml);
	 imagedata = canvas.toDataURL('image/png');
     // 如果浏览器支持msSaveOrOpenBlob方法（也就是使用IE浏览器的时候）
     if (window.navigator.msSaveOrOpenBlob) {
         var bstr = atob(imagedata.split(',')[1]);
         var n = bstr.length;
         var u8arr = new Uint8Array(n);
         while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
         }
         var blob = new Blob([u8arr]);
         window.navigator.msSaveOrOpenBlob(blob, modelName+'.png');
     }else{
		var a = document.createElement('a');
		a.href = imagedata;  //将画布内的信息导出为png图片数据
		a.download = modelName;  //设定下载名称
		a.click(); //点击触发下载
     }
}