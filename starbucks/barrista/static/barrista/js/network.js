
var network = {};

network.get = function(url, callback, onerror)
{
    $.ajax({
        'url': url,
        'success': function(data) {
            if (callback != null)
                callback(data);
        },
        'error': function(jqXHR, errorText) {
            console.log("Error calling "+url+" : "+errorText);
            if (onerror)
                onerror(errorText, jqXHR);
        },
        'type': 'GET'
    });
}
