// function launched when empty viewlet is loaded (before complete document ready)
function initPlonethemeImioapps() {
    resizeHeader();
    highlightTest();
}

// as header is fixed, we need to compute emptyviewlet height dynamically
// in case header is two lines high
// generate CSS for the faceted table header as sticky behavior needs a fixed "top" value in px
function resizeHeader() {
    portal_header_height = $("#portal-header").height();
    $("#emptyviewlet").height(portal_header_height);
    var sheet = document.createElement('style');
    sheet.innerHTML = "table.faceted-table-results th {top: " + portal_header_height + "px;}";
    document.body.appendChild(sheet);
}
$(window).resize(resizeHeader);

// when using a imio-test instance, highlight header
function highlightTest() {
    var url = $("link[rel='canonical']").attr('href');
    if (url.includes('imio-test') || url.includes('preprod')) {
        $("div#portal-header")[0].style.background = "#d00";
    }
}

var isChrome = /chrom/.test(navigator.userAgent.toLowerCase());
var isFirefox = /firefox/.test(navigator.userAgent.toLowerCase());

$(document).ready(function () {
    if (isChrome) {
        document.body.classList.add('using-chrome');
    }
    if (isFirefox) {
        document.body.classList.add('using-firefox');
    }
});
