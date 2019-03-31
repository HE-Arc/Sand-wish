
$((function() {
    $("#wishlist_creation_form").click(toggleWishlistFormDisplay);
    $("#show_form_button").click(toggleWishlistFormDisplay);
}));

/**
 * Toggles on and off the wishlist form's display attribute.
 */
function toggleWishlistFormDisplay() {
    $("#wishlist_creation_form").toggle();
    $("#show_form_button").toggle();
}