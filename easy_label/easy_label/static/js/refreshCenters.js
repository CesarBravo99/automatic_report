function refreshCenters(event) {
    /* 
    Refresh the center image tempaltes when the center is changed
    */

    var center = document.getElementById("centers-dropdown").value;
    var module = 0;
    var x_flip = + centers[center]['x_flip'][module];
    var y_flip = + centers[center]['y_flip'][module];
    var double = + centers[center]['double'][module];
    var center_modules = centers[center]['modules'];
    var jails = centers[center]['jails'][module];
    var scope = centers[center]['scopes'][module].toString()[0];


    document.getElementById("img-loberas-fondo").src = staticBaseUrl + "imgs/assets/background/" + center.replace(/ /g, "") + `_${module}.png`;
    document.getElementById("img-loberas-lateral").src = staticBaseUrl + "imgs/assets/lateral/" + center.replace(/ /g, "") + `_${module}.png`;
    document.getElementById("img-loberas-cabeceras").src = staticBaseUrl + "imgs/assets/fixed/seawolf_head_" + x_flip + y_flip + double + ".png";
    document.getElementById("img-tensores").src = staticBaseUrl + "imgs/assets/tensor/" + center.replace(/ /g, "") + `_${module}.png`;

    var dropdownModule = document.getElementById("modules-dropdown");
    for (i = dropdownModule.length - 1; i >= 0; i--) {
        dropdownModule.remove(i);
    }
    for (i = 1; i <= center_modules; i++) {
        dropdownModule.appendChild(new Option('Módulo ' + i, i));
    }

    refreshMamparos(x_flip, y_flip, jails);
    refreshPeceras(jails, scope);
    // refreshSystem();
}

function refreshModule(event) {
    /* 
    Refresh the center image templates when the module is changed
    */

    var center = document.getElementById("centers-dropdown").value;
    var module = document.getElementById("modules-dropdown").value - 1;
    var x_flip = + centers[center]['x_flip'][module];
    var y_flip = + centers[center]['y_flip'][module];
    var double = + centers[center]['double'][module];
    var jails = centers[center]['jails'][module];
    var scope = centers[center]['scopes'][module].toString()[0];
    
    document.getElementById("img-loberas-fondo").src = staticBaseUrl + "imgs/assets/background/" + center.replace(/ /g, "") + `_${module}.png`;
    document.getElementById("img-loberas-lateral").src = staticBaseUrl + "imgs/assets/lateral/" + center.replace(/ /g, "") + `_${module}.png`;
    document.getElementById("img-loberas-cabeceras").src = staticBaseUrl + "imgs/assets/fixed/seawolf_head_" + x_flip + y_flip + double + ".png";
    document.getElementById("img-tensores").src = staticBaseUrl + "imgs/assets/tensor/" + center.replace(/ /g, "") + `_${module}.png`;

    refreshMamparos(x_flip, y_flip, jails);
    refreshPeceras(jails, scope);
    // refreshSystem();

}

function refreshMamparos(x_flip, y_flip, jails){
    /* 
    Refresh the mamparos dropdown when the module or the center is changed
    */

    var dropdownModule = document.getElementById("mamparos-dropdown"); 
    for (i = dropdownModule.length - 1; i >= 0; i--) {
        dropdownModule.remove(i);
    }

    if (y_flip) {
        for (i = jails-3; i >= 0; i-=2) {
            var j = i+1
            if (x_flip) {
                var value = "L" + i + " - " + "L" + j ;
                dropdownModule.appendChild(new Option(value, value));
            } else {
                var value = "L" + j + " - " + "L" + i ;
                dropdownModule.appendChild(new Option(value, value));
            }
        }
    } else {
        for (i = 1; i <= jails-2; i+=2) {
            var j = i+1
            if (x_flip) {
                var value = "L" + i + " - " + "L" + j ;
                dropdownModule.appendChild(new Option(value, value));
            } else {
                var value = "L" + j + " - " + "L" + i ;
                dropdownModule.appendChild(new Option(value, value));
            }
        }
    };
    refeshIcons();
}

function refreshPeceras(jails, scope){
    /* 
    Refresh the peceras dropdown when the module or the center is changed
    */
    var dropdownModule = document.getElementById("peceras-dropdown"); 
    for (i = dropdownModule.length - 1; i >= 0; i--) {
        dropdownModule.remove(i);
    };
    for (i=1; i <= jails; i++) {
        if (i <= 9) {
            var value = scope + "0" + i
            dropdownModule.appendChild(new Option(value, value));
        } else {
            var value = scope + i
            dropdownModule.appendChild(new Option(value, value));
        }
    };
    refeshIcons();
}