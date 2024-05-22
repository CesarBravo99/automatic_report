
document.addEventListener('DOMContentLoaded', function () {
    const images = document.querySelectorAll('.img-thumbnail');
    images.forEach((image) => {
        image.addEventListener('click', function () {
            images.forEach((img) => img.classList.remove('selected'));
            this.classList.add('selected'); 
            document.getElementById('selected-image').src = this.getAttribute('src');

            const nameLabel = document.getElementById('name-label');
            nameLabel.innerText = 'Nombre: ' + this.getAttribute('src').split('/').pop();

            const commentBox = document.getElementById('comment-box');
            commentBox.value = imageMetaData['json'][this.getAttribute('src').split('/').pop()]['obs'];
        });
    });
});