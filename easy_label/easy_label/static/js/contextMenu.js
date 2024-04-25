

document.addEventListener('DOMContentLoaded', function () {

    contextMenuLoberas = document.getElementById('context-menu-lobera');
    contextMenuPeceras = document.getElementById('context-menu-pecera');
    contextMenuTensores = document.getElementById('context-menu-tensores');

    contextMenu = {
        'lobera': contextMenuLoberas,
        'pecera': contextMenuPeceras,
        'tensores': contextMenuTensores,
    }
    
    document.querySelectorAll(".tabcontent").forEach((system) => {
        document.querySelectorAll("[id=image-container-" + system.id + "]").forEach((template) => {
            template.addEventListener("contextmenu", function (event) {
                event.preventDefault();
                if (document.getElementById('selected-image').src.split('/').pop() == 'favicon_cover.png') return;
                menuMetadata = getMenuMetadata(event, system, template);
                showMenu(event, contextMenu[system.id])
            });
            template.addEventListener("click", hideMenu)
        });
        document.querySelectorAll("[id=context-link-" + system.id + ']').forEach((option) => {
            option.addEventListener('click', function(event) {
            const type = this.querySelector("span[role='icon']").ariaLabel;
            const icon = this.querySelector("span[role='icon']").textContent;
            const img_name = document.getElementById('selected-image').src.split('/').pop();
            saveImgMetadata(img_name, menuMetadata, type);
            saveIconMetadata(img_name, menuMetadata, icon);
            refeshIcons(icon);
            hideMenu();
            });
            option.addEventListener('dblclick', function(event) {event.preventDefault()});
        });
    });
});

function getMenuMetadata(event, system, template) {
    const imgRect = template.getBoundingClientRect();
    const x = event.clientX - imgRect.left;
    const y = event.clientY - imgRect.top;
    var separator = '';
    var jail = '';

    if (system.id == 'lobera'){ 
        sistema = 'lobero';
        if (template.role == 'separator'){ separator = document.getElementById("mamparos-dropdown").value.split(' - ') } 
        else { separator = 'None' };
    } else if (system.id == 'pecera') { 
        sistema = 'pecero' 
        jail = 'Pecera ' + document.getElementById("peceras-dropdown").value;
    } else { 
        sistema = 'tensores' 
    };

    x_json = weights[system.id][template.role]['x'][0] + x*weights[system.id][template.role]['x'][1]
    y_json = weights[system.id][template.role]['y'][0] + x*weights[system.id][template.role]['y'][1]


    return {
        'x': x,
        'y': y,
        'x_json': x_json,
        'y_json': y_json,
        'system': sistema,
        'template': template,
        'separator': separator,
        'jail': jail,
    };
};

function showMenu(event, menu){
    menu.style.left = `${event.pageX}px`;
    menu.style.top = `${event.pageY}px`;
    menu.style.display = 'block';
}

function hideMenu(){
    contextMenuLoberas.style.display = 'none'
    contextMenuPeceras.style.display = 'none'
    contextMenuTensores.style.display = 'none'
}

function saveImgMetadata(img_name, menuMetadata, type){
    imageMetaData[img_name]['json']['module'] = (document.getElementById("modules-dropdown").value - 1).toString();
    imageMetaData[img_name]['json']['system'] = menuMetadata.system;
    imageMetaData[img_name]['json']['type'] = type;
    imageMetaData[img_name]['json']['x'] = menuMetadata.x_json;
    imageMetaData[img_name]['json']['y'] = menuMetadata.y_json;
    if (menuMetadata.system == 'lobera'){ imageMetaData[img_name]['json']['separator'] = menuMetadata.separator}
    else if (menuMetadata.system == 'pecera') { imageMetaData[img_name]['json']['jail'] = menuMetadata.jail };
}

function saveIconMetadata(img_name, menuMetadata, icon){
    imageMetaData[img_name]['icon']['module'] = (document.getElementById("modules-dropdown").value - 1).toString();
    imageMetaData[img_name]['icon']['system'] = menuMetadata.system;
    imageMetaData[img_name]['icon']['template'] = menuMetadata.template;
    imageMetaData[img_name]['icon']['icon'] = icon;
    imageMetaData[img_name]['icon']['x'] = menuMetadata.x;
    imageMetaData[img_name]['icon']['y'] = menuMetadata.y;
    imageMetaData[img_name]['icon']['span'] = createIcon(img_name);
}

function refeshIcons(icon){
    refreshTemplates(icon);
    // refreshFrames()
};

function refreshTemplates(icon){
    document.querySelectorAll(".tabcontent").forEach((system) => {
        document.querySelectorAll("[id=image-container-" + system.id + "]").forEach((template) => {
            while (template.children.length > 1) {
                template.removeChild(template.lastChild)
            }
        });
    });

    for(i = 0; i < imgs_name.length; i++){
        if (imageMetaData[imgs_name[i]]['icon']['span'] != null){
            imageMetaData[imgs_name[i]]['icon']['template'].appendChild(imageMetaData[imgs_name[i]]['icon']['span'])
        }
    }
}

func

function refreshFrames(){

}

function createIcon(img_name) {
    const icon = document.createElement("span");
    icon.className = "icon-class";
    icon.textContent = imageMetaData[img_name]['icon']['icon'];
    icon.style.position = "absolute";

    const targetImageRect = imageMetaData[img_name]['icon']['template'].getBoundingClientRect();
    const iconWidth = 33;
    const iconHeight = 36;
    var centerX = 0
    var centerY = 0
    
    if (imageMetaData[img_name]['json']['type'] == 'correct'){
        centerX = targetImageRect.left + imageMetaData[img_name]['icon']['x'] - iconWidth * 4/ 11;
        centerY = targetImageRect.top + imageMetaData[img_name]['icon']['y'] - iconHeight * 2 / 3; 
    } else {
        centerX = targetImageRect.left + imageMetaData[img_name]['icon']['x'] - iconWidth / 2;
        centerY = targetImageRect.top + imageMetaData[img_name]['icon']['y'] - iconHeight / 2; 
    };

    icon.style.left = `${centerX}px`;
    icon.style.top = `${centerY}px`;
    icon.style.width = iconWidth;
    icon.style.height = iconHeight;

    return icon;
};
