const MAXIMUM_NUMBER_SEARCH_RESULTS = 50;
const URL_SEARCH_PAGE = "search";
const IS_ON_SEARCH_PAGE = window.location.href.split("/")[3] == URL_SEARCH_PAGE;

var autocompleteSource = [], searchField;

$(function() {
    searchField = $("#search-field");
    initEvents();

    // if searchbar is not empty and page just loaded : search given username
    if (searchField.val().length > 0)
        $("#search-form").submit();
});

/**
 * Initializes form's events.
 */
function initEvents() {
    $("#search-form").submit(e => e.preventDefault());

    searchField.autocomplete({ source: autocompleteSource });

    // prevent user using illegal characters
    // searchField.keypress(e => {
    //     let kc = e.which;
    //     if (!((kc >= 48 && kc <= 57) || // digits
    //          (kc >= 65 && kc <= 90)  || // letters (uppercase)
    //          (kc >= 97 && kc <= 122) || // letters (lowercase)
    //          kc === 45               || // -
    //          kc === 95               || // _
    //          kc === 13))
    //         e.preventDefault();
    // });

    searchField.keyup(_ => {
        if (searchField.val().length > 0)
            $("#search-form").submit();
        else
            clearSearchResults();
    });

    searchField.on("input", _ => {
        searchField[0].setCustomValidity(""); 
        searchField[0].reportValidity();
    });

    searchField.on("invalid", _ => searchField[0].setCustomValidity("Usernames are 30 characters or fewer. Letters, digits, - and _ only."));
}

/**
 * Submits searchbar form after button click. Redirects user to search page if he's not already there.
 * @param {String} crsftoken : seachbar form's crsf token
 */
function searchBtnClick(crsftoken) {
    if (!IS_ON_SEARCH_PAGE) {
        if (isSearchValid()) {
            $.ajax({
                url: "/search-redirect/",
                type: "POST",
                data: { 
                    search: encodeURIComponent(searchField.val()),
                    csrfmiddlewaretoken: crsftoken 
                },
                success: data => window.location = data.url
            });
        }
    } else
        search(crsftoken);
}

/**
 * Searches for usernames containing given pattern.
 * @param {String} crsftoken : seachbar form's crsf token
 */
function search(crsftoken) {
    if (isSearchValid()) {
        if (event)
            event.preventDefault();
        
        $.ajax({
            url: "/search/",
            type: "POST",
            data: { 
                search : searchField.val(),
                csrfmiddlewaretoken : crsftoken 
            },
            success : json => {
                let results = JSON.parse(json["results"]);
                
                // order results by usernames alphabetical order
                results.sort((a, b) => {
                    let usernameA = a.fields.username.toLowerCase(); 
                    let usernameB = b.fields.username.toLowerCase();
                    return usernameA < usernameB ? 1 : usernameA > usernameB ? -1 : 0;
                });

                // build html results
                let html_result = [];
                autocompleteSource = [];
                for (let i=0; i<results.length && i<MAXIMUM_NUMBER_SEARCH_RESULTS; i++) {
                    html_result.push(buildHtmlSearchResult(results[i].fields));
                    buildAutocompletionSearchResult(results[i].fields);
                }

                // display results
                if (IS_ON_SEARCH_PAGE)
                    displayInHomePage(html_result);
                else
                    searchField.autocomplete({
                        source: (request, response) => { 
                            // source of this trick to set the max number of results : https://stackoverflow.com/a/7617637
                            let results = $.ui.autocomplete.filter(autocompleteSource, request.term);
                            response(results.slice(0, 10));
                        },
                        select: (_, ui) => window.location.href = ui.item.href,
                        minLength: 1
                    });
            }
        });
    }
};

/**
 * Builds and returns html elements for a search result.
 * @param {String} searched_user : username matching seach pattern
 */
function buildHtmlSearchResult(searched_user) {
    let div = $("<div></div>");
    let a = $("<a></a>").attr("href", "/" + encodeURIComponent(searched_user.username) + "/")
                        .text(searched_user.username);
    div.prepend(a);
    return div;
}

/**
 * Builds and appends objects representing a search result to the autocomplete array.
 * @param {String} searched_user : username matching seach pattern
 */
function buildAutocompletionSearchResult(searched_user) {
    let username = htmlEntities(searched_user.username);
    autocompleteSource.push({ href: "/" + encodeURIComponent(searched_user.username) + "/",
                              value: username,
                              label: username 
                            });
}

/**
 * Returns true if the search is valid false otherwise.
 */
function isSearchValid() {
    return searchField.val().length > 0 && 
           searchField.val().split(" ").length <= 1 &&
           $("#search-field")[0].reportValidity();
}

/**
 * Appends search results html in home page div.
 * @param {Array} html_result : array of search results html
 */
function displayInHomePage(html_result) {
    clearSearchResults();
    for (let i=0; i<html_result.length; i++)
        $("#search-results").prepend(html_result[i]);
}

/**
 * Clears home page search results div.
 */
function clearSearchResults() {
    if ($("#search-results"))
        $("#search-results").empty();
}

/**
 * Escapes given string.
 * Source: https://css-tricks.com/snippets/javascript/htmlentities-for-javascript/
 * @param {String} str : string to sanitize
 */
function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}