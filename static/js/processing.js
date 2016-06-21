$('.done-processing').hide();
$('#state').hide();
var gcode_name;

ajaxCallback = function (data) {
    $('#state').hide();
    $('.done-processing').show();
    data_decoded = JSON.parse(data);

    var table = document.getElementById('slice-results');
    table.innerHTML = '';
    
    for (var i = 0; i < data_decoded['results'].length; i++) {
        var row = table.insertRow(i);

        var cell0 = row.insertCell(0);
        var cell1 = row.insertCell(1);
        var cell2 = row.insertCell(2);

        cell0.innerHTML = data_decoded['results'][i]['used-profile'];
        cell1.innerHTML = data_decoded['results'][i]['print_time'];
        cell2.innerHTML = data_decoded['results'][i]['price'];
    }
    gcode_name = data_decoded['gcode'];
};

function slice() {
    $('#state').show();
    selectedProfiles = [];
    $('.profiles-list').each(function (index) {
        selectedProfiles[index] = {
            index: parseInt(this.name),
            slice: this.checked
        };
    });
    request = {
        profiles: JSON.stringify(selectedProfiles),
        filename: $('#filename').text()
    };
    $.ajax({
        type: 'POST',
        url: '/stl-pricing/slice',
        success: ajaxCallback,
        data: request
    });
}
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