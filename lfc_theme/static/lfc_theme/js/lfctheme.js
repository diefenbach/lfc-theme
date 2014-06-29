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

$(function() {
    $("a.lightbox").lightBox();

    $("#search-form").keypress(function(e) {
        if (e.keyCode == 13) {
            var url = $("#live-search-results .selected a").attr("href");
            if (url) {
                window.location = url;
                return false;
            }
            else {
                return true;
            }
        }
        else {
          return true;
        }
    });

    $(".search").attr("autocomplete", "off")
    $(".search").focus();

    $(".search").keyup(function(e) {
        var current = $("#live-search-results .selected")

        // ESC
        if (e.keyCode == 27) {
            $("#live-search-results").hide();
        }

        // UP
        else if (e.keyCode == 38) {
            var prev = $("#live-search-results .selected").prev("#live-search-results div.item");

            if (prev.html()) {
                prev.addClass("selected");
            }
            else {
                $("#live-search-results div.item:last").addClass("selected");
            }
            current.removeClass("selected");
        }

        // RIGHT
        else if (e.keyCode == 39) {
            var url = $("#live-search-results .selected a").attr("href");
            if (url)
                window.location = url;
        }

        // DOWN
        else if (e.keyCode == 40) {
            var next = $("#live-search-results .selected").next("#live-search-results div.item");
            if (next.html()) {
                next.addClass("selected");
            }
            else {
                $("#live-search-results div.item:first").addClass("selected");
            }
            current.removeClass("selected");
        }

    })

    $(".search").delay({
        delay: 400,
        event: "keyup",
        fn: function(e) {
            if (e.keyCode in {13:1, 27:1, 38:1, 39:1, 40:1} == false) {
                var q = $(".search").val();
                if (q.length == 0) {
                    $("#live-search-results").hide();
                }

                if (q.length > 0) {
                    var url = $("#search-form").attr("data");
                    $.get(url, {"q" : q}, function(data) {
                        $("#live-search-results").html(data);
                        $("#live-search-results").show();
                    });
                }
            }
        }
    });

});
