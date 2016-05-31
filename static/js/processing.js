$('.done-processing').hide();

var gcode_name;

ajaxCallback = function (data) {
    data_decoded = JSON.parse(data);
    if (data_decoded['successful']) {
        $('#state').text('Successful');
        $('#time').text(data_decoded['print_time']);
        $('#price').text(data_decoded['price']);

        $('.done-processing').show();

    }
    else {
        $('#state').innerHTML = data['message'];
    }
    gcode_name = data_decoded['gcode'];
};

$.ajax({
    type: 'POST',
    url: '/stl-pricing/slice',
    success: ajaxCallback,
    data: {filename: $('#filename').text()}
});

//////////////////////
printCallback = function (data) {
    data = JSON.parse(data);
    alert(data['successful']);
};

function startPrint() {
    printer = $('#printer-list option:selected').val();

    $.ajax({
        type: 'POST',
        url: '/stl-pricing/print',
        success: printCallback,
        data: {printer: printer, gcode: gcode_name}
    });
}