var userid = document.getElementById("userid").innerHTML;

var Url = "https://2d9a621b.ngrok.io/"

var myNodelist = document.getElementsByTagName("LI");
for (var i = 0; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

var close = document.getElementsByClassName("close");
for (var i = 0; i < close.length; i++) {
  close[i].onclick = function() {
    var div = this.parentElement;
	var divs = div.getElementsByTagName("div");
	$.get(url + "delete" + "?" + "pokeid" + "=" + divs[3].innerHTML);
    div.style.display = "none";
  }
}

function newElement() {
  var li = document.createElement("li");
  var inputValue = document.getElementById("myInput").value;
  var t = document.createTextNode(inputValue);
  li.appendChild(t);
  if (inputValue === '') {
    alert("You must write someone's name");
  } else {
    document.getElementById("myOL").appendChild(li);
  }
  var textx = document.getElementById("myText").value;
  var timex = document.getElementById("myTime").value;
  var datex = document.getElementById("myDate").value;

  var fd = new FormData();
  fd.append("userid", userid);
  fd.append("myInput", inputValue);
  fd.append("myText", textx);
  fd.append("myTime", timex);
  fd.append("myDate", datex);
  fd.append("myFile", "");

  jQuery.ajax({
    url: Url + "add",
    data: fd,
    cache: false,
    contentType: false,
    processData: false,
    type: 'POST',
    success: function(){
        console.log("sucess");
    }
  });

  $.ajax({
    url: Url + "upload", 
    type: 'POST',
    data: new FormData($('#myFile')[0]), 
    processData: false
  }).done(function(){
  console.log("Success2");
  })

  document.getElementById("myInput").value = "";
  document.getElementById("myText").value = "";
  document.getElementById("myTime").value = "";
  document.getElementById("myDate").value = "";
  document.getElementById("myFile").value = "";

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      var div = this.parentElement;
      div.style.display = "none";
    }
  }
}
