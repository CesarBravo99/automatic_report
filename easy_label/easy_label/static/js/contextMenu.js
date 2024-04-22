

document.addEventListener('DOMContentLoaded', function () {

    const contextMenu = document.getElementById('context-menu');

    // Defines a custom context menu
    document.querySelectorAll('.tabcontent').forEach((template) => {
        template.addEventListener('contextmenu', function (event) {
            event.preventDefault();
            selectedImg = document.getElementById('selected-image').src.split('/').pop()
            if (selectedImg == 'favicon_cover.png') return;
            contextMenu.style.left = `${event.pageX}px`;
            contextMenu.style.top = `${event.pageY}px`;
            coords = getCoords(event, template);
            contextMenu.style.display = 'block';
        });
    });


    function getCoords(event, tempalte) {
        const imgRect = tempalte.getBoundingClientRect();

        if (tempalte.id == 'lobera'){
            system = 'lobero'
        } else if (tempalte.id == 'pecera') {
            system = 'lobero'
        } else {
            system = 'tensores'
        }
        return {
            x: event.clientX - imgRect.left,
            y: event.clientY - imgRect.top,
        };
    }

    // Handles a click on the context menu options
    document.querySelectorAll(".context-menu-items li").forEach((option) => {
        option.addEventListener('click', function(event) {
            const annText = this.innerText;
            const annIcon = this.querySelector("span[role='icon']").textContent;
            // alert(system)

            imageMetaData[selectedImg]['module'] = document.getElementById("modules-dropdown").value - 1;
            imageMetaData[selectedImg]['system'] = system;
            imageMetaData[selectedImg]['x'] = coords.x;
            imageMetaData[selectedImg]['y'] = coords.y;

            if (system == 'tensores'){

            } else {
                if (this.innerText == 'Correcto'){
                    imageMetaData[selectedImg]['type'] = system;
                } else if (this.innerText == 'Rotura/Falla') {
                    imageMetaData[selectedImg]['type'] = system;
                } else if (this.innerText == 'Anomalía') {
                    imageMetaData[selectedImg]['type'] = system;
                }  else if (this.innerText == 'Adherencia') {
                    imageMetaData[selectedImg]['type'] = system;
                }
            }
            



            // alert(selectedImg)
            // alert(coords.x);
            // alert(coords.y);

            contextMenu.style.display = 'none';
        });
    });
});