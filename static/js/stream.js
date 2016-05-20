/**
 * Created by Jakub on 20. 5. 2016.
 */
function startStream() {
showPrompt();
}
function stopStream() {
showPrompt();
}

function showPrompt() {
    var adress = prompt('Type in IP adress','192.168.2.9');
    console.log(adress);
}