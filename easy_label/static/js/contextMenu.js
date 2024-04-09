// Add event listener for right-click to show context menu
document.addEventListener(
  "contextmenu",
  function (event) {
    event.preventDefault();

    var contextMenu = document.getElementById("context-menu");
    var clickedElement = event.target;

    // Check if the clicked element is an image inside the specific containers
    if (
      clickedElement.tagName === "IMG" &&
      (clickedElement.closest(".grid-container-loberas") ||
        clickedElement.closest(".grid-container-peceras") ||
        clickedElement.closest(".img-tensores"))
    ) {
      updateContextMenuItems(clickedElement);
      contextMenu.style.display = "block";
      contextMenu.style.left = `${event.pageX}px`;
      contextMenu.style.top = `${event.pageY}px`;
    } else {
      contextMenu.style.display = "none";
    }
  },
  false
);

// Function to update context menu items based on clicked element
function updateContextMenuItems(clickedElement) {
  var contextMenuList = document.querySelector("#context-menu .context-menu-items");
  contextMenuList.innerHTML = ''; // Clear existing menu items

  // Define different sets of options
  var loberasOptions = [
    "✅ Correcto", "❌ Rotura/Falla", "⚠️ Anomalía", "➕ Adherencia"
  ];
  var tensoresOptions = [
    "✅ Correcto", "⚠️ Falta Tensión", "❌ Sin Tensión"
  ]
  var pecerasOptions = [
    "✅ Correcto", "❌ Rotura/Falla", "⚠️ Anomalía", "➕ Adherencia", "☠️ Mortalidad"
  ];

  // Determine the currently active tab
  var activeTab = document.querySelector(".tablinks.active").textContent;

  // Determine which options to show based on the active tab
  var optionsToShow;
  if (activeTab === "Peceras") {
    optionsToShow = pecerasOptions;
  } else if (activeTab === "Tensores") {
    optionsToShow = tensoresOptions;
  } else {
    optionsToShow = loberasOptions; // Default to loberasOptions if neither Peceras nor Tensores
  }
  console.log('options START')
  // Populate the context menu with the appropriate options
  optionsToShow.forEach(optionText => {
    var li = document.createElement("li");
    var span = document.createElement("span");
    span.setAttribute("role", "img");
    span.textContent = optionText.split(" ")[0]; // Emoji
    li.appendChild(span);
    li.appendChild(document.createTextNode(" " + optionText.split(" ").slice(1).join(" ")));
    contextMenuList.appendChild(li);
  });
  window.setupContextMenuClickEvents();
  console.log('options END')
}

// Add event listener for regular click to hide context menu
document.addEventListener(
  "click",
  function (event) {
    var contextMenu = document.getElementById("context-menu");
    if (contextMenu.style.display === "block") {
      contextMenu.style.display = "none";
    }
  },
  false
);