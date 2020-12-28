function login(){
  var username = $("#username").val()
  var password = $("#password").val()

  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "/token",
    "method": "POST",
    "headers": {
      "content-type": "application/x-www-form-urlencoded",
      "cache-control": "no-cache"
    },
    "data": {
      "username": username,
      "password": password
    }
  }

  $.ajax(settings).done(function (response) {
    console.log(response);
    document.cookie = "access_token="+response["access_token"];
    document.cookie = "token_type="+response["token_type"];

    var settings = {
      "url": "/logged",
      "method": "GET",
      "headers": {
        "Authorization": response["token_type"] + " " + response["access_token"]
      }
    }

    $.ajax(settings).done(function (response) {
      var remv = $(".form")
      remv.remove()
      var html = response
      html = $.parseHTML(html)
      $(".content").append(html)
    })
  })
}

function register() {
  var settings = {
    "url": "/register",
    "method": "GET"
  }

  $.ajax(settings).done(function (response) {
    var remv = $(".form")
    remv.remove()
    var html = response
    html = $.parseHTML(html)
    $(".content").append(html)
  })
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function send_registration_data(){
  var username = $("#username").val()
  var password = $("#password").val()
  var name = $("#name").val()
  var email = $("#email").val()

  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "/savenewuser",
    "method": "POST",
    "headers": {
      "content-type": "application/x-www-form-urlencoded",
      "cache-control": "no-cache"
    },
    "data": {
      "username": username,
      "password": password,
      "email": email,
      "full_name": name
    }
  }

  $.ajax(settings).done(function (response) {
    alert(':)')
  })
}

function back() {
  window.location.replace("/");
}
