// static/easy-label/js/downloadData.js

document.getElementById('download-button').addEventListener('click', function () {
    // Prepare the data to be sent in the POST request
    const postData = {
        images_dir: images_dir_int,
        iconData: iconData,
        imageData: imageData,
        imageComments: imageComments,
    };

    // Send a POST request to the server
    fetch('/json-download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // CSRF token for Django
        },
        body: JSON.stringify(postData),
    })
        .then(response => response.blob()) // Convert response to blob
        .then(blob => {
            // Create a link and trigger the download
            const url = window.URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = 'easylabel.zip';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}