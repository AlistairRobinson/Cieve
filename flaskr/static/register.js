$(function () {

  $('body').on(click, '#registerBttn', function (e) {

    e.preventDefault();
    var names = document.getElementById('regName').value;
    var emails = document.getElementById('regEmail').value;
    var passwords = document.getElementById('regPasswd').value;
    var token = document.getElementById('_csrf_token').value;

    $.ajax({
      type: 'post',
      url: '/apl/auth/register',
      header: {'_csrf_token': token},
      data: {name: names, email: emails, password: passwords},
      success: function () {
        alert('form was submitted');
      }
    });

  });

});
