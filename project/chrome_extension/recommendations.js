document.addEventListener('DOMContentLoaded', function () {
	var xhttp = new XMLHttpRequest();
  	xhttp.onload = function() {
	    if (this.readyState == 4 && this.status == 200) {
	      document.getElementById("body").innerHTML = this.responseText;
	    }
  	};
  	xhttp.open("GET", "http://localhost:5000/");
  	xhttp.send();
});