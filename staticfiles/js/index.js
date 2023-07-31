/**
 * A base function to send ajax get request
 * @param {String} url the url to send the request
 * @param {String} csrf_token the CSRF token
 * @param {Dictionary} data the data to send
 * @param {function} success_callback 
 * @param {function} error_callback 
 */
function ajax_post_request(url, csrf_token, data, success_callback, error_callback) {
    $.ajax({
        type: "POST",
        url: url,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': csrf_token 
        },
        data: data,
        success: function (response) {
            success_callback(response);
        },
        error: function (response) {
            error_callback(response);
        }
    });
}

// PROJECT

function filter_project(){
    var project_name = $('#project-name').val();
    var project_counter = 0;

    $("#project-name").unbind('keypress');

    $('.project-container').each(function(){

        if($(this).attr("project-name").includes(project_name)){
            $(this).show();
            project_counter++;

            if(project_counter == 1){
                var project_open_button = $(this).find('.open-project-button');
                $("#project-name").keypress(function (e) {
                    if (e.which == 13) {
                        project_open_button.click();
                        $('#project-name').val("");
                    }
                });
            }
        }else{
            $(this).hide();
        }
    });

    if (project_counter == 0){
        $('#create-project-button').show();
    

        $("#project-name").keypress(function (e) {
            if (e.which == 13) {
                create_project();
            }
        });

    }else{
        $('#create-project-button').hide();
    }
}

function set_activated_project(project_id){
    if(project_id != ''){
        $('.open-project-button').removeClass('activated_project');
        $('.open-project-button[project_id='+project_id+']').addClass('activated_project');
    }
}

// TASK


// TIMER
function timer() {
    var timers = $(".timer");
    for (var i = 0; i < timers.length; i++) {
        var timer = timers[i];
        var start_time = $(timer).attr('start_time')*1000;
        var current_time = new Date().getTime();
        var time = current_time - start_time;

        var hours = Math.floor((time % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((time % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((time % (1000 * 60)) / 1000);
        var milliseconds = Math.floor((time % (1000 * 60)) / 100);

        hours = hours.toString().padStart(2, '0');
        minutes = minutes.toString().padStart(2, '0');
        seconds = seconds.toString().padStart(2, '0');

        $(timer).html(hours + ":" + minutes + ":" + seconds);
    }
}

function edit_timer(element){

    var ttid = $(element).attr('task_timer_id');
    $(`.send-edit-timer-button[task_timer_id="${ttid}"]`).show();

    $(`.edit-timer-button[task_timer_id="${ttid}"]`).hide();

    current_start_time = $(`.start_time[task_timer_id="${ttid}"]`).html().trim();
    current_end_time = $(`.end_time[task_timer_id="${ttid}"]`).html().trim();
    $(`.start_time[task_timer_id="${ttid}"]`).html(`<input type="text" class='start_time_edit' task_timer_id="${ttid}" value="${current_start_time}">`);
    $(`.end_time[task_timer_id="${ttid}"]`).html(`<input type="text" class='end_time_edit' task_timer_id="${ttid}" value="${current_end_time}">`);
}


// NOTE

// STATUS


