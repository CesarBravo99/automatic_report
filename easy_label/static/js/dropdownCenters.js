document.addEventListener("DOMContentLoaded", () => {
  const centersDropdown = document.getElementById("centers-dropdown");
  const mamparosDropdown = document.getElementById("mamparos-dropdown");
  const modulesDropdown = document.getElementById("modules-dropdown");
  let currentModule = "0";

  if (centersDropdown) {
    centersDropdown.addEventListener("change", function () {
      const selectedCenter = this.value;
      console.log("Selected center:", selectedCenter);
      const centerImages = centersData[selectedCenter];
      console.log("Center images:", centerImages);
      if (centerImages) {
        if (centerImages.modules > 1) {
          console.log('Found modules for selected center:', centerImages.modules);
          populateModulesDropdown(centerImages.modules);
          modulesDropdown.style.display = "block";
        } else {
          console.log('No modules found for selected center.');
          modulesDropdown.style.display = "none";
          currentModule = "0";
        }
        updateImages(centerImages, currentModule);
        updateMamparosDropdown(centerImages, currentModule);
      } else {
        console.error("No data found for selected center:", selectedCenter);
      }

      if (typeof iconData !== "undefined") {
        iconData = {};
      }
      if (typeof imageData !== "undefined") {
        imageData = {};
      }
      clearThumbnailIcons()
      const firstImage = document.querySelector(".image-item:first-child img");
      if (firstImage) {
        firstImage.click();
      }
      const firstButton = document.querySelector(".tablinks:first-child");
      if (firstButton) {
        firstButton.click();
      }
    });

    modulesDropdown.addEventListener("change", function () {
      currentModule = this.value;
      const selectedCenter = centersDropdown.value;
      const centerImages = centersData[selectedCenter];
      updateImages(centerImages, currentModule);
      updateMamparosDropdown(centerImages, currentModule);
    });

    centersDropdown.dispatchEvent(new Event("change"));
  }

  function clearThumbnailIcons() {
    const thumbnailIcons = document.querySelectorAll(".image-item .thumbnail-icon");
    thumbnailIcons.forEach(icon => {
      icon.remove();
    });
  }

  function updateImages(centerImages, module) {
    document.querySelector(".img-loberas-fondo").src = staticBaseUrl + "easy-label/centers/background/" + centerImages.filename + `_${module}.png`;
    document.querySelector(".img-loberas-lateral").src = staticBaseUrl + "easy-label/centers/lateral/" + centerImages.filename + `_${module}.png`;
    document.querySelector(".img-tensores").src = staticBaseUrl + "easy-label/centers/tensor/" + centerImages.filename + `_${module}.png`;

    const xFlip = centerImages.x_flip[module] ? "1" : "0";
    const yFlip = centerImages.y_flip[module] ? "1" : "0";
    // const doubled = centerImages.double[module] ? "1" : "0";
    const doubled = "1"
    const cabecerasSuffix = xFlip + yFlip + doubled;
    // console.log("Cabeceras suffix:", cabecerasSuffix);
    document.querySelector(".img-loberas-cabeceras").src = staticBaseUrl + "easy-label/centers/fixed/seawolf_head_" + cabecerasSuffix + ".png";
  }

  function updateMamparosDropdown(centerImages, module) {
    const xFlip = centerImages.x_flip[module];
    const jailCount = centerImages.jails[module];
    const sep = [];
    for (let jail = 1; jail <= jailCount - 1; jail += 2) {
      if (xFlip) {
        sep.push(`L${jail} - L${jail + 1}`);
      } else {
        sep.push(`L${jail + 1} - L${jail}`);
      }
    }
    mamparosDropdown.innerHTML = '';
    sep.forEach(optionText => {
      const option = document.createElement("option");
      option.value = optionText;
      option.textContent = optionText;
      mamparosDropdown.appendChild(option);
    });
  }

  function populateModulesDropdown(numModules) {
    modulesDropdown.innerHTML = '';
    for (let i = 0; i < numModules; i++) {
      const option = document.createElement("option");
      option.value = i.toString();
      option.textContent = `Módulo ${i + 1}`;
      modulesDropdown.appendChild(option);
    }
  }
});