function create_project() {
    var project_name = $("#project_name").val();

    if(project_name == ""){
        alert("Please enter a project name");
        return;
    }

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:create_project' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_name': project_name,
        },
        success: function (response) {
            $("#project_name").val("");
            location.reload();
        },
        error: function (response) {
            console.log(response);
        }
    });
}


function filter_project(){
    var project_name = $('#project_name').val();
    var project_counter = 0;

    $("#project_name").unbind('keypress');

    $('.project_container').each(function(){
        if($(this).attr('project_name').includes(project_name)){
            $(this).show();
            project_counter++;

            if(project_counter == 1){
                var project_open_button = $(this).find('.open_project_button');
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

function delete_project(element) {
    var project_id = $(element).attr("project_id");

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:delete_project' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id,
        },
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function set_project_status(project_id, project_status_id){
    $.ajax({
        url: "{% url 'time_tracker:set_project_status' %}",
        type: 'POST',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            project_id: project_id,
            project_status_id: project_status_id 
        },
        success: function (data) {
            console.log(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function set_task_status(task_id, task_status_id){
    $.ajax({
        url: "{% url 'time_tracker:set_task_status' %}",
        type: 'POST',
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_id': task_id,
            'task_status_id': task_status_id 
        },
        success: function (data) {
            console.log(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function reload_project_detail(){
    var project_id = $('#project_detail_modal').attr('project_id');
    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:project_detail' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id,
        },
        success: function (response) {
            $('#project_detail_modal').html(response);
            $('#project_detail_modal').attr('project_id', project_id);
            connect_task_event();
            load_timeline(project_id);
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function reload_note_detail(){
    var project_id = $('#project_detail_modal').attr('project_id');
    
    $.ajax({
        type: "POST",
        url: "{% url 'sticky_note:view_notes' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id,
        },
        success: function (response) {
            $("#sticky_note_modal").html(response);
            $("#sticky_note_modal").attr('project_id', project_id);
            connect_note_event();
        },
        error: function (response) {
            console.log(response);
        }
    });
}

// a javascript function that take the value of the input and do a post request to the server 
function create_task() {
    var task_name = $("#task_name").val();
    var project_id = $('#project_detail_modal').attr('project_id');
    

    if(task_name == ""){
        alert("Please enter a task name");
        return;
    }

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:create_task' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_name': task_name,
            'project_id': project_id,
        },
        success: function (response) {
            $("#task_name").val("");
            reload_project_detail();
        },
        error: function (response) {
            console.log(response);
        }
    });
}


function start_task(element) {
    var task_id = $(element).attr('task_id');
    var user_id = $('.current_user').attr('user_id');

    
    if(task_id == ""){
        alert("no valid task id");
        return;
    }

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:create_task_timer' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_id': task_id,
            'user_id': user_id,
        },
        success: function (response) {
            reload_project_detail()
        },
        error: function (response) {
            console.log(response);
        }
    });
}


function stop_task(element) {
    var active_task_id = $(element).attr('active_task_id');
    var user_id = $('.current_user').attr('user_id');
    
    if(active_task_id== ""){
        alert("no valid task id");
        return;
    }

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:stop_task_timer' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'active_task_id': active_task_id,
            'user_id': user_id
        },
        success: function (response) {
            reload_project_detail(); 
            
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function delete_timer(element) {
    var task_timer_id = $(element).attr('task_timer_id');
    
    var task_id = $('#task_detail_modal').attr('task_id');

    if(task_timer_id== ""){
        alert("no valid task id");
        return;
    }

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:delete_task_timer' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_timer_id': task_timer_id,
        },
        success: function (response) {
            open_task(task_id);
        },
        error: function (response) {
            console.log(response);
        }
    });
}


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

function send_edit_timer(element){

    var ttid = $(element).attr('task_timer_id');

    var task_id = $('#task_detail_modal').attr('task_id');
    start_time_value = $(`.start_time_edit[task_timer_id="${ttid}"]`).val().trim();
    end_time_value = $(`.end_time_edit[task_timer_id="${ttid}"]`).val().trim();

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:edit_task_timer' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_timer_id': ttid,
            'start_time_value': start_time_value,
            'end_time_value': end_time_value,
        },
        success: function (response) {
            open_task(task_id);
        },
        error: function (response) {
            console.log(response);
        }
    });

}

function create_note(){

    var user_id = $('.current_user').attr('user_id');
    var project_id = $('#sticky_note_modal').attr('project_id');

    var note_name = $('#new_note_name').val().trim();
    var content = $('#new_note_content').val().trim();

    if(note_name == '' && content==''){
        alert('please fill all fields');
        return;
    }

    $.ajax({
        type: "POST",
        url: "{% url 'sticky_note:create_note' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id,
            'name': note_name,
            'content': content,
            'user_id': user_id
        },
        success: function (response) {
            console.log('success');
            reload_note_detail();
        },
        error: function (response) {
            console.log(response);
        }
    });

}
function delete_note(element){
    
    var note_id= $(element).attr('note_id');


    $.ajax({
        type: "POST",
        url: "{% url 'sticky_note:delete_note' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'note_id': note_id,
        },
        success: function (response) {
            console.log('success');
            reload_note_detail()
        },
        error: function (response) {
            console.log(response);
        }
    });

}


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

function unbine_task_event(){
    $('.open_project_button').unbind();

    $("#create_task_button").unbind();
    $("#task_name").unbind();
    $(".start_task_button").unbind();
    $(".stop_task_button").unbind();
    $(".delete_timer_button").unbind();
    $('.edit_timer_button').unbind();
    $('.send_edit_timer_button').unbind();
    $('.delete_task_button').unbind();
    $('.view_task_button').unbind();

    $('#project_status').unbind();

}

function connect_task_event(){
    
    unbine_task_event();

    $('.open_project_button').click(function () {
        open_project(this);
        load_notes(this);
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

function open_project(element) {
    var project_id = $(element).attr('project_id');

    
    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:project_detail' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id,
        },
        success: function (response) {
            $("#project_detail_modal").html(response);
            $("#project_detail_modal").attr('project_id', project_id);

            $("#task_detail_modal").hide();
            set_activated_project(project_id);

            connect_task_event();
            load_timeline(project_id);
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function set_activated_project(project_id){
    $('.open_project_button').removeClass('activated_project');
    $('.open_project_button[project_id='+project_id+']').addClass('activated_project');
}


function load_status(status_id) {
    $.ajax({
        type: "POST",
        url: "{% url 'status:status_detail' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'status_id': status_id,
        },
        success: function (response) {
            $("#status_detail_modal").html(response);
            $("#status_detail_modal").attr('status_id', status_id);
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function load_timeline(project_id) {
    
    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:timeline' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id
        },

        success: function (response) {
            $("#timeline-container").html(response);
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function load_notes(element) {
    var project_id = $(element).attr('project_id');

    $.ajax({
        type: "POST",
        url: "{% url 'sticky_note:view_notes' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'project_id': project_id,
        },
        success: function (response) {
            $("#sticky_note_modal").html(response);
            $("#sticky_note_modal").attr('project_id', project_id);
            connect_note_event()    
        },
        error: function (response) {
            console.log(response);
        }
    });
}


function open_task(task_id) {

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:task_detail' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_id': task_id,
        },
        success: function (response) {
            $("#task_detail_modal").html(response);
            $("#task_detail_modal").attr('task_id', task_id);
            $("#task_detail_modal").show();

            connect_task_timer_event();
        },
        error: function (response) {
            console.log(response);
        }
    });
}


function delete_task(element) {
    var task_id = $(element).attr('task_id');

    $.ajax({
        type: "POST",
        url: "{% url 'time_tracker:delete_task' %}",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            'X-CSRFToken': '{{ csrf_token }}'
        },
        data: {
            'task_id': task_id,
        },
        success: function (response) {
            reload_project_detail();
        },
        error: function (response) {
            console.log(response);
        }
    });
}