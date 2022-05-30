function get_exercises(filtertext, filtertype){
    var xml = new XMLHttpRequest()
    var url = "/exercise-get?filtertext="+filtertext+"&filtertype="+filtertype
    console.log(url)
    xml.open("POST", url, true );
    xml.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xml.onload = function(){
        var datareply = JSON.parse(this.responseText)
        console.log(datareply)
    }
    xml.send();
};