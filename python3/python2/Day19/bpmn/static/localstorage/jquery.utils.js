$.extend({

});

$.fn.extend({
    trim: function () { return $.trim(this.val()); },
    lTrim: function () { return this.val().replace(/^\s+/, ''); },
    rTrim: function () { return this.val().replace(/\s+$/, ''); },

    setDisabled: function (disabled) {
        return this.each(function () { $(this).attr('disabled', disabled).css('opacity', disabled ? 0.5 : 1.0); });
    },
    setReadOnly: function (readonly) {
        return this.each(function () { $(this).attr('readonly', readonly).css('opacity', readonly ? 0.5 : 1.0); });
    },
    setChecked: function (checked, value) {
        return this.each(function () { if (value == undefined) { $(this).attr('checked', checked); } else if ($(this).val() == value.toString()) { $(this).attr('checked', checked); } });
    }
});

var J = J || {};

$.extend(J, {
    IsIE: $.support.msie != undefined,
    IsIE6: $.support.msie && parseInt($.support.version) === 6,

    CopyText: function (obj) { var str = J.IsElement(obj) ? obj.value : ($(obj).size() > 0 ? $(obj).val() : obj); if (window.clipboardData && clipboardData.setData && window.clipboardData.setData("Text", str)) { return true; } else { if (J.IsElement(obj)) o.select(); return false; } },
    AddBookMark: function (url, title) { try { if (window.sidebar) { window.sidebar.addPanel(title, url, ''); } else if (J.IsIE) { window.external.AddFavorite(url, title); } else if (window.opera && window.print) { return true; } } catch (e) { alert("Your browser does not support it."); } },
    SetHomePage: function (url) { try { document.body.style.behavior = 'url(#default#homepage)'; document.body.setHomePage(url); } catch (e) { if (window.netscape) { try { netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect"); } catch (e) { alert("Your browser does not support it."); } var prefs = Components.classes['@mozilla.org/preferences-service;1'].getService(Components.interfaces.nsIPrefBranch); prefs.setCharPref('browser.startup.homepage', url); } } },

    GetCookie: function (name) { var r = new RegExp('(^|;|\\s+)' + name + '=([^;]*)(;|$)'); var m = document.cookie.match(r); return (!m ? '' : DecodeURIComponent(m[2])); },
    SetCookie: function (name, value, expire, domain, path) { var s = name + '=' + EncodeURIComponent(value); if (!J.IsUndefined(path)) s = s + '; path=' + path; if (expire > 0) { var d = new Date(); d.setTime(d.getTime() + expire * 1000); if (!J.IsUndefined(domain)) s = s + '; domain=' + domain; s = s + '; expires=' + d.toGMTString(); } document.cookie = s; },
    RemoveCookie: function (name, domain, path) { var s = name + '='; if (!J.IsUndefined(domain)) s = s + '; domain=' + domain; if (!J.IsUndefined(path)) s = s + '; path=' + path; s = s + '; expires=Fri, 02-Jan-1970 00:00:00 GMT'; document.cookie = s; },

    IsUndefined: function (obj) { return typeof obj == 'undefined'; },
    IsObject: function (obj) { return typeof obj == 'object'; },
    IsNumber: function (obj) { return typeof obj == 'number'; },
    IsString: function (obj) { return typeof obj == 'string'; },
    IsElement: function (obj) { return obj && obj.nodeType == 1; },
    IsFunction: function (obj) { return typeof obj == 'function'; },
    IsArray: function (obj) { return Object.prototype.toString.call(obj) === '[object Array]'; },

    IsInt: function (str) { return /^-?\d+$/.test(str); },
    IsFloat: function (str) { return /^(-?\d+)(\.\d+)?$/.test(str); },
    IsIntPositive: function (str) { return /^[0-9]*[1-9][0-9]*$/.test(str); },
    IsFloatPositive: function (str) { return /^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$/.test(str); },
    IsLetter: function (str) { return /^[A-Za-z]+$/.test(str); },
    IsChinese: function (str) { return /^[\u0391-\uFFE5]+$/.test(str); },
    IsZipCode: function (str) { return /^[1-9]\d{5}$/.test(str); },
    IsEmail: function (str) { return /^[A-Z_a-z0-9-\.]+@([A-Z_a-z0-9-]+\.)+[a-z0-9A-Z]{2,4}$/.test(str); },
    IsMobile: function (str) { return /^((\(\d{2,3}\))|(\d{3}\-))?((1[35]\d{9})|(18[89]\d{8}))$/.test(str); },
    IsUrl: function (str) { return /^(http:|ftp:)\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"])*$/.test(str); },
    IsIpAddress: function (str) { return /^(0|[1-9]\d?|[0-1]\d{2}|2[0-4]\d|25[0-5]).(0|[1-9]\d?|[0-1]\d{2}|2[0-4]\d|25[0-5]).(0|[1-9]\d?|[0-1]\d{2}|2[0-4]\d|25[0-5]).(0|[1-9]\d?|[0-1]\d{2}|2[0-4]\d|25[0-5])$/.test(str); },


    Encode: function (str) { return encodeURIComponent(str); },
    Decode: function (str) { return decodeURIComponent(str); },
    FormatString: function () { if (arguments.length == 0) return ''; if (arguments.length == 1) return arguments[0]; var args = J.CloneArray(arguments); args.splice(0, 1); return arguments[0].replace(/{(\d+)?}/g, function ($0, $1) { return args[parseInt($1)]; }); },

    EscapeHtml: function (str) { return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); },
    UnEscapeHtml: function (str) { return str.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&nbsp;/g, " ").replace(/&quot;/g, "\"").replace(/&amp;/g, "&"); },
    FilterHtml: function (str) { str = str.replace(/\<(.*?)\>/g, '', str); str = str.replace(/\<\/(.*?)\>/g, '', str); return str; },

    CloneArray: function (arr) { var cloned = []; for (var i = 0, j = arr.length; i < j; i++) { cloned[i] = arr[i]; } return cloned; },

    GetKeyCode: function (e) { var evt = window.event || e; return evt.keyCode ? evt.keyCode : evt.which ? evt.which : evt.charCode; },
    EnterSubmit: function (e, v) { if (J.GetKeyCode(e) == 13) { if (J.IsFunction(v)) { v(); } else if (J.IsString(v)) { $(v)[0].click(); } } },
    CtrlEnterSubmit: function (e, v) { var evt = window.event || e; if (evt.ctrlKey && J.GetKeyCode(evt) == 13) { if (J.IsFunction(v)) { v(); } else if (J.IsString(v)) { $(v)[0].click(); } } },

    GetUrlQuery: function (key, Decode, url) { url = url || window.location.href; if (url.indexOf("#") !== -1) url = url.substring(0, url.indexOf("#")); var rts = [], rt; queryReg = new RegExp("(^|\\?|&)" + key + "=([^&]*)(?=&|#|$)", "g"); while ((rt = queryReg.exec(url)) != null) { if (Decode && Decode == true) rts.push(DecodeURIComponent(rt[2])); else rts.push(rt[2]); } return rts.length == 0 ? '' : (rts.length == 1 ? rts[0] : rts); },

    PostJson: function (url, data, success, error, option) {
        var op = {
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            cache: false,
            success: function (data, textStatus) {
                if (data == null || data == undefined) {
                    if (typeof error == 'function') error();
                }
                else {
                    if (typeof error == 'function') success(data, textStatus);
                }
            },
            error: error
        };
        $.extend(op, option);
        $.ajax(op);
    },

    PreloadImages: function () {
        for (var i = 0; i < arguments.length; i++) {
            var img = new Image();
            img.src = arguments[i];
        }
    }

});