function checkLoggedIn(domain, name, callback) {
    chrome.cookies.get({"url": domain, "name": name}, function(cookie) {
        if (cookie != null && cookie.value != undefined) {
          callback(true);
        } else {
          callback(false);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
   checkLoggedIn("http://localhost", "remember_token", function(logged_in) {
    if(logged_in) {
      var logged_in_label = document.getElementById("logged_in");
      logged_in_label.style.display = "block";
    } else {
      var not_logged_in_label = document.getElementById("not_logged_in");
      not_logged_in_label.style.display = "block";
    }

   });
}, false);
