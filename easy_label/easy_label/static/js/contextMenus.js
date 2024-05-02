// import "./addIcon.js";

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
            refeshIcons();
            refreshFrames(document.getElementById('selected-image').src.split('/').pop());
            hideMenu();
            });
            option.addEventListener('dblclick', function(event) {event.preventDefault()});
        });
    });
});

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

function getMenuMetadata(event, system, template) {
    const templateBox = template.getBoundingClientRect();
    const x_icon = event.clientX - templateBox.left;
    const y_icon = event.clientY - templateBox.top;
    const x_json = weights[system.id][template.role]['x'][0] + x_icon*weights[system.id][template.role]['x'][1]
    const y_json = weights[system.id][template.role]['y'][0] + y_icon*weights[system.id][template.role]['y'][1]

    if (system.id == 'lobera') {sistema = 'lobero'}
    else if (system.id == 'pecera') {sistema = 'pecero'}
    else {sistema = 'tensores'};

    return {
        'module': (document.getElementById("modules-dropdown").value - 1).toString(),
        'center': document.getElementById("centers-dropdown").value,
        'template': template,
        'json': {
            'system': sistema,
            'separator': (template.role == 'separator') ? document.getElementById("mamparos-dropdown").value.split(' - ') : 'None',
            'jail': 'Pecera ' + document.getElementById("peceras-dropdown").value,
            'x': x_json,
            'y': y_json
        },
        'icon': {
            'system': system.id,
            'separator': (template.role == 'separator') ? document.getElementById("mamparos-dropdown").value : 'None',
            'jail': document.getElementById("peceras-dropdown").value,
            'x': x_icon,
            'y': y_icon,
        }
    };
};


function saveImgMetadata(img_name, menuMetadata, type){
    imageMetaData['json'][img_name]['module'] = menuMetadata.module;
    imageMetaData['json'][img_name]['system'] = menuMetadata.json.system;
    imageMetaData['json'][img_name]['type'] = type;
    imageMetaData['json'][img_name]['x'] = menuMetadata.json.x;
    imageMetaData['json'][img_name]['y'] = menuMetadata.json.y;
    if (menuMetadata.system == 'lobera'){ imageMetaData['json'][img_name]['separator'] = menuMetadata.json.separator}
    else if (menuMetadata.system == 'pecera') { imageMetaData['json'][img_name]['jail'] = menuMetadata.json.jail };
}

function saveIconMetadata(img_name, menuMetadata, icon){
    imageMetaData['icon'][img_name]['module'] = menuMetadata.module;
    imageMetaData['icon'][img_name]['center'] = menuMetadata.center;
    imageMetaData['icon'][img_name]['system'] = menuMetadata.icon.system;
    imageMetaData['icon'][img_name]['template'] = menuMetadata.template;
    imageMetaData['icon'][img_name]['separator'] = menuMetadata.icon.separator;
    imageMetaData['icon'][img_name]['jail'] = menuMetadata.icon.jail;
    imageMetaData['icon'][img_name]['icon'] = icon;
    imageMetaData['icon'][img_name]['x'] = menuMetadata.icon.x;
    imageMetaData['icon'][img_name]['y'] = menuMetadata.icon.y;
    imageMetaData['icon'][img_name]['span'] = createIcon(img_name);
    imageMetaData['icon'][img_name]['thumbnail'] = createThumbnail(img_name);
};    

function createIcon(img_name) {
    const icon = document.createElement("span");
    icon.className = "icon-class";
    icon.textContent = imageMetaData['icon'][img_name]['icon'];
    icon.style.position = "absolute";

    const targetImageRect = imageMetaData['icon'][img_name]['template'].getBoundingClientRect();
    const iconWidth = 33;
    const iconHeight = 36;
    var centerX = 0
    var centerY = 0
    
    if (imageMetaData['json'][img_name]['type'] == 'correct'){
        centerX = targetImageRect.left + imageMetaData['icon'][img_name]['x'] - iconWidth * 4/ 11;
        centerY = targetImageRect.top + imageMetaData['icon'][img_name]['y'] - iconHeight * 2 / 3; 
    } else {
        centerX = targetImageRect.left + imageMetaData['icon'][img_name]['x'] - iconWidth / 2;
        centerY = targetImageRect.top + imageMetaData['icon'][img_name]['y'] - iconHeight / 2; 
    };

    icon.style.left = `${centerX}px`;
    icon.style.top = `${centerY}px`;
    icon.style.width = iconWidth;
    icon.style.height = iconHeight;

    return icon;
};



function createThumbnail(img_name) {
    const icon = document.createElement("span");
    icon.className = "thumbnail-icon no-select";
    icon.textContent = imageMetaData['icon'][img_name]['icon'];
    icon.style.position = "absolute";
    // icon.style.fontSize = "20px";
    icon.style.left = "50%";
    icon.style.top = "50%";
    icon.style.transform = "translate(-50%, -45%)"
    return icon
}

