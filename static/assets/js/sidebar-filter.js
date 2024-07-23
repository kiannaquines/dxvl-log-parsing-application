function filter_sidebar() {
    var filter = document.querySelector("#search_input").value.toUpperCase();
    var ul = document.querySelector("#menu-list");
    var li = ul.querySelectorAll(".menu-item");
    var liHeader = ul.querySelectorAll(".menu-header");
    var txtValue;
    var i, j;
    var hasVisibleItems = false;

    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
            hasVisibleItems = true;
        } else {
            li[i].style.display = "none";
        }
    }

    for (j = 0; j < liHeader.length; j++) {
        var nextSibling = liHeader[j].nextElementSibling;
        var headerHasVisibleItems = false;

        while (nextSibling && nextSibling.classList.contains("menu-item")) {
            if (nextSibling.style.display !== "none") {
                headerHasVisibleItems = true;
                break;
            }
            nextSibling = nextSibling.nextElementSibling;
        }

        if (headerHasVisibleItems) {
            liHeader[j].style.display = "";
        } else {
            liHeader[j].style.display = "none";
        }
    }
}