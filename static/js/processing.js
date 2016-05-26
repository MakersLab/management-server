$('#price-state').hide();

ajaxCallback=function (data) {
    data_decoded=JSON.parse(data);
    if (data_decoded['successful']) {
        $('#state').text('Successful');
        $('#time').text(data_decoded['print_time']);
        $('#price').text(data_decoded['price']);

        $('#done-processing').show();

    }
    else {
        $('#state').innerHTML = data['message'];
    }
};

$.ajax({
    type: 'POST',
    url: '/stl-pricing/slice',
    success: ajaxCallback,
    data: {filename: $('#filename').text()}
});

function startPrint() {
    
}