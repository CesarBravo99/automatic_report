function refreshIcons(){
    document.querySelectorAll(".image-container").forEach((template) => {
        while (template.children.length > 1) {
            template.removeChild(template.lastChild)
        }
    });
    
    const module = (document.getElementById("modules-dropdown").value - 1).toString();
    const center = document.getElementById("centers-dropdown").value;
    const separator = document.getElementById("mamparos-dropdown").value;
    var jail = document.getElementById("peceras-dropdown").value;

    document.getElementById('images-container').style.height = `${window.innerHeight*0.625}px`

    for(i = 0; i < imgs_name.length; i++){

        if (imageMetaData.icon[imgs_name[i]].span != null &&  
            imageMetaData.icon[imgs_name[i]].module == module &&
            imageMetaData.icon[imgs_name[i]].center == center &&
            imageMetaData.icon[imgs_name[i]].system == clicked_system){
            refreshIcon(imageMetaData.icon[imgs_name[i]]);

            if (imageMetaData.icon[imgs_name[i]].system == 'tensores'){
                imageMetaData.icon[imgs_name[i]].template.appendChild(imageMetaData.icon[imgs_name[i]].span)
            } else if (imageMetaData.icon[imgs_name[i]].system == 'pecera' &&
                        imageMetaData.icon[imgs_name[i]].jail == jail) {
                imageMetaData.icon[imgs_name[i]].template.appendChild(imageMetaData.icon[imgs_name[i]].span)
            } else if (imageMetaData.icon[imgs_name[i]].system == 'lobera' && (
                        imageMetaData.icon[imgs_name[i]].separator == 'None' || 
                        imageMetaData.icon[imgs_name[i]].separator == separator) ){
                imageMetaData.icon[imgs_name[i]].template.appendChild(imageMetaData.icon[imgs_name[i]].span)
            };
        };
    };
};


function refreshIcon(icon){
    const templateBBox = icon.template.children[0].getBoundingClientRect();
    var iconWidth = window.innerWidth / 50;
    var iconHeight = window.innerHeight / 50;
    var centerX = 0
    var centerY = 0

    if (icon['type'] == 'correct'){centerX = templateBBox.left + window.scrollX + icon['x'] - iconWidth * 4/ 11} 
    else {centerX = templateBBox.left + window.scrollX + icon['x'] - iconWidth / 2};
    centerY = templateBBox.top + window.scrollY + icon['y'] - iconHeight ;
    icon.span.style.left = `${centerX}px`;
    icon.span.style.top = `${centerY}px`;
    icon.span.style.width = `${iconWidth}px`;
    icon.span.style.height = `${iconHeight}px`;

}


function refreshFrames(img_name){
    var thumbnail = document.querySelector(`.image-item img[src$='media/${hash}/images/${img_name}']`).parentElement;
    while (thumbnail.children.length > 1) {
        thumbnail.removeChild(thumbnail.lastChild)
    }
    thumbnail.appendChild(imageMetaData.icon[img_name].thumbnail);
    // document.querySelector(`.image-item img[src$='media/${hash}/imgs/${img_name}']`).parentElement.style.border = "2px solid black";
};


window.addEventListener('resize', refreshIcons)