$(function() {

   $.fn.delay = function(options) {
        var timer;
        var delayImpl = function(eventObj) {
            if (timer != null) {
                clearTimeout(timer);
            }
            var newFn = function() {
                options.fn(eventObj);
            };
            timer = setTimeout(newFn, options.delay);
        }

        return this.each(function() {
            var obj = $(this);
            obj.bind(options.event, function(eventObj) {
                 delayImpl(eventObj);
            });
        });
    };

    $("a.photo-image").lightBox();
    
    $(".search").attr("autocomplete", "off")
    
    $(".search").delay({
        delay: 400,
        event: "keyup",
        fn: function(e) {
            if (e.keyCode == 27) {
                $("#live-search-results").hide();
            }
            else {
                var q = $(".search").attr("value");
                if (q.length == 0) {
                    $("#live-search-results").hide();
                }

                if (q.length > 2) {
                    $.get("live-search-results", {"q" : q}, function(data) {
                        $("#live-search-results").html(data);
                        $("#live-search-results").show();
                    });
                }
            }
        }
    });

});