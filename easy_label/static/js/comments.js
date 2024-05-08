function saveComment(){
    const commentBox = document.getElementById('comment-box');
    const selectedImgName = document.getElementById('selected-image').getAttribute('src').split('/').pop();
    imageMetaData.json[selectedImgName].obs = commentBox.value;
};