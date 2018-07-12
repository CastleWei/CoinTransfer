var lblStatus = document.getElementById('status');
var chkAutoRefresh = document.getElementById('auto-refresh');
var txtRefreshInterval = document.getElementById('refresh-interval');
var btn = document.getElementById('refresh-now');
// var tbd = document.getElementById('result');
// var tbl = document.getElementById('table');

var nTimer = 0;
var isEditing = false;

btn.onclick = refresh;
chkAutoRefresh.onclick = startTimer;

refresh();  // 先自动刷新一次
startTimer();


// 修改设置部分
$('#btnChangeSetting').click(function(){
    if(!isEditing){
        $('#setting-table input').attr('disabled', false);
        $('#btnChangeSetting').text('提交修改');
        $('#lblPasswordPrompt').show();
        isEditing = true;
    }
    else{
        if($.trim($('#inpPassword').val())==''){
            alert('请输入密码！');
            return;
        }

        data = {
            prepared_money: parseFloat($('#form-setting [name=prepared-money]').val()),
            operation_interval: parseFloat($('#form-setting [name=operation-interval]').val()),
            profit_threshold: parseFloat($('#form-setting [name=profit-threshold]').val()),
            password: $('#form-setting [name=password]').val()
        }

        if(!data.prepared_money || !data.operation_interval || !data.profit_threshold){
            alert('无效设置！');
        }

        $('#setting-table input').attr('disabled', true);
        $('#btnChangeSetting').attr('disabled', true);
        $('#lblPasswordPrompt').hide();
        $('#lblWaiting').show();
        $('#form-setting #inpPassword').val('');
        isEditing = false;

        $.post('/post-setting', data, function(result){
            $('#btnChangeSetting').text('修改设置');
            $('#btnChangeSetting').attr('disabled', false);
            $('#lblWaiting').hide();

            if(result==='ok'){
                alert('提交成功');
            }
            else{
                alert('提交失败。'+result);
            }
        });
    }
})


// 以下为函数声明部分

function refresh(){
    var requestURL = 'data.json';
    var request = new XMLHttpRequest();
    request.open('GET', requestURL);
    request.responseType = 'json';
    request.send();

    lblStatus.innerHTML = '正在更新...';
    btn.disabled = true;
    
    request.onload = function() {
        var resp = request.response;

        inflateTable(document.getElementById('market-table'), resp['market'], 
            function(x,y){ return (x.platform_name+x.coin).localeCompare(y.platform_name+y.coin); },
            inflateMarketTable
        );

        inflateTable(document.getElementById('result-table'), resp['result'], 
            function(x,y){ return y.profit - x.profit; },
            inflateResultTable
        );
        
        if(!isEditing){
            fm = document.forms['form-setting']
            fm['prepared-money'].value = resp['setting']['预备资金']
            fm['operation-interval'].value = resp['setting']['查询间隔']
            fm['profit-threshold'].value = resp['setting']['操作阈值']
        }

        lblStatus.innerHTML = '上次更新：'+ new Date().toLocaleTimeString();
        btn.disabled = false;
    }
}


function inflateTable(viewTable, data, sorting, how){
    var list = new Array();
    for(var key in data){
        list.push(data[key]);
    }
    list.sort(sorting);
    
    var new_tbd = document.createElement('tbody');
    how(new_tbd, list);
    viewTable.replaceChild(new_tbd, viewTable.querySelector('tbody'));
}


function inflateMarketTable(new_tbd, list){
    var i = 0
    for(var j = 0; j<list.length; j++){
        var info = list[j]

        row = new_tbd.insertRow()
        row.insertCell().innerHTML = ++i  // 序号
        row.insertCell().innerHTML = info.platform_name+': '+info.coin
        row.insertCell().innerHTML = tmstr(info.time)
        row.insertCell().innerHTML = info.usdt_buy_price
        row.insertCell().innerHTML = info.usdt_sell_price
        row.insertCell().innerHTML = addPairs(info['卖盘'], 4)
        row.insertCell().innerHTML = addPairs(info['买盘'], 4)
    }
}


function inflateResultTable(new_tbd, list){
    for(i=0;i<list.length;i++){
        var item = list[i]
        row = new_tbd.insertRow();
        row.insertCell().innerHTML = i+1;  // 序号
        row.insertCell().innerHTML = item.name.replace(/\$\$/g, '→');
        row.insertCell().innerHTML = tmstr(item.time);
        row.insertCell().innerHTML = item.src_price.toFixed(2);
        row.insertCell().innerHTML = item.dst_price.toFixed(2);

        profitCell =  row.insertCell()
        if(item.profit > document.forms['form-setting']['profit-threshold'].value){
            profitCell.className = 'profit-good';
        }
        // else if(item.profit < -70){
        //     profitCell.className = 'profit-bad';
        // }
        profitCell.innerHTML = item.profit.toFixed(2);
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


function maxPrecision(num, precision){
    var nstr = num.toPrecision(precision);
    if(nstr.indexOf('.') === -1) return nstr;
    var i = nstr.length - 1;
    while(i>0 && nstr.charAt(i)==='0'){
        i--;
    }
    if(nstr.charAt(i)==='.') i++
    return nstr.slice(0, i+1);
}


function addPairs(pairList, n){
    var ret = pairList[0][0].toPrecision(6) + ' - ' +  maxPrecision(pairList[0][1], 3)
    for(var i = 1; i < n; i++){
        ret += '<br>' + pairList[i][0].toPrecision(6) + ' - ' +  maxPrecision(pairList[i][1], 3)
    }
    return ret
}


function tmstr(totalSec){
    var tm = new Date()
    tm.setTime(totalSec * 1000)

    function addZero(n){
        if(n<10) return '0'+n;
        else return ''+n;
    }
    return tm.getHours()+':'+addZero(tm.getMinutes())+':'+addZero(tm.getSeconds());
}
