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
    var project_name = $('#project_name').val();
    var project_counter = 0;

    $("#project_name").unbind('keypress');

    $('.project-container').each(function(){
        if($(this).attr('project_name').includes(project_name)){
            $(this).show();
            project_counter++;

            if(project_counter == 1){
                var project_open_button = $(this).find('.open-project-button');
                $("#project_name").keypress(function (e) {
                    if (e.which == 13) {
                        project_open_button.click();
                        $('#project_name').val("");
                    }
                });
            }
        }else{
            $(this).hide();
        }
    });

    if (project_counter == 0){
        $('#create_project_button').show();
    

        $("#project_name").keypress(function (e) {
            if (e.which == 13) {
                create_project();
            }
        });

    }else{
        $('#create_project_button').hide();
    }
}

function set_activated_project(project_id){
    if(project_id != ''){
        $('.open-project-button').removeClass('activated_project');
        $('.open-project-button[project_id='+project_id+']').addClass('activated_project');
    }
}

// TASK
function unbine_task_event(){
    $('.open-project-button').unbind();

    $("#create_task_button").unbind();
    $("#task_name").unbind();
    $(".start_task_button").unbind();
    $(".stop_task_button").unbind();
    $(".delete_timer_button").unbind();
    $('.edit_timer_button').unbind();
    $('.send_edit_timer_button').unbind();
    $('.delete_task_button').unbind();
    $('.view_task_button').unbind();
    $('.edit-start-time-button').unbind();

    $('#project_status').unbind();

}

function connect_task_event(){
    
    unbine_task_event();

    $('.open-project-button').click(function () {
        open_project(this);
        load_notes(this);
    });
    

    $('.open-project-button').mousedown(function () {

        const delete_button = $(this).siblings('.delete-project-button');
        const timeout_id = setTimeout(function(){
            delete_button.show()
        }, 300);
        console.log(timeout_id)

        $(this).data("timeout_id", timeout_id)
        
    });

    $('.open-project-button').mouseup(function () {
        const timeout_id = $(this).data("timeout_id")
        if (timeout_id != null){
            clearTimeout(timeout_id);
            const delete_button = $(this).siblings('.delete-project-button');
            delete_button.hide();
            $(this).removeData("timeout_id");
        }
    });


    $("#create_task_button").click(function () {
        console.log("Sending request to create task");
        create_task();
    });

    $("#task_name").keypress(function (e) {
        if (e.which == 13) {
            create_task();
        }
    });

    $(".start_task_button").click(function () {
        start_task(this);
    });

    $(".stop_task_button").click(function () {
        stop_task(this);
    });

    $(".view_task_button").click(function () {

        var task_id = $(this).attr('task_id');
        
        open_task(task_id);
    });

    $(".delete_task_button").click(function () {
        delete_task(this);
    });

    $('#project-status').change(function () {
        var project_id = $('#project_detail_modal').attr('project_id');
        var project_status_id = $(this).val();
        set_project_status(project_id, project_status_id);
    });

    $('.task-status').change(function () {
        var task_id = $(this).attr('task_id');
        var task_status_id = $(this).val();
        set_task_status(task_id, task_status_id);
    });
}


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
    var send_edit_timer_button= $(`.send_edit_timer_button[task_timer_id="${ttid}"]`);
    send_edit_timer_button.show();

    var edit_timer_button = $(`.edit_timer_button[task_timer_id="${ttid}"]`);
    edit_timer_button.hide();

    current_start_time = $(`.start_time[task_timer_id="${ttid}"]`).html().trim();
    current_end_time = $(`.end_time[task_timer_id="${ttid}"]`).html().trim();
    $(`.start_time[task_timer_id="${ttid}"]`).html(`<input type="text" class='start_time_edit' task_timer_id="${ttid}" value="${current_start_time}">`);
    $(`.end_time[task_timer_id="${ttid}"]`).html(`<input type="text" class='end_time_edit' task_timer_id="${ttid}" value="${current_end_time}">`);
}

function connect_task_timer_event(){
    $(".delete_timer_button").click(function () {
        delete_timer(this);
    });


    $('.edit_timer_button').click(function () {
        edit_timer(this);
    });

    $('.send_edit_timer_button').click(function () {
        send_edit_timer(this);
    });
}



// NOTE
function unbine_note_evet(){
    $('.new_note_submit').unbind();
    $('.delete_note').unbind();
}

function connect_note_event(){
    unbine_note_evet();
    $('#new_note_submit').click(function () {
        create_note();
    });


    $('.delete_note').click(function () {
        delete_note(this);
    });
}

// STATUS


