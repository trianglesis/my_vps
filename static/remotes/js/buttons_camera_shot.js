// Run now - button listeners add when page is loaded.
$(document).ready(function () {
    buttonSnapShot(pushedSnapShot);
});


function buttonSnapShot(funcToRun) {
    let cameraShot = document.getElementsByClassName("run-camera-shot");

    if (cameraShot && cameraShot[0]) {
        for (let button of cameraShot) {
            if (!button.dataset['dvr']) {
                throw new Error("<=Run Now=> run-camera-shot buttons cannot be set without camera drv data attribute!")
            }
            if (!button.dataset['cam']) {
                throw new Error("<=Run Now=> run-camera-shot buttons cannot be set without camera cam data attribute!")
            }
            button.addEventListener("click", function () {
                funcToRun(button);
            });
        }
    }
}

function pushedSnapShot(button) {
    new RESTPostMakeShot(button);
}

function changeButtonSnapShotText(button, result, fallbackMessage) {
    // console.log(`Button pushed! Rest Sent! Now change button text with response, wait 1-2 sec and change text back to usual`)
    let cameraShot = document.getElementById(`${button.dataset['dvr']}-${button.dataset['cam']}`);
    let status = result.status
    let previousText = cameraShot.innerText
    if (!fallbackMessage) {
        cameraShot.innerText = status
        cameraShot.disabled = 'disabled';
    } else {
        cameraShot.innerText = fallbackMessage
        cameraShot.disabled = 'disabled';
    }
    // Wait for a few seconds, make button disabled, and then assign previous text back
    setTimeout(function () {
        new SetBackSnapshotButton(cameraShot, previousText);
    }, 5000);

}

function SetBackSnapshotButton(cameraShot, previousText) {
    // console.log("Set back previous text")
    cameraShot.innerText = previousText;
    cameraShot.disabled = '';
}


function RESTPostMakeShot(button) {
    // console.log("Sending request:" + button)
    $.ajax({
        type: "POST",
        dataType: "json",
        contentType: "application/x-www-form-urlencoded",
        url: `/remotes/remote_camera_shot/`,
        data: button.dataset,
        "beforeSend": function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings)
        },
        "success": function (result) {
            console.log(`Request sent!`, result)
            if (result && result.status) {
                // On success - run get task status:
                console.log(`Success`, result)
                let fallbackMessage = undefined;
                changeButtonSnapShotText(button, result, fallbackMessage)
            } else {
                console.log("Unsuccessful", result)
                let fallbackMessage = 'Nothing happened, error on the server side!';
                changeButtonSnapShotText(button, result, fallbackMessage)
            }
        },
        "error": function (result) {
            console.log("ERROR, something goes wrong... Output below:")
            console.error(result)
            let fallbackMessage = 'Nothing happened, error on the server side!';
            changeButtonSnapShotText(button, result, fallbackMessage)
        },
    });
}

