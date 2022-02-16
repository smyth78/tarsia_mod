document.addEventListener("DOMContentLoaded", function(event) {
    // this is to change the visibility of the inoput boxes -> needs improvement
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

    // this is to check to see which shaped jigsaw is suitable
    var question_number = document.getElementById('size').getAttribute('value');
    var squareCheckDiv = document.getElementById('jigsaw-shape-square-div')
    var squareCheck = document.getElementById('jigsaw-shape-square')
    var triCheckDiv = document.getElementById('jigsaw-shape-tri-div')
    var triCheck = document.getElementById('jigsaw-shape-tri')
    const squareValues = ['4', '12', '24', '40']
    const triValues = ['3', '9', '18', '30']
    if (squareValues.includes(question_number) === true){
        squareCheckDiv.style.visibility = 'visible';
        squareCheck.checked = true;
    };
    if (triValues.includes(question_number) === true){
        triCheckDiv.style.visibility = 'visible';
        triCheck.checked = true;
    };

    // // this code makes the jigsaw sahpe type div hidden when jigsaw NOT sleected
    // var treasureButton = document.getElementById('treasure');
    // var worksheetButton = document.getElementById('worksheet');
    // var jigsawButton = document.getElementById('tarsia');
    // var jigShapeDiv = document.getElementById('jig-shape-div');
    // console.log(jigShapeDiv);
    //
    //
    // jigsawButton.addEventListener('change', function() {
    //     console.log('jig');
    //     jigShapeDiv.style.visibility = 'visible';
    // })
    // treasureButton.addEventListener('change', function() {
    //     console.log('trea');
    //     jigShapeDiv.style.visibility = 'hidden';
    // })
    // worksheetButton.addEventListener('change', function() {
    //     console.log('work');
    //     jigShapeDiv.style.visibility = 'hidden';
    // })
});