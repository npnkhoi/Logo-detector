"use strict";
var time_interval = 500;
var counter = 0, ok_value = 0, ng_value = 0;

function changeFileName() {
    var image1 = new Image();
    var image2 = new Image();
    var imageName1 = counter + "_OK.jpg";
    var imageName2 = counter + "_NG.jpg";
    image1.src = imageName1;
    if (image1.width === 0) { //there is no ok image
        image2.src = imageName2; 
        if (image2.width !== 0) { //there is ng image
            document.getElementById("Img_in").src = imageName2;
            document.getElementById("Img_in").style.border = "thick solid #FF0000";
            document.getElementById("Img_in").style.height = "200px";
            document.getElementById("Img_in").style.width = "300px";
            document.getElementById("Result_text").innerHTML = "NOTGOOD";
            document.getElementById("time").innerHTML = new Date();
            document.getElementById("file_name").innerHTML = imageName2;
            counter += 1;
            ng_value += 1;
            document.getElementById("notgood").innerHTML = ng_value;
        }
    }
    else {//there is ok image
        document.getElementById("Img_in").src = imageName1;
        document.getElementById("Img_in").style.border = "thick solid #008800";
        document.getElementById("Img_in").style.height = "200px";
        document.getElementById("Img_in").style.width = "300px";
        document.getElementById("Result_text").innerHTML = "OKAY";
        document.getElementById("time").innerHTML = new Date();
        document.getElementById("file_name").innerHTML = imageName1;
        counter += 1;
        ok_value += 1;
        document.getElementById("okay").innerHTML = ok_value;
    }
    document.getElementById("counter").innerHTML = counter;
}

function Init() {
    window.setInterval(changeFileName, time_interval);
    document.getElementById("time").innerHTML = new Date();
}