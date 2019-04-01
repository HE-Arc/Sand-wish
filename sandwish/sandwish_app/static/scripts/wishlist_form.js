
$((function() {
    $("#show_form_button").click(toggleWishlistFormDisplay);
    $("#hide_form_button").click(toggleWishlistFormDisplay);
}));

/**
 * Toggles on and off the wishlist form's display attribute.
 */
function toggleWishlistFormDisplay() {
    $("#show_form_button").toggle();
    $("#wishlist_creation_form").toggle("fast");
}