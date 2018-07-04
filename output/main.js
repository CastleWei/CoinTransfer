var lblStatus = document.querySelector('#status');
var chkAutoRefresh = document.querySelector('#auto-refresh');
var txtRefreshInterval = document.querySelector('#refresh-interval');
var btn = document.querySelector('#refresh-now');
var tbd = document.querySelector('#result');
var tbl = document.querySelector('table');

nTimer = 0

btn.onclick = refresh;
chkAutoRefresh.onclick = startTimer

refresh()  // 一打开就默认开始自动刷新
startTimer()


// 以下为函数声明部分

function refresh(){
    var requestURL = 'result.json';
    var request = new XMLHttpRequest();
    request.open('GET', requestURL);
    request.responseType = 'json';
    request.send();

    lblStatus.innerHTML = '正在更新...'
    btn.disabled = true
    
    request.onload = function() {
        var resp = request.response;
        
        var list = Object.values(resp)
        list.sort(function(x,y){ return y.profit-x.profit; })
        
        new_tbd = document.createElement('tbody')
        for(var i=0;i<list.length;i++){
            sch = list[i]

            row = new_tbd.insertRow()
            row.insertCell().innerHTML = sch.name.replace(/\$\$/g, '→')
            row.insertCell().innerHTML = tmstr(sch.time)
            row.insertCell().innerHTML = '$'+sch.total_money
            row.insertCell().innerHTML = sch.buy_amount.toFixed(4)
            row.insertCell().innerHTML = '$'+sch.sell_money.toFixed(2)
            row.insertCell().innerHTML = sch.profit.toFixed(4)
        }
        tbl.replaceChild(new_tbd, tbd)
        tbd = new_tbd

        lblStatus.innerHTML = '上次更新：'+ new Date().toLocaleTimeString()
        btn.disabled = false
    }
}

function startTimer(){
    if(chkAutoRefresh.checked){
        var refreshInterval = parseFloat(txtRefreshInterval.value)
        if (isNaN(refreshInterval) || refreshInterval<=0){
            alert('请输入正确数值');
            refreshInterval = 3  // 默认值
            txtRefreshInterval.value = 3
        }
        nTimer = setInterval(refresh, refreshInterval * 1000)
    }
    else{
        clearInterval(nTimer)
    }
}

function tmstr(totalSec){
    tm = new Date()
    tm.setTime(sch.time * 1000)

    function addZero(n){
        if(n<10) return '0'+n;
        else return ''+n;
    }
    return tm.getHours()+':'+addZero(tm.getMinutes())+':'+addZero(tm.getSeconds());
}
