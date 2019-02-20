$(function () {

  $('body').on(click, '#registerBttn', function (e) {

    e.preventDefault();
    var names = document.getElementById('regName').value;
    var emails = document.getElementById('regEmail').value;
    var passwords = document.getElementById('regPasswd').value;

    $.ajax({
      type: 'post',
      url: '/apl/auth/register',
      data: {name: names, email: emails, password: passwords},
      success: function () {
        alert('form was submitted');
      }
    });

  });

});
