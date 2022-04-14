import PySimpleGUI as Sg

Sg.theme("Material1")
font_name = 'Courier'
font_size = 14


def add_task(value):
    task = value['task_name']
    if task != "":
        if values[0]:
            to_do_list.insert(0, task+" -Top")
        elif values[1]:
            to_do_list.insert(int(len(to_do_list)/2)+1, task+" -Normal")
        elif values[2]:
            to_do_list.insert(len(to_do_list), task+" -Low")

    window.FindElement('task_name').Update(value="")
    window.FindElement('to_do_list').Update(values=to_do_list)
    window.FindElement('add_save').Update('Add')


def edit_tasks(value):
    try:
        edit_val = value['to_do_list'][0]
        window.FindElement('task_name').Update(value=edit_val)
        todolist.remove(edit_val)
        window.FindElement('add_save').Update('Save')
    except:
        pass


def delete_tasks(value):
    try:
        delete_val = value['to_do_list'][0]
        todolist.remove(delete_val)
        window.FindElement('to_do_list').Update(values=to_do_list)
    except:
        pass

def delete_all():
    try:
        for i in range(len(to_do_list)):
            del to_do_list[i]
        window.FindElement("to_do_list").Update(values=to_do_list)
    except:
        pass

layout = [
    [
        Sg.Text("Enter the task", font=(font_name, font_size)),
        Sg.InputText("", font=(font_name, font_size), size=(20, 1), border_width=0, key="task_name"),
    ],

    [
        Sg.Text("Priority      ", font=(font_name, font_size)),
        Sg.Radio("Top", 1),
        Sg.Radio("Normal", 1, default=True),
        Sg.Radio("Low", 1)
    ],

    [
        Sg.Button("Add", font=(font_name, font_size), border_width=0, key="add_save"),
        Sg.Button("Edit", font=(font_name, font_size), border_width=0),
        Sg.Button("Delete", font=(font_name, font_size), border_width=0),
        Sg.Button("Delete All", font=(font_name, font_size), border_width=0)
    ],

    [
        Sg.Listbox(values=[], size=(40, 10), font=(font_name, font_size), key='to_do_list')
    ]

]

to_do_list = []

window = Sg.Window("To Do List", layout)

while True:
    event, values = window.Read()
    if event == 'add_save':
        add_task(values)
    elif event == 'Edit':
        edit_tasks(values)
    elif event == 'Delete':
        delete_tasks(values)
    elif event == "Delete All":
        delete_all()
    else:
        break

window.Close()