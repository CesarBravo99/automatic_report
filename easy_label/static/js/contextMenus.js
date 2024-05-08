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
            option.addEventListener('click', function() {
            const type = this.querySelector("span[role='icon']").ariaLabel;
            const icon = this.querySelector("span[role='icon']").textContent;
            const img_name = document.getElementById('selected-image').src.split('/').pop();
            saveImgMetadata(img_name, menuMetadata, type);
            saveIconMetadata(img_name, menuMetadata, type, icon);
            refreshIcons();
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
    const templateBBox = template.children[0].getBoundingClientRect();
    const templateWidth = templateBBox.width;
    const templateHeight = templateBBox.height;
    const imgWidth = template.children[0].naturalWidth
    const imgHeight = template.children[0].naturalHeight

    const px = (event.clientX - templateBBox.left) / templateWidth
    const py = (event.clientY - templateBBox.top) / templateHeight
    const x = weights[system.id][template.role]['x'][0] + px*imgWidth*weights[system.id][template.role]['x'][1]
    const y = weights[system.id][template.role]['y'][0] + py*imgHeight*weights[system.id][template.role]['y'][1]

    // alert(imgWidth)
    // alert(x)
    if (system.id == 'lobera') {sistema = 'lobero'}
    else if (system.id == 'pecera') {sistema = 'pecero'}
    else {sistema = 'tensor'};
    return {
        'module': (document.getElementById("modules-dropdown").value - 1).toString(),
        'center': document.getElementById("centers-dropdown").value,
        'template': template,
        'json': {
            'system': sistema,
            'separator': (template.role == 'separator') ? document.getElementById("mamparos-dropdown").value.split(' - ') : 'None',
            'jail': 'Pecera ' + document.getElementById("peceras-dropdown").value,
            'x': x,
            'y': y
        },
        'icon': {
            'system': system.id,
            'separator': (template.role == 'separator') ? document.getElementById("mamparos-dropdown").value : 'None',
            'jail': document.getElementById("peceras-dropdown").value,
            'x': event.clientX - templateBBox.left,
            'y': event.clientY - templateBBox.top,
        }
    };
};


function saveImgMetadata(img_name, menuMetadata, type){
    imageMetaData['json'][img_name]['module'] = menuMetadata.module;
    imageMetaData['json'][img_name]['system'] = menuMetadata.json.system;
    imageMetaData['json'][img_name]['type'] = type;
    imageMetaData['json'][img_name]['x'] = menuMetadata.json.x;
    imageMetaData['json'][img_name]['y'] = menuMetadata.json.y;
    if (menuMetadata.json.system == 'lobero'){ imageMetaData['json'][img_name]['separator'] = menuMetadata.json.separator}
    else if (menuMetadata.json.system == 'pecero') { imageMetaData['json'][img_name]['jail'] = menuMetadata.json.jail };
}

function saveIconMetadata(img_name, menuMetadata, type, icon){
    imageMetaData['icon'][img_name]['module'] = menuMetadata.module;
    imageMetaData['icon'][img_name]['center'] = menuMetadata.center;
    imageMetaData['icon'][img_name]['system'] = menuMetadata.icon.system;
    imageMetaData['icon'][img_name]['type'] = type;
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

    // const templateBBox = imageMetaData['icon'][img_name]['template'].children[0].getBoundingClientRect();
    // const iconWidth = window.screen.width / 50;
    // const iconHeight = window.screen.height / 50;
    // var centerX = 0
    // var centerY = 0
    
    // if (imageMetaData['json'][img_name]['type'] == 'correct'){
    //     centerX = templateBBox.left + window.scrollX + imageMetaData['icon'][img_name]['x']//*templateWidth //+ iconWidth * 3/2
    //     centerY = templateBBox.top + window.scrollY + imageMetaData['icon'][img_name]['y']//*templateHeight //- iconHeight * 2 / 3; 
    // } else {
    //     centerX = templateBBox.left + window.scrollX + imageMetaData['icon'][img_name]['x']//*templateWidth //+ iconWidth ;
    //     centerY = templateBBox.top + window.scrollY + imageMetaData['icon'][img_name]['y']//*templateHeight //- iconHeight / 2; 
    // };

    // icon.style.left = `${centerX}px`;
    // icon.style.top = `${centerY}px`;
    // icon.style.width = iconWidth;
    // icon.style.height = iconHeight;

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

