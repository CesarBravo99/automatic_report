var imageComments = {}; // Object to store comments for each image

document.addEventListener("DOMContentLoaded", function () {
    var selectedImageSrc = null; // Currently selected image source

    const imageItems = document.querySelectorAll(".image-item");
    const commentBox = document.getElementById("comment-box");

    // Function to display the selected image in the right sidebar
    function displaySelectedImage(imageSrc) {
        const selectedImageElement = document.getElementById("selected-image");
        selectedImageElement.src = imageSrc;
    }

    // Function to display and automatically save the comment for a selected image
    function displayCommentForImage(imageSrc) {
        // Update the value of the comment box
        commentBox.value = imageComments[imageSrc] ? imageComments[imageSrc].comment : '';

        // Update the global variable to reflect the currently selected image source
        selectedImageSrc = imageSrc;
    }

    // Add an input event listener to save comments for the current image
    if (commentBox) {
        commentBox.addEventListener("input", function () {
            if (selectedImageSrc) {
                if (!imageComments[selectedImageSrc]) {
                    imageComments[selectedImageSrc] = {};
                }
                imageComments[selectedImageSrc].comment = commentBox.value;
            }
        });
    }

    // Add click event listeners to left sidebar image items (including images and icons)
    imageItems.forEach(item => {
        item.addEventListener("click", function (event) {
            let imageSrc;
            if (event.target.tagName === 'IMG') {
                // If the clicked target is an image
                imageSrc = event.target.getAttribute("src");
            } else if (event.target.classList.contains("thumbnail-icon")) {
                // If the clicked target is a thumbnail icon
                const img = item.querySelector("img");
                imageSrc = img ? img.getAttribute("src") : '';
            }

            if (imageSrc) {
                displaySelectedImage(imageSrc);
                displayCommentForImage(imageSrc);
            }
        });
    });

    // Automatically select the first image if it exists
    if (imageItems.length > 0) {
        const firstImage = imageItems[0].querySelector("img");
        if (firstImage) {
            firstImage.click();
        }
    }
});
