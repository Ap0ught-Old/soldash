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
            count--;
        }, 1000);
    });

    $(".command.server_side a").throbber("click");
    
    fadeInAndOut();
}

main();