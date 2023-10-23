# crontab jobs 

## Resetings Repeatable Todo:

python manage.py checkRepeatableTodos

using djang-cron for now but APScheduler might be an alternative?
run at mid-night every day
0 0 * * * python manage.py checkRepeatableTodos

python manage.py crontab add
python manage.py crontab show


For json responses:
- 'success': true if the request is a success

# sticky_note

This is an app that provides the sticky notes to the system

## template
-> note_view: create note + list all notes

-> StickyNote
    - user
    - project
    - name
    - note
    - status 
  
-> Views
    - view_notes 
    - create_note
    - delete_note


# TODO:

2023/07/31:
- [X] ~~*Adding html location tag for each html page:*~~ [2023-10-01]
    - eg. <!-- time_tracker/templates/time_tracker/index.html-->
- [X] ~~*Review time_tracker/views.py*~~ [2023-10-02]
  - [X] ~~*Function comments*~~ [2023-10-02]
  - [X] ~~*Other comments and notes*~~ [2023-10-02]
- [X] ~~*Fix the display bug when "All" is selected as project*~~ [2023-10-07]
- [X] ~~*UI improvement*~~ [2023-10-08]
    - [X] ~~*Integrate Priority Display*~~ [2023-10-08]
      - [X] ~~*Sort todo by priority*~~ [2023-10-08]
      - NOTE -> currently we are doing this in a very non-dynamic way
    - [X] ~~*Saved note styling*~~ [2023-10-07] 


2023/08/06
- [X] ~~*Adding a logging system for the python code*~~ [2023-10-10]
  - NOTE: there are two handlers
    - Console handler print out the simple version of the log
    - File handler print out the verboose version of the log
      - By default the file handler is saved to .logs / debug.log
- [X] ~~*Add Eisenhower Matrix to UI/webview*~~ [2023-10-23]
- [ ] Add the task_timer's note to the UI/webview
  - The purpose of task_timer's note is like a short diary/note on what was done during that time.
    - [ ] A button on active task to add note using the single/focus view
    - [ ] The task timer view need some update + a button to edit the note for that task timer
- [ ] Add the Project and Task description to the UI/webview

2023/10/01
- [ ] Refactoring -> time_tracker/views.py
  - [ ] in  the index function also send title to the template -> code it to do something meaningful such as a custom name for the tracker
  - [ ] project_detail function seem to have some query that can be optimized 

2023/10/02
- [ ] Idea: 
  - [ ] reviewable component such as audio reviewable with the ability to add notes
  - [ ] using eq as a way to zoom on the element that needed to be reviewed


2023/10/07
- [ ] Change the CODE ME in the title to the name of the currently active Project and Task
- [ ] When a project is selected -> the url also change so that if the user restart they don't loose where they are and have to start from fresh
- [ ] Test if it make more sense to have an add note button to focus user on an area to add note instead of having it kind of attach to the note section at the moment. 
- [ ] Add the feature where user can edit old notes and the title should not be an input field =))


2023/10/23:
- update active task display to be fixed to the bottom 
- [ ] single_todo.html needed to be edit so that it can send edited data to server. E.G. when the Eissenhower matrix is edited -> [Save] -> Data is sent to the server


LOW-PRIO TODO:
- [ ] Debug static/js/index,js so that when the user press enter while they are in the project filter, the page will open the most left project
- [ ] DEBUG -> whenever the timer stop the timeline does not stop
- [ ] Adding registration page
- [ ] Investigate "Style sheet could not be loaded `static/scss/bootstrap.scss`
- [ ] When timeline in clicked, do something
- [ ] Adding function to delete status 
- [ ] Adding more logging statement into python functions
- An way to shows weekly activity: https://javascript.daypilot.org/

# Change Logo

2023/07/31
- when user go to local host, they will be redirected to either: 
      - > Login Page, if not log in , or
      - time_tracker page


- login blue heeler picture source
    - https://www.researchgate.net/figure/A-clear-faced-no-mask-blue-Australian-Cattle-Dog-aged-6-weeks_fig6_232737049

- user login/logout more smoothly now


2023/08/06
- The project filter is case insensitive now


2023/08/20
- Motivation:
    - The idea of success is personal and subjective.
    - We need a way to set our own goals and define our own success.
- Implemetation:
  - Daily goals are set and tracked by the time_tracker app.
  - The goal is just a simple checkbox that is created new every day.
    - Backend:
        - The goal is an object that contiains:
            - user
            - start_date
            - end_date: if does not exists -> repeat indefinitely
            - name: the name of the goal
            - description: the description of the goal
            - interval: the interval of the goal (measure in days. If the interval is set to 0, then this goal is not repeated)
        - Tracked goal is an object that is connected to the goal object
            - goal
            - date
            - is_completed: true if the goal is completed 
            - completed_time: the time when the goal was marked as completed
            - quality: just a scale from 1 -> 10 of what was the quality of their goal. e.g. If my goal was to read and I only have time to read for 5 mins, the quality would be 1. Otherwise, if I read for 1 hour with a really good book that helped me learned a lot the quality would be 10. This is something very subjective. Need a quick way to do this quality such as a simple scale or star system. 
    - Frontend:
        - Creating/editing goals:
            - User can set their goal
            - User can see their old goals and edit them by going to the individual goals info page (maybe a pop up?)
        - Checking the goals:
            - Just a simple interface that shows the goals that are due for today
            - The goals that are due in the future (This will exclude the goals that are already existed as a today's goal)
        - Overview/Statistic:
            - This view will be used by user as a way to reflect their success
            - It should shows at a weekly level how their daily goals are accomplished
            - Some statistic of when the goals are marked as completed -> to help them identify the pattern
            - Visually shows the quality of the goal accomplised


#  project code structure

- blue_heeler:
  - whole project management
    - urls.py -> main url 
    - settings.py -> set the apps and stuff

- common
  - shared code between different apps
  - models > base_models.py this is where all the models are based on
  - views contains common functions that can be used across different apps
    - process_ajax_request is used to process ajax requests

- static and staticfiles
  - A place where the statics files are stored and served t
  - MUST run `python manage.py collectstatic` if there is an update to the old files or new files are added
    - Once the `collectstatic` command is run -> the files in the `static` folder will be coppied over to `staticfiles`
  - The dependencies that we are using for this project are
    - bootstrap
    - quilljs
  - Under `static/js` we also have an `index.js` file that contains the common js code

https://docs.djangoproject.com/en/4.1/howto/static-files/https://docs.djangoproject.com/en/4.1/howto/static-files/