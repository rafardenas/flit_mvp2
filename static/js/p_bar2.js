function statusWatcher() {
    var estatus = document.getElementById("demo").innerHTML;
    return estatus
}

var estatus = statusWatcher();
var dictStatus = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
}

var p_bar = document.getElementById("1").innerHTML;
var length = Object.keys(dictStatus).length


var i = 1;
var counter = 1;

while (i <= length) {
    if (i <= estatus) {
        var iid = counter.toString();
        code = dictStatus[iid];
        document.getElementById(code).className = "active";
    } else {
        var iid = counter.toString();
        code = dictStatus[iid];
        document.getElementById(code).className = "inactive";
        
    }
    counter = counter+1;
    i++;
}



