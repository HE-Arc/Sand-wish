/**
 * Submit post on submit
 * @param {int} giftId : gift's id
 * @param {String} crsftoken : contribution form's crsf token
 */
function contributionSubmit(giftId, csrf_token) {
    if (event)
        event.preventDefault();
    create_contribution(giftId, csrf_token);
}

/**
 * AJAX for posting
 * @param {int} giftId : gift's id
 * @param {String} crsftoken : contribution form's crsf token
 */
function create_contribution(giftId, csrf_token) {
    valueFieldName = "#contribution" + giftId;

    $.ajax({
        url : "/contribution/create/",
        type : "POST",
        data : {
            "value": $(valueFieldName).val(),
            "giftId": giftId,
            "csrfmiddlewaretoken": csrf_token
        },

        // handle a successful response
        success : function(json) {
            // console.log(json); // log the returned json to the console
            if (json.result == "success"){
                $("#full_contribution" + giftId).text(json.new_total_contribution);
            }
            else if (json.result == "fail"){
                $(valueFieldName).val(json.old_value);
                $('#contribution-error' + giftId).text(json.error_message);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("fail");
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
