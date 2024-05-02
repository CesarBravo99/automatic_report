// document.addEventListener('DOMContentLoaded', function () {
//     document.getElementById('download-btn').addEventListener('click', function () {
   
        // alert('asd')
        
        // const postData = {
        //     imageMetaData: imageMetaData,
        // };

        // fetch('/download', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'X-CSRFToken': getCookie('csrftoken'), // CSRF token for Django
        //     },
        //     body: JSON.stringify(postData),
        // })
        // fetch('download', {
        //     method: 'GET',
        // })

        // .then(response => response.blob()) // Convert response to blob
        // .then(blob => {
        //     // Create a link and trigger the download
        //     const url = window.URL.createObjectURL(blob);
        //     const downloadLink = document.createElement('a');
        //     downloadLink.href = url;
        //     downloadLink.download = 'easylabel.zip';
        //     document.body.appendChild(downloadLink);
        //     downloadLink.click();
        //     document.body.removeChild(downloadLink);
        //     window.URL.revokeObjectURL(url);
        // })
        // .catch(error => {
        //     console.error('Error:', error);
        //     alert('Error: ' + error.message);
        // });
//     });
// });


function downloadJson(){
    const postData = {
        imageMetaData: imageMetaData,
    };
    fetch('/download/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // CSRF token for Django
        },
        body: JSON.stringify(postData),
    })
    .then(response => response.blob())
    // .then(blob => {
    //     const url = window.URL.createObjectURL(blob);
    //     const downloadLink = document.createElement('a');
    //     downloadLink.href = url;
    //     downloadLink.download = 'easylabel.zip';
    //     document.body.appendChild(downloadLink);
    //     downloadLink.click();
    //     document.body.removeChild(downloadLink);
    //     window.URL.revokeObjectURL(url);
    // })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    });

}


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
};