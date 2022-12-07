
/*   ======  Input Number Only  =====   */

$('.number_only').bind('keyup paste', function () {
    this.value = this.value.replace(/[^0-9]/g, '');
});

/*   ======  Alert Message Set timeout function  =====   */

setTimeout(function () {
    if ($('#msg').length > 0) {
        $('#msg').remove();
    }
}, 2000)

/*   ======  Show Image  =====   */
imgInp.onchange = evt => {
    const [file] = imgInp.files
    if (file) {
        imagepreview.src = URL.createObjectURL(file)
    }
}   
/* var fnf = document.getElementById("aadharnumber");
fnf.addEventListener('keyup', function(evt){
    var n = parseInt(this.value.replace(/(\d{4})(\d{4})(\d{4})/, "$1-$2-$3"));
    fnf.value = n.toLocaleString();
}, false); 
 
 $('.licensenumberformat').keyup(function (event) {
    addSpace(this);
  });*/


$(document).ready(function () {
    $('.aadharnumberformat').keyup(function (event) {
        addHyphen(this);
    });
    $('.mobilenumberformat').keyup(function (event) {
        addSpace(this);
    });
    // $('.licensenumberformat').keyup(function (event) {
    //     var dd = $('.licensenumberformat').val()
    //     alert(dd);
    // });
    $('.licensenumberformat').inputmask("TN9999999999999");

});
function addHyphen(element) {
    let val = $(element).val().split('-').join('');   // Remove dash (-) if mistakenly entered.

    let finalVal = val.match(/.{1,4}/g).join(' ');    // Add (-) after 4rd every char.
    $(element).val(finalVal);		// Update the input box.
};
function addSpace(element) {
    let val = $(element).val().split('-').join('');   // Remove dash (-) if mistakenly entered.

    let finalVal = val.match(/.{1,5}/g).join(' ');    // Add (-) after 4rd every char.
    $(element).val(finalVal);		// Update the input box.
};
