var iconData = {};
var imageData = {}; // Store icon and comment data for each left sidebar image

document.addEventListener("DOMContentLoaded", function () {
    var selectedLeftImage = null;
    var selectedEmoji = "";
    var contextMenu = document.getElementById("context-menu");
    var lastRightClickPosition = null; // Store the last right-click position

    // Handle left sidebar image selection (including clicking on icons)
    document.querySelectorAll(".image-item").forEach((item) => {
        item.addEventListener("click", function () {
            const img = item.querySelector("img");
            selectedLeftImage = img.getAttribute("src").split("/").pop(); // Use only the filename
            displayCommentForImage(selectedLeftImage);
            redrawIconForSelectedImage();
        });
    });

    // Handle clicking on icons
    document.querySelectorAll(".thumbnail-icon").forEach((icon) => {
        icon.addEventListener("click", function (event) {
            event.stopPropagation(); // Prevent click event from propagating to the thumbnail
            // Find the associated image filename
            const imageFilename = this.parentElement.querySelector("img").getAttribute("src").split("/").pop();
            selectedLeftImage = imageFilename;
            displayCommentForImage(selectedLeftImage);
            redrawIconForSelectedImage();
        });
    });

    // Prevent the default behavior when double-clicking on thumbnails
    document.querySelectorAll(".image-item img").forEach((img) => {
        img.addEventListener("dblclick", function (event) {
            event.preventDefault();
        });
    });

    // Function to display and automatically save the comment for a selected image
    function displayCommentForImage(imageSrc) {
        const commentBox = document.getElementById("comment-box");
        commentBox.value = imageData[imageSrc] && imageData[imageSrc].comment ? imageData[imageSrc].comment : '';
        commentBox.addEventListener("input", function () {
            if (!imageData[imageSrc]) {
                imageData[imageSrc] = {};
            }
            imageData[imageSrc].comment = commentBox.value;
        });
    }

    // Function to set up context menu item click event listeners
    window.setupContextMenuClickEvents = function () {
        document.querySelectorAll(".context-menu-items li").forEach((item) => {
            item.addEventListener("click", function () {
                selectedEmoji = this.querySelector("span[role='img']").textContent.trim();
                const emojiDescription = this.innerText;
                console.log("Selected emoji:", selectedEmoji);
                if (lastRightClickPosition && selectedLeftImage) {
                    addIconToPosition(lastRightClickPosition, selectedEmoji, emojiDescription);
                    lastRightClickPosition = null; // Reset the stored position
                }
                contextMenu.style.display = "none";
            });
        });
    }

    // Handle right-click on tab content images
    document.querySelectorAll(".tabcontent img").forEach((img) => {
        img.addEventListener("contextmenu", function (event) {
            event.preventDefault();
            if (!selectedLeftImage) return;
            // Set up context menu item click event listeners
            // console.log('START')
            lastRightClickPosition = getIconPlacementData(event, img);
            console.log("Right-click position:", lastRightClickPosition);
            contextMenu.style.left = `${event.pageX}px`;
            contextMenu.style.top = `${event.pageY}px`;
            contextMenu.style.display = "block";
            // console.log('END')
        });
    });

    function getIconPlacementData(event, img) {
        const imgRect = img.getBoundingClientRect();
        const imgClass = img.classList[0]; // Use the first class as the unique identifier
        return {
            x: event.clientX - imgRect.left,
            y: event.clientY - imgRect.top,
            tabContent: img.closest(".tabcontent"),
            associatedImage: selectedLeftImage,
            imageClass: imgClass, // Store the class name
            imageName: img.src.split("/").pop(),
        };
    }

    function addIconToPosition(placementData, emoji, emojiDescription) {
        removeCurrentIcon();
        const icon = createIcon(emoji, placementData);
        const activeTab = document.querySelector(".tablinks.active");
        const activeTabName = activeTab ? activeTab.innerText : 'unknown';
        const activeModule = document.getElementById("modules-dropdown").value;
        const comment = document.getElementById("comment-box").value;
        const pecerasValue = document.getElementById("peceras-dropdown").value;
        const mamparosValue = document.getElementById("mamparos-dropdown").value;
        const targetImage = document.querySelector(`.${placementData.imageClass}`);
        const targetImageRect = targetImage.getBoundingClientRect();
        const px = (placementData.x/targetImageRect.width);
        const py = (placementData.y/targetImageRect.height);
        // Update icon data with active tab information
        iconData[selectedLeftImage] = {
            ...placementData,
            emoji: emoji,
            activeTab: activeTabName,
            module: activeModule ? activeModule : '0',
            comment: comment,
            type: emojiDescription,
            peceras: pecerasValue,
            mamparos: mamparosValue,
            px: px,
            py: py,
        };

        positionIcon(icon, placementData.tabContent, placementData);
        console.log("Icon data:", iconData); // Log icon data
        if (!imageData[selectedLeftImage]) {
            imageData[selectedLeftImage] = {};
        }
        imageData[selectedLeftImage].icon = iconData[selectedLeftImage];
        addIconToThumbnail(selectedLeftImage, emoji);
        // Log combined icon and comment data
        console.log("Image data:", imageData);
    }

    function positionIcon(icon, tabContent, placementData) {
        const targetImage = tabContent.querySelector(`.${placementData.imageClass}`);
        if (targetImage) {
            const targetImageRect = targetImage.getBoundingClientRect();
            const iconWidth = 32.96; // Fixed icon width
            const iconHeight = 36;   // Fixed icon height

            // Calculate the centered position with respect to the icon's size
            const centerX = targetImageRect.left + window.scrollX + placementData.x - iconWidth / 2;
            const centerY = targetImageRect.top + window.scrollY + placementData.y - iconHeight / 2;

            icon.style.left = `${centerX}px`;
            icon.style.top = `${centerY}px`;
            tabContent.appendChild(icon);
        }
    }


    function createIcon(emoji, placementData) {
        const icon = document.createElement("span");
        icon.className = "icon-class";
        icon.textContent = emoji;
        icon.style.position = "absolute";
        return icon;
    }

    // Add event listener for tab changes
    document.querySelectorAll(".tablinks").forEach((tab) => {
        tab.addEventListener("click", function () {
            redrawIconForSelectedImage();
        });
    });

    function redrawIconForSelectedImage() {
        removeCurrentIcon();

        // Clear all existing icons in the current tab
        const existingIcons = document.querySelectorAll(".icon-class");
        existingIcons.forEach((icon) => {
            icon.remove();
        });

        const placementData = iconData[selectedLeftImage];
        if (placementData) {
            const targetTab = placementData.tabContent;
            if (targetTab && targetTab.style.display !== "none") {
                const targetImage = targetTab.querySelector(`img[src*='${placementData.imageName}']`);
                if (targetImage) {
                    // Calculate the icon's position based on the current image's position
                    const targetImageRect = targetImage.getBoundingClientRect();
                    const iconWidth = 32.96; // Fixed icon width
                    const iconHeight = 36;   // Fixed icon height

                    // Calculate the centered position with respect to the icon's size
                    const centerX = targetImageRect.left + window.scrollX + placementData.x - iconWidth / 2;
                    const centerY = targetImageRect.top + window.scrollY + placementData.y - iconHeight / 2;

                    const icon = createIcon(placementData.emoji, placementData);
                    icon.style.left = `${centerX}px`;
                    icon.style.top = `${centerY}px`;
                    targetTab.appendChild(icon);
                }
            }
        }
    }

    function redrawIconAtTargetImage(targetImage, placementData, targetTab) {
        const targetImageRect = targetImage.getBoundingClientRect();

        // Calculate icon size based on the target container size
        const iconWidth = targetImageRect.width * 0.1; // Adjust the factor as needed
        const iconHeight = targetImageRect.height * 0.1; // Adjust the factor as needed

        // Calculate the centered position with respect to the icon's size
        const centerX = targetImageRect.left + window.scrollX + placementData.x - iconWidth / 2;
        const centerY = targetImageRect.top + window.scrollY + placementData.y - iconHeight / 2;

        const icon = createIcon(placementData.emoji, placementData);
        icon.style.width = `${iconWidth}px`; // Set icon width
        icon.style.height = `${iconHeight}px`; // Set icon height
        icon.style.left = `${centerX}px`;
        icon.style.top = `${centerY}px`;
        targetTab.appendChild(icon);
    }

    function removeCurrentIcon() {
        const existingIcon = document.querySelector(".icon-class");
        if (existingIcon) {
            existingIcon.remove();
        }
    }

    // Automatically select the first image if it exists
    const firstImage = document.querySelector(".image-item img");
    if (firstImage) {
        firstImage.click();
    }

    function addIconToThumbnail(imageFilename, emoji) {
        // Find the corresponding thumbnail image in the left sidebar
        var thumbnail = document.querySelector(`.image-item img[src$='${imageFilename}']`);
        if (thumbnail) {
            // Check if an icon already exists for this thumbnail
            var existingIcon = thumbnail.parentElement.querySelector(".thumbnail-icon");
            if (existingIcon) {
                // Update the existing icon
                existingIcon.textContent = emoji;
            } else {
                // Create a new icon
                var icon = document.createElement("span");
                icon.className = "thumbnail-icon";
                icon.textContent = emoji;

                // Style the icon (you can adjust these styles)
                icon.style.position = "absolute";
                icon.style.fontSize = "20px"; // Smaller size for thumbnail
                icon.style.left = "50%";
                icon.style.top = "50%";
                icon.style.transform = "translate(-50%, -50%)";

                // Append the icon to the thumbnail's parent element
                thumbnail.parentElement.style.position = "relative";
                thumbnail.parentElement.appendChild(icon);
            }
        }
    }
});