document.addEventListener("DOMContentLoaded", function(event) {
    var inputs = document.getElementsByClassName("form-group");
    var mathCheck = document.getElementById('math-text')
    var normCheck = document.getElementById('normal-text')
    mathCheck.addEventListener('change', function() {
      if (mathCheck.checked) {
         for(var i = 0; i < inputs.length; i++) {
        var myname = inputs[i].getAttribute("name");
        if(myname.indexOf('qm') == 0) {
            inputs[i].style.visibility = 'visible';
        }
        if(myname.indexOf('am') == 0) {
            inputs[i].style.visibility = 'visible';
        }
        }
    }
        else{
            for (var i = 0; i < inputs.length; i++) {
            var myname = inputs[i].getAttribute("name");
            if (myname.indexOf('qm') == 0) {
                inputs[i].style.visibility = 'hidden';
            }
            if (myname.indexOf('am') == 0) {
                inputs[i].style.visibility = 'hidden';
            }
        }

    }
    });
    normCheck.addEventListener('change', function() {
      if (normCheck.checked) {
         for(var i = 0; i < inputs.length; i++) {
        var myname = inputs[i].getAttribute("name");
        if(myname.indexOf('qt') == 0) {
            inputs[i].style.visibility = 'visible';
        }
        if(myname.indexOf('at') == 0) {
            inputs[i].style.visibility = 'visible';
        }
        }
    }
        else{
            for (var i = 0; i < inputs.length; i++) {
            var myname = inputs[i].getAttribute("name");
            if (myname.indexOf('qt') == 0) {
                inputs[i].style.visibility = 'hidden';
            }
            if (myname.indexOf('at') == 0) {
                inputs[i].style.visibility = 'hidden';
            }
        }

    }
    });
});