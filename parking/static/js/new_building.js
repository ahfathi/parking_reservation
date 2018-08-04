function generate_slot(id) {
    return $("<div class=\"slot\" id=\"" + id + "\"><input type=\"text\"> <p id=\"hint\"></p></div>").html();
}
function generate_segment(id) {
    return $("<div class=\"segment\" id=\"" + id + "\"><input type=\"text\"> <p id=\"hint\"></p>" + generate_slot(0) + "</div>").html();
}

function generate_floor(id) {
    return $("<div class=\"floor\" id=\"" + id + "\"><input type=\"text\"> <p id=\"hint\"></p>" + generate_segment(0) + "</div>").html();
}

$(document).ready(function(){
    $("#building").append(generate_floor(0));
    $("input").focus(function() {
        var div = $(this).prev();
        var parent = $(this).parent();
        $(this).bind("keypress", function(event) {
            if (event.which == 13) { //Enter 13
                if (div.attr("class") === "slot") {
                    parent.append(generate_slot(div.id + 1));
                }
                else if (div.attr("class" == "segment")) {
                    parent.append(generate_segment(div.id + 1));
                }
                else if (div.attr("class" == "floor")) {
                    parent.append(generate_floor(div.id + 1));
                }
            }
            else if (event.which == 9) { //tab 9
                
            }
        });
    });
    $("#submit").click(function() {
        var building = {"label": $("#building").next().val(), "floors": []};
        var error = false;
        $("#building").children("div").each(function(floor_id){
            var value = $(this).next().val();
            if (value === "") {
                $(this).next().next().text("please full up this place");
                error = true;
                return false;
            }
            building["floors"][floor_id] = {"label": value, "segments": []};
            $(this).children("div").each(function(segment_id){
                var value = $(this).next().val();
                if (value === "") {
                    $(this).next().next().text("please full up this place");
                    error = true;
                    return false;
                }
                building["floors"][floor_id]["segments"][segment_id] = {"label": value, "slots": []};
                $(this).children("div").each(function(slot_id){
                    var value = $(this).next().val();
                    if (value === "") {
                        $(this).next().next().text("please full up this place");
                        error = true;
                        return false;
                    }
                    building["floors"][floor_id]["segments"][segment_id]["slots"][slot_id] = value;
                });
            });
        });
        if (error === false) {
            //send data
        }
    });
});