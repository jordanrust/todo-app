from modules import functions
import PySimpleGUI as sg
import time
import os

if not os.path.exists("todos.txt"):
    with open("todos.txt", "w") as file:
        pass

sg.theme("LightGreen3")

clock = sg.Text('', key="clock")
label = sg.Text("Type in a to-do")
input_box = sg.InputText(tooltip="Enter todo", key="todo", size=25)
add_button = sg.Button("Add", size=22)
list_box = sg.Listbox(values=functions.get_todos(), key='todos',
                      enable_events=True, size=(25, 8))
edit_button = sg.Button("Edit", size=22)
complete_button = sg.Button("Complete", size=22)
exit_button = sg.Button("Exit", size=22)

window = sg.Window('My To-Do App',
                   layout=[[clock],
                           [label],
                           [sg.Column([[input_box], [list_box]]),
                           sg.Column([[add_button], [edit_button], [complete_button], [exit_button]])]],
                   font=('Helvetica', 10),
                   size=(320, 250))
while True:
    event, values = window.read(timeout=200)
    window["clock"].update(value=time.strftime("%x   %X"))
    match event:
        case "Add":
            todos = functions.get_todos()
            new_todo = values['todo'] + "\n"
            todos.append(new_todo)
            functions.write_todos(todos)
            window['todos'].update(values=todos)

        case "Edit":
            try:
                todo_to_edit = values['todos'][0]
                new_todo = values['todo'] + "\n"

                todos = functions.get_todos()
                index = todos.index(todo_to_edit)
                todos[index] = new_todo
                functions.write_todos(todos)
                window['todos'].update(values=todos)
            except IndexError:
                sg.popup("Please select an item first", font=('Helvetica', 15))

        case "Complete":
            todo_to_complete = values['todos'][0]
            todos = functions.get_todos()
            todos.remove(todo_to_complete)
            functions.write_todos(todos)
            window['todos'].update(values=todos)
            window['todo'].update(value='')

        case "Exit":
            break

        case "todos":
            window['todo'].update(value=values['todos'][0])

        case sg.WIN_CLOSED:
            break


window.close()
