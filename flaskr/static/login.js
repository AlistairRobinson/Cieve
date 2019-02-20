$(function () {

  $('body').on(click, '#loginButton', function (e) {

    e.preventDefault();
    var emails = document.getElementById('emailBox').value;
    var passwords = document.getElementById('passwdBox').value;

    $.ajax({
      type: 'post',
      url: '/apl/auth/login',
      data: {email: emaisl, email: passwords},
      success: function () {
        alert('form was submitted');
      }
    });

  });

});
