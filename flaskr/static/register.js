$(function () {

  $('body').on(click, '#registerBttn', function (e) {

    e.preventDefault();
    var names = document.getElementById('regName').value;
    var emails = document.getElementById('regEmail').value;
    var passwords = document.getElementById('regPasswd').value;
    var token = document.getElementById('_csrf_token').value;

    var regex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
    if (!regex.test(passwords)) {
      //Feed back to user that password is too weak
    } else {
      $.ajax({
        type: 'post',
        url: '/apl/auth/register',
        data: {name: names, email: emails, password: passwords, _csrf_token: token},
        success: function () {
          alert('form was submitted');
        }
      });
    }
  });

});
