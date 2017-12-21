// execute when the DOM is fully loaded
$(document).ready(function() {

    var checkBoxData = document.getElementById("checkbox-data");

    var africa = checkBoxData.dataset.africa;
    var americas = checkBoxData.dataset.americas;
    var asiaPacific = checkBoxData.dataset.asiapacific;
    var europe = checkBoxData.dataset.europe;
    var middleEast = checkBoxData.dataset.middleeast;
    var travel = checkBoxData.dataset.travel;

    if(africa == 1)  {

            document.getElementById("0").checked = true;
    }

    else {
            document.getElementById("0").checked = false;
    }

    if(americas == 1)  {

            document.getElementById("1").checked = true;
    }

    else {
            document.getElementById("1").checked = false;
    }

    if(asiaPacific == 1)  {

            document.getElementById("2").checked = true;
    }

    else {
            document.getElementById("2").checked = false;
    }

    if(europe == 1)  {

            document.getElementById("3").checked = true;
    }

    else {
            document.getElementById("3").checked = false;
    }

    if(middleEast == 1)  {

            document.getElementById("4").checked = true;
    }

    else {
            document.getElementById("4").checked = false;
    }

    if(travel == 1)  {

            document.getElementById("5").checked = true;
    }

    else {
            document.getElementById("5").checked = false;
    }

    $("#submitBtn").click(function() {
        $.ajax({
            type: "POST",
            url: "/",
            contentType: "application/json; charset=utf-8",
            success: function(data) {
                articleString = '<div class="row">' +
                                    '<div class="col-xs-2 text-left"></div>' +
                                    '<div class="col-xs-6 text-left">Your random article:</div>' +
                                '</div>' +
                                '<div class="row">' +
                                    '<div class="col-xs-2 text-left">Title: </div>' +
                                    '<div class="col-xs-6 text-left"><a href=\"' + data[0].link + '\" target=\"_blank\"\>' + data[0].title + '</a></div>' +
                                '</div>' +
                                '<div class="row">' +
                                    '<div class="col-xs-2 text-left">Description: </div>' +
                                    '<div class="col-xs-6 text-left">' + data[0].description + '</a></div>' +
                                '</div>' +
                                '<div class="row">' +
                                    '<div class="col-xs-2 text-left">Date: </div>' +
                                    '<div class="col-xs-6 text-left">' + data[0].date + '</a></div>' +
                                '</div>'
                $('#getArticleResult').html(articleString);
            }

        })
    })

  });

function  toggle_select(id) {

    var X = document.getElementById(id);
    if (X.checked == true) {
     X.value = 1;
    }
    else {
    X.value = 0;
    }
    var category=X.id;
    var chk=X.value;

    var parameters = {
        category: X.id,
        chk : X.value
    };

     $.getJSON(Flask.url_for("update"), parameters);

}


