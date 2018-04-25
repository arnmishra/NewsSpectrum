function checkLoggedIn(domain, name, callback) {
    chrome.cookies.get({"url": domain, "name": name}, function(cookie) {
        if (cookie != null && cookie.value != undefined) {
          callback(true);
        } else {
          callback(false);
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {

	checkLoggedIn("http://localhost", "remember_token", function(logged_in) {
	    if(logged_in) {
	     	var xhttp = new XMLHttpRequest();
  			xhttp.onload = function() {
		    	if (this.readyState == 4 && this.status == 200) {
		      		document.getElementById("body").innerHTML = this.responseText;
		    	}
  			};
  			xhttp.open("GET", "http://localhost:5000/");
  			xhttp.send();
	    } else {
	    	console.log('here')
	    	document.getElementById("header").style.display = "block";
	    	document.getElementById("header_2").style.display = "block";
	    }
   });
});