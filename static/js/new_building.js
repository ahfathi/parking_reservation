function generate_slot(id) {
    return '<div class="slot" id="' + id +'">Slot: <input type="text"/></div>';
}
function generate_segment(id) {
    return '<div class="segment" id="' + id +'">Segment: <input type="text"/>' + generate_slot(0) + '</div>';
}
function generate_floor(id) {
    return '<div class="floor" id="' + id +'">Floor: <input type="text"/>' + generate_segment(0) + '</div>';
}

$(document).ready(function() {
    $("#building").append(generate_floor(0));
    $(document).on("focus", "input", function() {
        var div = $(this).parent();
        $(this).bind("keydown", function(event) {
            if (event.which == 13 && event.shiftKey) {
                div.siblings("input").focus();
            }
            else if (event.which == 13) {
                if (div.next().text() != "") {
                    return false;
                }
                id = parseInt(div.attr("id")) + 1;
                if (div.attr("class") == "slot") {
                    div.after(generate_slot(id));
                }
                else if (div.attr("class") == "segment") {
                    div.after(generate_segment(id));
                }
                else if (div.attr("class") == "floor") {
                    div.after(generate_floor(id));
                }
                div.next().children().first().focus();
            }
        });
    });
    $("button.submit").click(function() {
        var buil = $("#building").children().first()
        label = buil.val()
        var error = false;
        if (label == "") {
            error = true;
        }
        var building = {"label": label, "floors": []}
        buil.siblings().each(function(floor_id) {
            var floor = $(this).children().first();
            var label = floor.val();
            if (label == "" || error == true) {
                error = true;
                return false;
            }
            building["floors"][floor_id] = {"label": label, "segments": []};
            floor.siblings().each(function(segment_id) {
                var segment = $(this).children().first();
                var label = segment.val();
                if (label == "" || error == true) {
                    error = true;
                    return false;
                }
                building["floors"][floor_id]["segments"][segment_id] = {"label": label, "slots": []};
                segment.siblings().each(function(slot_id) {
                    var label = $(this).children().first().val();
                    if (label == "") {
                        error = true;
                        return false;
                    }
                    building["floors"][floor_id]["segments"][segment_id]["slots"][slot_id] = label;
                });
            });
        });
        if (error == true) {
            $("p.error").text("please full up all the entries");
        }
        else {
            //submit
            $.post("/management/buildings/new/", JSON.stringify(building), function(response) {
                console.log(response);
                var redirect_url = response.split("\r\n")[2].slice(16);
                window.location.replace(redirect_url);
            });
        }
    });
});