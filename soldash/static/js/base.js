function fadeInAndOut() {
    $(".fade_in_and_out").animate({opacity: 1.0}, {duration: 1000})
        .animate({opacity: 0}, {duration: 1000})
        .animate({opacity: 1.0}, {duration: 1000, complete: fadeInAndOut});
}

function filelist(hostname, core, indexVersion) {
    $.ajax({
        url: '/execute/filelist?hostname='+hostname+'&core='+core+'&indexversion='+indexVersion,
        type: 'GET',
        data: '',
        async: false,
        success: function(data, status, jqXHR){
            html = "<table><tr><th>Name</th><th>Size</th><th>Last Modified</th></tr>";
            $.each(data['data']['filelist'], function(index, value) {
                html += "<tr><td class='name'>"+value['name']+"</td>";
                html += "<td class='size'>"+(value['size'] / (1024*1024)).toFixed(2)+"MB</td>";
                var dt = new Date(value['lastmodified']);
                html += "<td class='lastmodified'>"+dt.toUTCString()+"</td></tr>";
            })
            html += "</table>"
            $.modal(html);
        }
    });
}

function openQueryDialog(hostname, core) {
    var html = '<form name="queryForm"><textarea rows="4" cols="30" name="q">solr</textarea><input name="version" type="hidden" value="2.2">';
    html += '<input name="start" type="hidden" value="0"><input name="rows" type="hidden" value="10">';
    html += '<input name="indent" type="hidden" value="on">';
    html += '<br><input type="submit" value="search" onclick="submitQuery(\''+hostname+'\', \''+core+'\', queryForm.q.value)"></form>';
    $.modal(html);
}

function submitQuery(hostname, core, query) {
    window.open('/execute/select?hostname='+hostname+'&core='+core+'&q='+query);
}

function main() {
    $(function(){
      var count = 20;
      $("span.countdown").html("Reloading in "+count+"...");
      countdown = setInterval(function(){
            $("span.countdown").html("Reloading in "+count+"...");
            if (count == 0) {
                $("span.countdown").html("Reloading...");
                window.location.reload();
            }
            if($('#simplemodal-container').length == 0) {
                count--;
            }
        }, 1000);
    });

    $(".command.server_side a").throbber("click");
    
    fadeInAndOut();
}

main();