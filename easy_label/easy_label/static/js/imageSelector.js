document.addEventListener("DOMContentLoaded", function () {

    const images = document.querySelectorAll(".img-thumbnail");

    images.forEach((image) => {
        image.addEventListener("click", function () {
            images.forEach((img) => img.classList.remove("selected"));
            this.classList.add("selected"); 
            document.getElementById('selected-image').src = this.getAttribute("src")
        });
    });
});