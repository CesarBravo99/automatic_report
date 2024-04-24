
function refeshIcons(){
    refreshTemplates()
    refreshFrames()
};

function refreshTemplates(){
    for(i = 0; i < imgs_name.length; i++){
        if (imageMetaData[imgs_name[i]]['icon']['icon'] != ''){
            icon = createIcon(imgs_name[i])
            imageMetaData[imgs_name[i]]['icon']['template'].appendChild(icon)
        }
    }
}

function refreshFrames(){

}

function createIcon(img_name) {
    const icon = document.createElement("span");
    icon.className = "icon-class";
    icon.textContent = imageMetaData[img_name]['icon']['icon'];
    icon.style.position = "absolute";
    return icon;
}
