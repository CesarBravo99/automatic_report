
function addIcon(icon){
};

function createIcon(emoji, placementData) {
    const icon = document.createElement("span");
    icon.className = "icon-class";
    icon.textContent = emoji;
    icon.style.position = "absolute";
    return icon;
}
