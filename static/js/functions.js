$('document').ready(function () {

    //ADD YEARS TO THE CC DROWPDOWN FOR NEW ADS
    var currentYear = new Date().getFullYear()


    //HOME SEARCH SUBMIT
    $('#homeSearchForm').submit(function (event) {
        if ($("#search").val() == "") {
            event.preventDefault()
        }
        //Sanitize inputs prior to submit
        $("#search").val(sanitize($('#search').val()));
    })

    //EMAIL SIGN-UP IS AN ASYNCH POST
    $('#emailSignUpButton').click(function () {
        if (isEmail($('#emailInput').val())) {
            $.post("/email", {
                email: $('#emailInput').val()
            });
            $("#emailSection").html("<br>Thank you for signing up.")
        } else {
            $('#emailInputHelp').removeClass("is-hidden")
        }
    })


    //New Job Payment Type radio button hide/show
    $("input[name=payment_type]").click(function () {
        if ($("input[name=payment_type]:checked").val() == "CC") {
            $('#CC').removeClass("is-hidden")
        } else {
            $('#CC').addClass("is-hidden")
        };
    })

    //NEW JOB SUBMIT
    $('#newJobForm').submit(function (event) {

        //Get cropped image
        $uploadCrop.croppie('result', {
            type: "base64",
            size: {
                width: 150,
                height: 150
            },
            format: "png",
            quality: 0.9
        }).then(function (resp) {
            $('#imagebase64').val(resp);
        });

        //Job Details check for empty fields
        $.each(['#titleInput', '#jobLocationInput', '#descriptionInput', '#companyInput', '#locationInput'],
            function (index, value) {
                isBlank($(value), $(value + 'Help')) ? event.preventDefault() : 0;
            });

        //CC Payment check for empty fields
        if ($("input[name=payment_type]:checked").val() == "CC") {

            //Check for empty fields
            $.each(['#ccNameInput', '#ccMonthInput', '#ccYearInput'],
                function (index, value) {
                    isBlank($(value), $(value + 'Help')) ? event.preventDefault() : 0;
                });

            //Validate CC number 
            if ($.payform.validateCardNumber($('#ccNumInput').val())) {
                $('#ccNumInputHelp').addClass("is-hidden")
            } else {
                $('#ccNumInputHelp').removeClass("is-hidden");
                event.preventDefault();
            };
            //Validate CCV number
            if ($.payform.validateCardCVC($('#ccvInput').val())) {
                $('#ccvInputHelp').addClass("is-hidden")
            } else {
                $('#ccvInputHelp').removeClass("is-hidden");
                event.preventDefault();
            };
        };

        //Regex checks
        !isURL($('#applyLinkInput'), $('#applyLinkInputHelp')) ? event.preventDefault() : 0;
        !isURL($('#websiteInput'), $('#websiteInputHelp')) ? event.preventDefault() : 0;

        //Sanitize Inputs
        $.each(['#titleInput', '#jobLocationInput', '#descriptionInput', '#applyLinkInput', '#companyInput', '#locationInput', '#websiteInput'],
            function (index, value) {
                $(value).val(sanitize($(value).val()))
            });

        if (!event.isDefaultPrevented()) {
            $('#descriptionInput').val(marked($('#descriptionInput').val()));
        };

    })

    //Hide errors when conditions are met
    $('#emailInput').keyup(function () {
        if (isEmail($('#emailInput').val())) {
            $('#emailInputHelp').addClass("is-hidden")
        }
    })
    $('#passwordMatch').keyup(function () {
        if ($("#passwordInput").val() == $("#passwordMatch").val()) {
            $('#passwordMatchHelp').addClass("is-hidden")
        }
    })
    $('#passwordInput').keyup(function () {
        if (isPassword($("#passwordInput").val())) {
            $('#passwordInputHelp').addClass("is-hidden")
        }
    })

  $('#dismiss-flash').click(function () {
    $('#flash-message').remove()
  })

});

//POSTS
function sendEmailPassword() {
    if (!isEmail($("#emailInput").val())) {
        $('#emailInputHelp').removeClass("is-hidden")
        $('#passwordInputHelp').addClass("is-hidden")
    } else {
        $.post("/login/sign-in.html", {
            reset_email: $('#emailInput').val()
        });
        $("#emailPassword").html("Email has been sent")
    }
}

function deleteJob() {
    $("#deleteJobForm").submit()
}

function goToJobLink(id) {
    $("#job").val(id);
    $("#goToJobForm").submit()
}


function goToEditLink() {
    $("#goToEditForm").submit()
}

function fullSearchFunc() {
    $("#search").val(sanitize($('#search').val()));
    $("#job_location").val(sanitize($('#job_location').val()));
    $("#fullSearchForm").submit()
}

// SANITIZE INPUT
function sanitize(input) {
    var output = input.replace(/<script[^>]*?>.*?<\/script>/gi, '').
    replace(/<[\/\!]*?[^<>]*?>/gi, '').
    replace(/<style[^>]*?>.*?<\/style>/gi, '').
    replace(/<![\s\S]*?--[ \t\n\r]*>/gi, '').
    replace(/ +(?= )/g, '');
    return jQuery.trim(output);
};

//VALIDATIONS

function isBlank(fieldInput, helpInput) {
    var isBlankCheck = fieldInput.val() == "";
    if (isBlankCheck) {
        helpInput.removeClass("is-hidden")
    } else {
        helpInput.addClass("is-hidden")
    }
    return isBlankCheck;
}
