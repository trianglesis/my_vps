$(document).ready(function () {
    console.log("Main page ready");
    setInterval(runContinuously, 2000);  /* 3000 = 3 sec */
});

function runContinuously() {
    console.log("Refreshing camera views");
    let cameras = document.getElementsByClassName('cam-refresh');
    for (let cam of cameras) {
        replaceCamView(cam)
    }
}

function replaceCamView(camObj) {
    camObj.src = camObj.src + "&" + Date.now();
}
