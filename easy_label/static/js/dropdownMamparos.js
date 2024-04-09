document.addEventListener("DOMContentLoaded", () => {
  const mamparosDropdown = document.getElementById("mamparos-dropdown");
  if (mamparosDropdown) {
    mamparosDropdown.addEventListener("change", function () {
      // Handle the dropdown change event
      // Example: Log the selected value or update another element
      console.log("Selected option:", this.value);
    });
  }
});

// function hoverOpenDropdown() {
//   const mamparosDropdown = document.getElementById("mamparos-dropdown");
//   if (mamparosDropdown) {
//     mamparosDropdown.addEventListener("mouseenter", function () {
//       this.size = this.options.length; // Set size to number of options
//     });
//     mamparosDropdown.addEventListener("mouseleave", function () {
//       this.size = 1; // Reset size when not hovering
//     });
//   }
// }

// // Call the function when the document is loaded
// document.addEventListener("DOMContentLoaded", hoverOpenDropdown);
