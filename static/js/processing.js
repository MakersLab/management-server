$('#price-state').hide();

request = new XMLHttpRequest();
request.onreadystatechange = function () {
    if (request.readyState == 4 && request.status == 200) {
        textJson = request.responseText;
        data = JSON.parse(textJson);
        console.log(data);
        console.log('JSON was successful');
        if (data['successful']) {
            console.log('got successful');
            $('#state').text('Successful');
            $('#price').text(data['price']);
            $('#price-state').show();
        }
        else {
            $('#state').innerHTML = 'There was an error. Try again later';
        }

    }
};
request.open('POST', '/slicing', true);
request.send();

console.log('Called');