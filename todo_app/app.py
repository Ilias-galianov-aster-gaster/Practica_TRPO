from flask import Flask, render_template, request, redirect
import json
import os
from datetime import date


app = Flask(__name__)
FILE_NAME = 'tasks.json'


def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_tasks(tasks_list):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return render_template('index.html', tasks=load_tasks())


@app.route('/add', methods=['POST'])
def add_task():
    new_task = request.form.get('task')
    priority = request.form.get('priority', 'средний') # По умолчанию средний приоритет


    if new_task:
        today = date.today().strftime('%Y-%m-%d')
        tasks = load_tasks()
        tasks.append({
            'text': new_task,
            'date': today,
            'done': False,
            'priority': priority})

        save_tasks(tasks)
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()

    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect('/')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404

    task = tasks[task_id]

    if request.method == 'POST':
        new_text = request.form.get('task', '').strip()
        new_priority = request.form.get('priority', 'средний')
        old_text = task['text']
        old_priority = task.get('priority', 'средний')

        if new_text == '':
            return render_template('edit.html', task=task, message="Текст не может быть пустым!")

        if new_text == old_text and new_priority == old_priority:
            return render_template('edit.html', task=task, message="Ничего не изменено")

        task['text'] = new_text
        task['priority'] = new_priority
        save_tasks(tasks)
        return redirect('/')
    else:
        return render_template('edit.html', task=task)


@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        save_tasks(tasks)
    return redirect('/')


@app.route('/clear_all')
def clear_all():
    save_tasks([])
    return redirect('/')


# Самостоятельные задания
@app.route('/active')
def active_tasks():
    tasks = [t for t in load_tasks() if not t.get('done')]
    return render_template('index.html', tasks=tasks)


@app.route('/completed')
def completed_tasks():
    tasks = [t for t in load_tasks() if t.get('done')]
    return render_template('index.html', tasks=tasks)


@app.route('/complete_all')
def complete_all():
    tasks = load_tasks()
    for task in tasks:
        task['done'] = True
    save_tasks(tasks)
    return redirect('/')


@app.route('/uncomplete_all')
def uncomplete_all():
    tasks = load_tasks()
    for task in tasks:
        task['done'] = False
    save_tasks(tasks)
    return redirect('/')


@app.route('/by_priority')
def by_priority():
    tasks = load_tasks()
    priority_order = {'высокий': 3, 'средний': 2, 'низкий': 1}
    sorted_tasks = sorted(
        tasks,
        key=lambda task: priority_order.get(task.get('priority', 'средний')),
        reverse=True
    )
    return render_template('index.html', tasks=sorted_tasks)

    
@app.route('/by_priority_active')
def by_priority_active():
    priority_order = {'высокий': 3, 'средний': 2, 'низкий': 1}
    
    # Сначала загружаем задачи!
    tasks_list = load_tasks()
    
    # Фильтруем только активные
    active_tasks = [task for task in tasks_list if not task.get('done')]
    
    # Сортируем
    sorted_tasks = sorted(
        active_tasks,
        key=lambda task: priority_order.get(task.get('priority'), 'средний'),
        reverse=True
    )
    return render_template('index.html', tasks=sorted_tasks)


if __name__ == '__main__':
    app.run(debug=True)