
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


# TODOS:

2023/07/31:
- [ ] Adding html location tag for each html page:
    - eg. <!-- time_tracker/templates/time_tracker/index.html-->
- [ ] Review time_tracker/views.py
  - [ ] Function comments
  - [ ] Other comments and notes
- [ ] Adding registration page
- [ ] Fix the display bug when "All" is selected as project
- [ ] UI improvement
    - [ ] Integrate Priority Display
    - [ ] When timeline in clicked, do something
    - [ ] Saved note styling 
- [ ] Adding function to delete status 


# Change Logo

2023/07/31
- when user go to local host, they will be redirected to either: 
      - > Login Page, if not log in , or
      - time_tracker page


- login blue heeler picture source
    - https://www.researchgate.net/figure/A-clear-faced-no-mask-blue-Australian-Cattle-Dog-aged-6-weeks_fig6_232737049

- user login/logout more smoothly now