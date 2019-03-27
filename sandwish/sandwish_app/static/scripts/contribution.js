// Submit post on submit
function contributionSubmit(giftId, last_value, csrf_token)
{
    if (event){
        event.preventDefault();
    }
    create_contribution(giftId, last_value, csrf_token);
}

// AJAX for posting
function create_contribution(giftId, last_value, csrf_token) {
    valueFieldName = '#contribution' + giftId;
    console.log(giftId);

    $.ajax({
        url : "/contribution/create/", // the endpoint
        type : "POST", // http method
        data : {'value' : $(valueFieldName).val(), 'giftId' : giftId, 'csrfmiddlewaretoken' : csrf_token}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            if (json.result == "success")
            {
                $("#full_contribution" + giftId).text(json.new_total_contribution);
            }
            else if (json.result == "fail")
            {
                $(valueFieldName).val(json.old_value);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("fail");
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
