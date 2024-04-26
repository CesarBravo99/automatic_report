
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

    // TODO: Reinciar todo cuando se cambie de centro.
    
    for(i = 0; i < imgs_name.length; i++){

        if (imageMetaData[imgs_name[i]].icon.span != null &&  
            imageMetaData[imgs_name[i]].icon.module == module &&
            imageMetaData[imgs_name[i]].icon.center == center ){
            if (imageMetaData[imgs_name[i]].icon.system == clicked_system) {
                if (imageMetaData[imgs_name[i]].icon.separator == 'None' || 
                    imageMetaData[imgs_name[i]].icon.separator == separator) {
                imageMetaData[imgs_name[i]].icon.template.appendChild(imageMetaData[imgs_name[i]].icon.span)
                } else if (imageMetaData[imgs_name[i]].icon.jail == jail) {
                    imageMetaData[imgs_name[i]].icon.template.appendChild(imageMetaData[imgs_name[i]].icon.span)
                } else {
                    imageMetaData[imgs_name[i]].icon.template.appendChild(imageMetaData[imgs_name[i]].icon.span)
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
    thumbnail.appendChild(imageMetaData[img_name].icon.thumbnail);
    // document.querySelector(`.image-item img[src$='media/${hash}/imgs/${img_name}']`).parentElement.style.border = "2px solid black";
};
