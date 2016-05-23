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
    address = prompt('Type in IP adress', '192.168.2.9');
    return address;
}
function streamControl(method) {

    if (($('#stream-key').val() != '' && method == 'start') || ( method == 'stop')) {
        var key = $('#stream-key').val();
        var printer = $('#printer-list option:selected').val();
            $.ajax({
                type: 'POST',
                url: '/stream/control',
                success: ajaxCallback,
                data: {address: address, command: method, key: key, printer: printer}
            });
    }
    else {
        alert('Stream key input is empty.')
    }
}
ajaxCallback = function (data) {
    data_decoded = JSON.parse(data);
    console.log(data_decoded);
    alert(data_decoded['message']);

};