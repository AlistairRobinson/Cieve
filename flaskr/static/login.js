$(function () {

  $('body').on(click, '#loginButton', function (e) {

    e.preventDefault();
    var emails = document.getElementById('emailBox').value;
    var passwords = document.getElementById('passwdBox').value;
    var token = document.getElementById('_csrf_token').value;

    $.ajax({
      type: 'post',
      url: '/apl/auth/login',
      header: {'_csrf_token': token},
      data: {email: emaisl, email: passwords},
      success: function () {
        alert('form was submitted');
      }
    });

  });

});
