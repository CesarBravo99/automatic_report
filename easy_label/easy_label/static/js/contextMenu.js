

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
                coords = getCoords(event, system, template);
                contextMenu[system.id].style.left = `${event.pageX}px`;
                contextMenu[system.id].style.top = `${event.pageY}px`;
                contextMenu[system.id].style.display = 'block';
            });
            template.addEventListener("click", function (event) {
                contextMenuLoberas.style.display = 'none'
                contextMenuPeceras.style.display = 'none'
                contextMenuTensores.style.display = 'none'
            });
        });
        document.querySelectorAll("[id=context-link-" + system.id + ']').forEach((option) => {
            option.addEventListener('click', function(event) {
            const annText = this.innerText.slice(3);
            const annIcon = this.querySelector("span[role='icon']").textContent;
            var img_name = document.getElementById('selected-image').src.split('/').pop()
            saveAnnotation(img_name, coords, annText)
            addIcon(annIcon)
            contextMenu[system.id].style.display = 'none';
            });
        });
    });

    function getCoords(event, system, template) {
        const imgRect = template.getBoundingClientRect();
        var x = event.clientX - imgRect.left;
        var y = event.clientY - imgRect.top;
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

        x = weights[system.id][template.role]['x'][0] + x*weights[system.id][template.role]['x'][1]
        y = weights[system.id][template.role]['y'][0] + x*weights[system.id][template.role]['y'][1]


        return {
            "x": x,
            "y": y,
            "system": sistema,
            "separator": separator,
            "jail": jail,
        };
    };

    function saveAnnotation(img_name, coords, ann){
        imageMetaData[img_name]['module'] = (document.getElementById("modules-dropdown").value - 1).toString();
        imageMetaData[img_name]['system'] = coords.system
        imageMetaData[img_name]['type'] = getType(ann)
        imageMetaData[img_name]['x'] = coords.x
        imageMetaData[img_name]['y'] = coords.y
        if (coords.system == 'lobera'){ imageMetaData[img_name]['separator'] = coords.separator } 
        else if (coords.system == 'pecera') { imageMetaData[img_name]['jail'] = coords.jail }
    };

    function getType(ann){
        if (ann == 'Correcto'){ return 'correct'}
        else if (ann == 'Rotura/Falla'){ return 'tear'}
        else if (ann == 'Anomalía'){ return 'anomaly'}
        else if (ann == 'Adherencia'){ return 'adherence'}
        else if (ann == 'Mortalidad'){ return 'mortality'}
        else if (ann == 'Falta tensión'){ return 'lack_tension'}
        else if (ann == 'Sin tensión'){ return 'no_tension'}
    };
})