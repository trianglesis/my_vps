$(document).ready(function () {
    console.log("Main page ready");
    setInterval(runContinuously, 2000);  /* 3000 = 3 sec */
});

function runContinuously() {
    console.log("Refreshing camera views");
    let cameras = document.getElementsByClassName('cam-refresh');
    let cam_card_datetime = document.getElementsByClassName('current-time');
    for (let cam of cameras) {
        replaceCamView(cam)
    }
    for (let card_txt of cam_card_datetime) {
        currentDateTime(card_txt)
    }
}

function replaceCamView(camObj) {
    camObj.src = camObj.src + "&" + Date.now();
}

function currentDateTime(camCard) {
    let today = new Date();
    camCard.textContent = ''
    camCard.textContent = today.toLocaleTimeString();

}
