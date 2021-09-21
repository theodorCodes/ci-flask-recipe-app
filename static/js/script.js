$(document).ready(function () {
    // Materialize/jQuery - Collapsible mobile menu
    $(".sidenav").sidenav({edge: "right"});
    // Desktop menu - dropdown
    $(".dropdown-trigger").dropdown({hover: false});
    // Select - in recipe edit
    $('select').formSelect();
});

