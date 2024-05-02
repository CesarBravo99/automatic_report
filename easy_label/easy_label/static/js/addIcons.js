
function refeshIcons(){
    document.querySelectorAll("[id=image-container-" + clicked_system + "]").forEach((template) => {
        while (template.children.length > 1) {
            template.removeChild(template.lastChild)
        }
    });
    
    const module = (document.getElementById("modules-dropdown").value - 1).toString();
    const center = document.getElementById("centers-dropdown").value;
    const separator = document.getElementById("mamparos-dropdown").value;
    const jail = document.getElementById("peceras-dropdown").value;

    for(i = 0; i < imgs_name.length; i++){

        if (imageMetaData.icon[imgs_name[i]].span != null &&  
            imageMetaData.icon[imgs_name[i]].module == module &&
            imageMetaData.icon[imgs_name[i]].center == center ){
            if (imageMetaData.icon[imgs_name[i]].system == clicked_system) {
                if (imageMetaData.icon[imgs_name[i]].separator == 'None' || 
                    imageMetaData.icon[imgs_name[i]].separator == separator) {
                imageMetaData.icon[imgs_name[i]].template.appendChild(imageMetaData.icon[imgs_name[i]].span)
                } else if (imageMetaData.icon[imgs_name[i]].jail == jail) {
                    imageMetaData.icon[imgs_name[i]].template.appendChild(imageMetaData.icon[imgs_name[i]].span)
                } else {
                    imageMetaData.icon[imgs_name[i]].template.appendChild(imageMetaData.icon[imgs_name[i]].span)
                }   
            }
        }
    }
}

function refreshFrames(img_name){
    var thumbnail = document.querySelector(`.image-item img[src$='media/${hash}/imgs/${img_name}']`).parentElement;
    while (thumbnail.children.length > 1) {
        thumbnail.removeChild(thumbnail.lastChild)
    }
    thumbnail.appendChild(imageMetaData.icon[img_name].thumbnail);
    // document.querySelector(`.image-item img[src$='media/${hash}/imgs/${img_name}']`).parentElement.style.border = "2px solid black";
};
