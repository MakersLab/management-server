/**
 * Created by Jakub on 20. 5. 2016.
 */
function startStream() {
    streamControl('start');
}
function stopStream() {
    streamControl('stop');
}

function showPrompt() {
    var adress = prompt('Type in IP adress', '192.168.2.9');
    return adress;
}
function streamControl(method) {
    var adress = showPrompt();
    if (adress != null) {
        console.log('Calling JSON')
        $.ajax({
            type: 'POST',
            url: '/stream/control',
            success: ajaxCallback,
            data: {adress: adress, command: method}
        })
    }

}
ajaxCallback = function (data) {
    data_decoded = JSON.parse(data);
    console.log(data_decoded);
};