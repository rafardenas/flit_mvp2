function statusWatcher() {
    var estatus = document.getElementById("demo").innerHTML;
    return estatus
}

var estatus = statusWatcher();
var dictStatus = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
}

var p_bar = document.getElementById("1").innerHTML;
var length = Object.keys(dictStatus).length


var i = 0;
var counter = 0;

while (i <= length) {
    if (i <= estatus) {
        var iid = counter.toString();
        code = dictStatus[iid];
        document.getElementById(code).className = "active";
        if (code == 3) {
            document.getElementById("3").innerHTML += ' (Ver más)';
        }
        if (code == 6) {
            document.getElementById("6").innerHTML += " (Ver prueba de entrega)";
        }

    } else {
        var iid = counter.toString();
        code = dictStatus[iid];
        document.getElementById(code).className = "inactive";
        document.getElementById(code+"a").href = "#!";
        
    }
    counter = counter+1;
    i++;
}



