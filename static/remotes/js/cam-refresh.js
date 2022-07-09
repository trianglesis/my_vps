$(document).ready(function () {
    // window.setInterval("runContinuously();", 100); // one second interval
    document.cookie = "Set-Cookie: widget_session=abc123; SameSite=None"
    setInterval(runContinuously, 2000);  /* 3000 = 3 sec */
});

function runContinuously() {

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
    let dvr = camObj.dataset.dvr
    let cam = camObj.dataset.cam
    camObj.src = `${perl_hostname}cam.php?dvr=${dvr}&cam=${cam}&r=${Date.now()}`;


}

function currentDateTime(camCard) {
    let today = new Date();
    camCard.textContent = ''
    camCard.textContent = today.toLocaleTimeString();

}
