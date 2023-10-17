from todo.models import TodoRepeat

import logging
logger = logging.getLogger(__name__)

def listDueRepeatableTodos():
    # get all the repeatable todos
    todo_repeats = TodoRepeat.objects.all()

    # loop through the repeatable todos
    is_due_repeats = []
    for todo_repeat in todo_repeats:
        # If the todo is not done, skip it

        if todo_repeat.todo is None:
            # todo_repeat must have a todo -> remove it
            todo_repeat.delete()

        if not todo_repeat.todo.is_done:
            logger.debug(f"Todo {todo_repeat.todo} is not done, skipping")
            continue

        # check if the todo is due
        if todo_repeat.is_due():
            # if it is, reset the todo
            logger.debug(f"Todo {todo_repeat.todo} is due, adding to list")
            is_due_repeats.append(todo_repeat)
    
    return is_due_repeats


def resetTodos(todo_repeats):
    # reset the todos
    for todo_repeat in todo_repeats:
        todo_repeat.reset()


def checkRepeatableTodos(check_only=False):
    todo_repeats = listDueRepeatableTodos()

    if check_only:
        return 
    
    resetTodos(todo_repeats)
            

