function ajax_post_request(url, csrf_token, data, success_callback, error_callback) {
    /**
     * A base function to send ajax get request
     * @param {String} url the url to send the request
     * @param {String} csrf_token the CSRF token
     * @param {Dictionary} data the data to send
     * @param {function} success_callback the function to call on success
     * @param {function} error_callback the function to call on error
     */

    // Send the request
    $.ajax({
        type: "POST",
        url: url,
        // csrf stands for Cross Site Request Forgery
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

/*
-------------------
    PROJECT
-------------------
*/

function filter_project(){
    /**
     * Filter the project based on the project name
     * The project name is taken from the input with id project-name
     */

    // Get the project name from the input field with id project-name
    var project_name_filter = $('#project-name').val();
    var project_name_filter_lower = project_name_filter.toLowerCase();

    // Initialize the project counter
    var project_counter = 0;

    // Why do we need to unbind the keypress event?
    $("#project-name").unbind('keypress');

    // Iterate thourgh all the project-container
    $('.project-container').each(function(){

        var project_name_lower = $(this).attr("project-name").toLowerCase(); 

        // If the project name contains the project name filter
        // The search is case insensitive
        if(project_name_lower.includes(project_name_filter_lower)){

            // Show the project-container
            $(this).show();
            // Increment the project counter
            project_counter++;
            
            // I want to bind the kepress enter to the open project button
            // I want to modify the code so that when the user press enter,
            // the most left project will be opened.
            // At the moment this is not quite reliable. 
            // TODO: Debug this
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
            // If the project does not match the project name, hide it
            $(this).hide();
        }
    });

    if (project_counter == 0){
        // If there is no project, show the create project button
        // User can also create a project by pressing enter
        $('#create-project-button').show();
    
        $("#project-name").keypress(function (e) {
            if (e.which == 13) {
                create_project();
            }
        });
    }else{
        // Hide the create project button
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


