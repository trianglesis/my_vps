// Run now - button listeners add when page is loaded.
$(document).ready(function () {
    // console.log("<=Run Now=> Init event listener assign for test run now buttons")
    buttonRunNowEventListenerAssign(pushedButtonSendRequest);
});


function buttonRunNowEventListenerAssign(funcToRun) {
    // console.log("<=Run Now=> Test run now buttons assigning listener!")

    let openGates = document.getElementsByClassName("run-open-gates");

    if (openGates && openGates[0]) {

        for (let btn of openGates) {
            if (!btn.dataset['nonce']) {
                throw new Error("<=Run Now=> run-open-gates buttons cannot be set without token data attribute!")
            }
            if (!btn.dataset['dom']) {
                throw new Error("<=Run Now=> run-open-gates buttons cannot be set without dom data attribute!")
            }
            if (!btn.dataset['gate']) {
                throw new Error("<=Run Now=> run-open-gates buttons cannot be set without gate data attribute!")
            }
            if (!btn.dataset['mode']) {
                throw new Error("<=Run Now=> run-open-gates buttons cannot be set without mode data attribute!")
            }

            // console.log("<=Run Now=> Assign listener for button with case id: " + btn.dataset['case_id'])
            btn.addEventListener("click", function () {
                funcToRun(btn);
            });
        }
    }
}


function pushedButtonSendRequest(btn) {
    // console.log(`<=Run Now=> btn:`,  btn)
    // console.log(`<=Run Now=> btn.dataset:`, btn.dataset)
    // console.log(`perl_token: `, perl_token)
    // console.log(`perl_hostname: `, perl_hostname)

    btn.dataset.perl_token = perl_token
    btn.dataset.perl_hostname = perl_hostname

    console.log(btn.dataset);
    new RESTPostTask(btn);
}


function changeButtonText(btn, result, fallbackMessage) {
    console.log(`Button pushed! Rest Sent! Now change button text with response, wait 1-2 sec and change text back to usual`)
    let status = result.status
    let previousText = btn.innerText

    if (!fallbackMessage) {
        btn.innerText = status
        btn.disabled = 'disabled';
    } else {
        btn.innerText = fallbackMessage
        btn.disabled = 'disabled';
    }


    // Wait for a few seconds, make button disabled, and then assign previous text back
    setTimeout(function () {
        new SetButtonBack(btn, previousText);
    }, 5000);

}

function SetButtonBack(btn, previousText) {
    // btn.css("background-color", previousColor);
    btn.innerText = previousText;
    btn.disabled = '';
}


function RESTPostTask(btn) {
    $.ajax({
        type: "POST",
        dataType: "json",
        // dataType: "jsonp",
        contentType: "application/x-www-form-urlencoded",
        // contentType: "application/json; charset=utf8",
        url: `/remotes/remote_open/`,
        data: btn.dataset,
        "beforeSend": function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings)
        },
        "success": function (result) {
            console.log(`Request sent!`, result)
            if (result && result.status) {
                // On success - run get task status:
                console.log(`Success`, result)
                let fallbackMessage = undefined;
                changeButtonText(btn, result, fallbackMessage)
            } else {
                console.log("Unsuccessful", result)
                let fallbackMessage = 'Nothing happened, error on the server side!';
                changeButtonText(btn, result, fallbackMessage)
            }
        },
        "error": function (result) {
            console.log("ERROR, something goes wrong... Output below:")
            console.error(result)
            let fallbackMessage = 'Nothing happened, error on the server side!';
            changeButtonText(btn, result, fallbackMessage)
        },
    });
}

