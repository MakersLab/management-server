$('#price-state').hide();

ajaxCallback=function (data) {
    data_decoded=JSON.parse(data);
    if (data_decoded['successful']) {
        console.log('got successful');
        $('#state').text('Successful');
        $('#time').text(data_decoded['print_time']);
        $('#price').text(data_decoded['price']);

        $('#price-state').show();

        console.log('This better be called');
    }
    else {
        $('#state').innerHTML = data['message'];
        console.log('This better not be called')
    }
};

$.ajax({
    type: 'POST',
    url: '/stl-pricing/slice',
    success: ajaxCallback,
    data: {filename: $('#filename').text()}
});
