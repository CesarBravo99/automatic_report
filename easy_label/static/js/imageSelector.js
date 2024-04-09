document.addEventListener("DOMContentLoaded", function () {
  const images = document.querySelectorAll(".image-item");

  images.forEach((image) => {
    image.addEventListener("click", function () {
      images.forEach((img) => img.classList.remove("selected")); // Remove selected class from all images
      this.classList.add("selected"); // Add selected class to clicked image
    });
  });
});