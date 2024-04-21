
document.addEventListener("DOMContentLoaded", function () {
    const images = document.querySelectorAll(".img-thumbnail");
    images.forEach((image) => {
        image.addEventListener("click", function () {
            images.forEach((img) => img.classList.remove("selected"));
            this.classList.add("selected"); 
            document.getElementById('selected-image').src = this.getAttribute("src");
            // selectedImgSrc = this.getAttribute("src")
            // alert(selectedImgSrc);
            // displayImageComment(selectedImgSrc);
        });
    });

    // function displayImageComment(selectedImgSrc) {
    //     const commentBox = document.getElementById("comment-box");
    //     commentBox.value = imageData[selectedImgSrc] && imageData[selectedImgSrc].comment ? imageData[selectedImgSrc].comment : '';
    //     commentBox.addEventListener("input", function () {
    //         if (!imageData[selectedImgSrc]) {
    //             imageData[selectedImgSrc] = {};
    //         }
    //         imageData[selectedImgSrc].comment = commentBox.value;
    //     });
    // };
});