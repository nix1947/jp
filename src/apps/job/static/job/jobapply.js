 {% if  request.user.is_authenticated %}
         window.isAuthenticated = true;

        {%else %}
         window.isAuthenticated = false;

    {% endif %}



  function jobApply() {




    if(!isAuthenticated) {
        alert('not auth');
        window.location.href='/account/jobseeker/login';
     } else {
        // call ajax to job Apply
        alert('calling ajax');
      }
  }