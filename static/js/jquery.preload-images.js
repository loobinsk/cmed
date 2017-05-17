jQuery.preloadImages = function () {
    var images = (typeof arguments[0] == 'object') ? arguments[0] : arguments;
    for (var i = 0; i < images.length; i++) {
        jQuery("<img>").attr("src", images[i]);
    }
}