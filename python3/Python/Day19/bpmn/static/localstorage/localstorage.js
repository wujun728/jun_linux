/**
 * 注册命名空间
 * @param {String} fullNS 完整的命名空间字符串，如qui.dialog
 * @param {Boolean} isIgnorSelf 是否忽略自己，默认为false，不忽略
 * @example
 *      window.registNS("QingFeed.Text.Bold");
 */
window.registNS = function(fullNS,isIgnorSelf){
    //命名空间合法性校验依据
    var reg = /^[_$a-z]+[_$a-z0-9]*/i;
         
    // 将命名空间切成N部分, 比如baidu.libs.Firefox等
    var nsArray = fullNS.split('.');
    var sEval = "";
    var sNS = "";
    var n = isIgnorSelf ? nsArray.length - 1 : nsArray.length;
    for (var i = 0; i < n; i++){
        //命名空间合法性校验
        if(!reg.test(nsArray[i])) {
            throw new Error("Invalid namespace:" + nsArray[i] + "");
            return ;
        }
        if (i != 0) sNS += ".";
        sNS += nsArray[i];
        // 依次创建构造命名空间对象（假如不存在的话）的语句
        sEval += "if(typeof(" + sNS + ")=='undefined') " + sNS + "=new Object();else " + sNS + ";";
    }
    //生成命名空间
    if (sEval != "") {
        return eval(sEval);
    }
    return {};
};


/**
 * 注册命名空间
 */
window.registNS('bpmn');

/**
 * @class bpmn.LocalStorage
 * 跨浏览器的本地存储实现。高级浏览器使用localstorage，ie使用UserData。虽然说是本地存储，也请不要存储过大数据，最好不要大于64K.
 * 因为ie下UserData每页最大存储是64k。
 * @singleton
 */
(function(){
    /**
     * 验证字符串是否合法的键名
     * @param {Object} key 待验证的key
     * @return {Boolean} true：合法，false：不合法
     * @private
     */
    function _isValidKey(key) {
        return (new RegExp("^[^\\x00-\\x20\\x7f\\(\\)<>@,;:\\\\\\\"\\[\\]\\?=\\{\\}\\/\\u0080-\\uffff]+\x24")).test(key);
    }
    //所有的key
    var _clearAllKey = "_bpmn.ALL.KEY_";
    
    /**
     * 创建并获取这个input:hidden实例
     * @return {HTMLInputElement} input:hidden实例
     * @private
     */
    function _getInstance(){
        //把UserData绑定到input:hidden上
        var _input = null;
        //是的，不要惊讶，这里每次都会创建一个input:hidden并增加到DOM树种
        //目的是避免数据被重复写入，提早造成“磁盘空间写满”的Exception
        _input = document.createElement("input");
        _input.type = "hidden";
        _input.addBehavior("#default#userData");
        document.body.appendChild(_input); 
        return _input;
    }
    
    /**
     * 将数据通过UserData的方式保存到本地，文件名为：文件名为：config.key[1].xml
     * @param {String} key 待存储数据的key，和config参数中的key是一样的
     * @param {Object} config 待存储数据相关配置
     * @cofnig {String} key 待存储数据的key
     * @config {String} value 待存储数据的内容
     * @config {String|Object} [expires] 数据的过期时间，可以是数字，单位是毫秒；也可以是日期对象，表示过期时间
     * @private
     */
    function __setItem(key,config){
        try {
            var input = _getInstance();
            //创建一个Storage对象
            var storageInfo = config || {};
            //设置过期时间
            if(storageInfo.expires) {
                var expires;
                //如果设置项里的expires为数字，则表示数据的能存活的毫秒数
                if ('number' == typeof storageInfo.expires) {
                    expires = new Date();
                    expires.setTime(expires.getTime() + storageInfo.expires);
                }
                input.expires = expires.toUTCString();
            }
            
            //存储数据
            input.setAttribute(storageInfo.key,storageInfo.value);
            //存储到本地文件，文件名为：storageInfo.key[1].xml
            input.save(storageInfo.key);
        } catch (e) {
        }
    }

    /**
     * 将数据通过UserData的方式保存到本地，文件名为：文件名为：config.key[1].xml
     * @param {String} key 待存储数据的key，和config参数中的key是一样的
     * @param {Object} config 待存储数据相关配置
     * @cofnig {String} key 待存储数据的key
     * @config {String} value 待存储数据的内容
     * @config {String|Object} [expires] 数据的过期时间，可以是数字，单位是毫秒；也可以是日期对象，表示过期时间
     * @private
     */
    function _setItem(key,config){
        //保存有效内容
        __setItem(key,config);
        
        //下面的代码用来记录当前保存的key，便于以后clearAll
        var result = _getItem({key : _clearAllKey});
        if(result) {
            result = {
                key : _clearAllKey,
                value : result 
            };
        } else {
            result = {
                key : _clearAllKey,
                value : ""
            };
        }
        
        if(!(new RegExp("(^|\\|)" + key + "(\\||$)",'g')).test(result.value)) {
            result.value += "|" + key;
            //保存键
            __setItem(_clearAllKey,result);     
        }
    }
    
    /**
     * 提取本地存储的数据
     * @param {String} config 待获取的存储数据相关配置
     * @cofnig {String} key 待获取的数据的key
     * @return {String} 本地存储的数据，获取不到时返回null
     * @example 
     * bpmn.LocalStorage.get({
     *      key : "username"
     * });
     * @private
     */
    function _getItem(config){
        try {
            var input = _getInstance();
            //载入本地文件，文件名为：config.key[1].xml
            input.load(config.key);
            //取得数据
            return input.getAttribute(config.key) || null;
        } catch (e) {
            return null;            
        }
    }
    
    /**
     * 移除某项存储数据
     * @param {Object} config 配置参数
     * @cofnig {String} key 待存储数据的key
     * @private
     */
    function _removeItem(config){
		try {
			var input = _getInstance();
			//载入存储区块
			input.load(config.key);
			//移除配置项
			input.removeAttribute(config.key);
			//强制使其过期
			var expires = new Date();
			expires.setTime(expires.getTime() - 1);
			input.expires = expires.toUTCString();
			input.save(config.key);
			
			//从allkey中删除当前key			
			//下面的代码用来记录当前保存的key，便于以后clearAll
			var result = _getItem({key : _clearAllKey});
			if(result) {
				result = result.replace(new RegExp("(^|\\|)" + config.key + "(\\||$)",'g'),'');
				result = {
					key : _clearAllKey,
					value : result 
				};
				//保存键
				__setItem(_clearAllKey,result);	
			}
			
		} catch (e) {
		}
	}
    
    //移除所有的本地数据
    function _clearAll(){
        result = _getItem({key : _clearAllKey});
        if(result) {
            var allKeys = result.split("|");
            var count = allKeys.length;
            for(var i = 0;i < count;i++){
                if(!!allKeys[i]) {
                    _removeItem({key:allKeys[i]});
                }
            }
        }
    }
    
    
    /**
     * 获取所有的本地存储数据对应的key
     * @return {Array} 所有的key
     * @private 
     */
    function _getAllKeys(){
        var result = [];
        var keys = _getItem({key : _clearAllKey});
        if(keys) {
            keys = keys.split('|');
            for(var i = 0,len = keys.length;i < len;i++){
                if(!!keys[i]) {
                    result.push(keys[i]);
                }
            }
        }
        return result ;
    }
    
    /**
     * 判断当前浏览器是否支持本地存储：window.localStorage
     * @return {Boolean} true：支持；false：不支持(jQuery.browser建议弃用，可以使用jQuery.support来代替)
     * @remark 支持本地存储的浏览器：IE8+、Firefox3.0+、Opera10.5+、Chrome4.0+、Safari4.0+、iPhone2.0+、Andrioid2.0+
     * @private
     */
    var _isSupportLocalStorage = (('localStorage' in window) && (window['localStorage'] !== null)),
        _isSupportUserData = !!jQuery.support.ie;
    bpmn.LocalStorage = {
        /**
         * 如果支持本地存储，返回true；否则返回false
         * @type Boolean
         */
        isAvailable : _isSupportLocalStorage || _isSupportUserData,
        
        /**
         * 将数据进行本地存储（只能存储字符串信息）
         * <pre><code>
		 * //保存单个对象
		 * bpmn.LocalStorage.set({
		 * 		key : "username",
		 * 		value : "baiduie",
		 * 		expires : 3600 * 1000
		 * });
		 * //保存对个对象
		 * bpmn.LocalStorage.set([{
		 * 		key : "username",
		 * 		value : "baiduie",
		 * 		expires : 3600 * 1000
		 * },{
		 * 		key : "password",
		 * 		value : "zxlie",
		 * 		expires : 3600 * 1000
		 * }]);
         * </code></pre>
         * @param {Object} obj 待存储数据相关配置，可以是单个JSON对象，也可以是由多个JSON对象组成的数组
         * <ul>
         * <li><b>key</b> : String <div class="sub-desc">待存储数据的key，务必将key值起的复杂一些，如：bpmn.username</div></li>
         * <li><b>value</b> : String <div class="sub-desc">待存储数据的内容</div></li>
         * <li><b>expires</b> : String/Object (Optional)<div class="sub-desc">数据的过期时间，可以是数字，单位是毫秒；也可以是日期对象，表示过期时间</div></li>
         * </ul>
         */
        set : function(obj){
			//保存单个对象
			var _set_ = function(config){
				//key校验
				if(!_isValidKey(config.key)) {return;}

				//待存储的数据
				var storageInfo = config || {};
				
				//支持本地存储的浏览器：IE8+、Firefox3.0+、Opera10.5+、Chrome4.0+、Safari4.0+、iPhone2.0+、Andrioid2.0+
				if(_isSupportLocalStorage) {
					window.localStorage.setItem(storageInfo.key,storageInfo.value);
					if(config.expires) {
                        var expires;
                        //如果设置项里的expires为数字，则表示数据的能存活的毫秒数
                        if ('number' == typeof storageInfo.expires) {
                            expires = new Date();
                            expires.setTime(expires.getTime() + storageInfo.expires);
                        }

                        window.localStorage.setItem(storageInfo.key + ".expires",expires);
					}
				} else if(_isSupportUserData) { //IE7及以下版本，采用UserData方式
					_setItem(config.key,storageInfo);
				}	
			};

			//判断传入的参数是否为数组
			if(obj && obj.constructor === Array && obj instanceof Array){
				for(var i = 0,len = obj.length;i < len;i++){
					_set_(obj[i]);
				}
			}else if(obj){
				_set_(obj);
			}
        },
		
		/**
		 * 提取本地存储的数据
         * <pre><code>
		 * //获取某一个本地存储，返回值为：{key:"",value:"",expires:""}，未取到值时返回值为：null
		 * var rst = bpmn.LocalStorage.get({
		 * 		key : "username"
		 * });
		 * //获取多个本地存储，返回值为：["","",""]，未取到值时返回值为：[null,null,null]
		 * bpmn.LocalStorage.get([{
		 * 		key : "username"
		 * },{
		 * 		key : "password"
		 * },{
		 * 		key : "sex"
		 * }]);
         * </code></pre>
		 * @param {String} obj 待获取的存储数据相关配置，支持单个对象传入，同样也支持多个对象封装的数组格式
		 * @config {String} key 待存储数据的key
		 * @return {String} 本地存储的数据，传入为单个对象时，返回单个对象，获取不到时返回null；传入为数组时，返回为数组
		 */
        get : function(obj){
			//获取某一个本地存储
			var _get_ = function(config){
				//结果	
				var result = null;
				if(typeof config === "string") config = {key : config};
				//key校验
				if(!_isValidKey(config.key)) {return result;}
				
				//支持本地存储的浏览器：IE8+、Firefox3.0+、Opera10.5+、Chrome4.0+、Safari4.0+、iPhone2.0+、Andrioid2.0+
				if(_isSupportLocalStorage) {
					result = window.localStorage.getItem(config.key);
					//过期时间判断，如果过期了，则移除该项
					if(result) {
						var expires = window.localStorage.getItem(config.key + ".expires");
						result = {
							value : result,
							expires : expires ? new Date(expires) : null
						};
						if(result && result.expires && result.expires < new Date()) {
							result = null;
							window.localStorage.removeItem(config.key);
                            window.localStorage.removeItem(config.key + ".expires");
						}
					}
				} else if(_isSupportUserData) { //IE7及以下版本，采用UserData方式
					//这里不用单独判断其expires，因为UserData本身具有这个判断
					result = _getItem(config);
					if(result) {
						result = { value : result };
					}
				}
				
				return result ? result.value : "";
			};
			
			var rst = null;
			//判断传入的参数是否为数组
			if(obj && obj.constructor === Array && obj instanceof Array){
				rst = [];
				for(var i = 0,len = obj.length;i < len;i++){
					rst.push(_get_(obj[i]));
				}
			}else if(obj){
				rst = _get_(obj);
			}
			return rst;
        },
        
        /**
         * 移除某一项本地存储的数据
         * <pre><code>
		 * //删除一个本地存储项
		 * bpmn.LocalStorage.remove({
		 * 		key : "username"
		 * });
		 * //删除多个本地存储项目 *
		 * bpmn.LocalStorage.remove([{
		 * 		key : "username"
		 * },{
		 * 		key : "password"
		 * },{
		 * 		key : "sex"
		 * }]);
         * </code></pre>
		 * @param {String} obj 待移除的存储数据相关配置，支持移除某一个本地存储，也支持数组形式的批量移除
		 * @config {String} key 待移除数据的key
		 * @return 无
         */
        remove : function(obj){
			//移除某一项本地存储的数据
			var _remove_ = function(config){
				//支持本地存储的浏览器：IE8+、Firefox3.0+、Opera10.5+、Chrome4.0+、Safari4.0+、iPhone2.0+、Andrioid2.0+
				if(_isSupportLocalStorage) {
					window.localStorage.removeItem(config.key);
					window.localStorage.removeItem(config.key + ".expires");
				} else if(_isSupportUserData){ //IE7及以下版本，采用UserData方式
					_removeItem(config);
				}
			};
			
			//判断传入的参数是否为数组
			if(obj && obj.constructor === Array && obj instanceof Array){
				for(var i = 0,len = obj.length;i < len;i++){
					_remove_(obj[i]);
				}
			}else if(obj){
				_remove_(obj);
			}
        },
        
        /**
         * 清除所有本地存储的数据
         * <pre><code>
         * bpmn.LocalStorage.clearAll();
         * </code></pre>
         */
        clearAll : function(){
            //支持本地存储的浏览器：IE8+、Firefox3.0+、Opera10.5+、Chrome4.0+、Safari4.0+、iPhone2.0+、Andrioid2.0+
            if(_isSupportLocalStorage) {
                window.localStorage.clear();
            } else if(_isSupportUserData) { //IE7及以下版本，采用UserData方式
                _clearAll();
            }
        },
        
        //保存单个对象到本地
        save:function(key,value){
	        bpmn.LocalStorage.set({
	           key : key,
	           value : value,
	           expires : 30 * 12 * 3600 * 1000  /*单位：ms 这里缓存一个月*/
	        });
        },
        /**
         * 获取所有的本地存储数据对应的key
         * <pre><code>
         * var keys = bpmn.LocalStorage.getAllKeys();
         * </code></pre>
         * @return {Array} 所有的key
         */
        getAllKeys : function(){
            var result = [];
            //支持本地存储的浏览器：IE8+、Firefox3.0+、Opera10.5+、Chrome4.0+、Safari4.0+、iPhone2.0+、Andrioid2.0+
            if(_isSupportLocalStorage) {
                var key;
                for(var i = 0,len = window.localStorage.length;i < len;i++){
                    key = window.localStorage.key(i);
                    if(!/.+\.expires$/.test(key)) {
                        result.push(key);
                    }
                }
            } else if(_isSupportUserData) { //IE7及以下版本，采用UserData方式
                result = _getAllKeys();
            }
            
            return result;
        }
    };

})();