function playVideo() {
    var video = document.getElementById("myVideo");
    video.play();
}

function pauseVideo() {
    var video = document.getElementById("myVideo");
    video.pause();
}

function stopVideo() {
    var video = document.getElementById("myVideo");
    video.pause();
    video.currentTime = 0;
}

function loadVideo(videoFile) {
    var video = document.getElementById("myVideo");
    var source = document.getElementById("videoSource");
    source.src = videoFile;
    video.load();
}

function showNoteInput() {
    const type = document.getElementById('type').value;
    const textInput = document.getElementById('text-input');
    const fileInput = document.getElementById('file-input');

    if (type === 'text') {
        textInput.style.display = 'block';
        fileInput.style.display = 'none';
    } else {
        textInput.style.display = 'none';
        fileInput.style.display = 'block';
    }
}

