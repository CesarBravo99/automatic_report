function openGrid(event, gridName) {
    /*
    Show the grid of the selected section
    */ 

    var tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    var tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(gridName).style.display = "block";
    event.currentTarget.className += " active";
    clicked_system = gridName
    refeshIcons();
}