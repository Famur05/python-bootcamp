import os
import random
import time
from multiprocessing import Process, Queue
from prettytable import PrettyTable
from classes import *
from typing import List

def load_data():
    """Загружает данные из файлов."""
    with open('examiners.txt', 'r', encoding='utf-8') as f:
        examiners = [line.strip().split() for line in f.readlines()]

    with open('students.txt', 'r', encoding='utf-8') as f:
        students = [line.strip().split() for line in f.readlines()]

    with open('questions.txt', 'r', encoding='utf-8') as f:
        questions = [line.strip() for line in f.readlines()]

    return examiners, students, questions

def examiner_process(examiner: Examiner, students_queue: Queue, results_queue: Queue, questions: List[Question]) -> None:
    """Обрабатывает студентов в очереди для конкретного экзаменатора."""
    start_time = time.time()

    while not students_queue.empty():
        try:
            elapsed_time = time.time() - start_time
            if elapsed_time > 30:
                print(f"{examiner.name} отправляется на обед...")
                time.sleep(random.uniform(12, 18))
                start_time = time.time()

            student = students_queue.get()
            examiner.current_student = student
            results_queue.put((examiner, student, questions))
        except Exception:
            continue
        
        examiner.examine_student(student, questions)
        results_queue.put((examiner, student, questions))
        examiner.current_student = None

def print_status(students, examiners, elapsed_time):
    """Печатает текущий статус студентов и экзаменаторов."""
    os.system('cls' if os.name == 'nt' else 'clear')

    student_table = PrettyTable(["Студент", "Статус"])

    for student in sorted(students, key=lambda s: ("Очередь", "Сдал", "Провалил").index(s.status)):
        student_table.add_row([student.name, student.status])

    print(student_table)

    examiner_table = PrettyTable(["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы"])
    for examiner in examiners:
        examiner_table.add_row([
            examiner.name,
            examiner.current_student.name if examiner.current_student else "-",
            examiner.total_students,
            examiner.failed_students,
            f"{examiner.work_time:.2f}"
        ])
    print(examiner_table)

    remaining_in_queue = sum(1 for student in students if student.status == "Очередь")
    print(f"\nОсталось в очереди: {remaining_in_queue} из {len(students)}")

    print(f"Время с момента начала экзамена: {elapsed_time:.2f} секунд")

def print_final_status(students, examiners, elapsed_time, questions):
    """Печатает итоговый статус после завершения экзамена."""
    student_table = PrettyTable(["Студент", "Статус"])
    for student in sorted(students, key=lambda s: ("Сдал", "Провалил").index(s.status)):
        student_table.add_row([student.name, student.status])
    print(student_table)

    examiner_table = PrettyTable(["Экзаменатор", "Всего студентов", "Завалил", "Время работы"])
    for examiner in examiners:
        examiner_table.add_row([
            examiner.name,
            examiner.total_students,
            examiner.failed_students,
            f"{examiner.work_time:.2f}"
        ])
    print(examiner_table)

    print(f"\nВремя с момента начала экзамена и до момента его завершения: {elapsed_time:.2f}")

    best_students = [student.name for student in students if student.status == "Сдал" and student.exam_time == min([s.exam_time for s in students if s.status == "Сдал"])]
    print(f"Имена лучших студентов: {', '.join(best_students)}")

    best_examiners = [examiner.name for examiner in examiners if examiner.failed_students / examiner.total_students == min([e.failed_students / e.total_students for e in examiners])]
    print(f"Имена лучших экзаменаторов: {', '.join(best_examiners)}")

    worst_students = [student.name for student in students if student.status == "Провалил" and student.exam_time == min([s.exam_time for s in students if s.status == "Провалил"])]
    print(f"Имена студентов, которых после экзамена отчислят: {', '.join(worst_students)}")

    best_questions = [question.text for question in questions if question.general_correct_answers == max([q.general_correct_answers for q in questions])]
    print(f"Лучшие вопросы: {', '.join(best_questions)}")

    pass_rate = len([s for s in students if s.status == "Сдал"]) / len(students) * 100
    if pass_rate > 85:
        print("Вывод: экзамен удался")
    else:
        print("Вывод: экзамен не удался")

def main():
    """Главная функция."""
    examiners_data, students_data, questions_data = load_data()
    examiners = [Examiner(name, gender) for name, gender in examiners_data]
    students = [Student(name, gender) for name, gender in students_data]
    questions = [Question(text) for text in questions_data]

    students_queue = Queue()
    for student in students:
        students_queue.put(student)

    results_queue = Queue()

    processes = []
    for examiner in examiners:
        p = Process(target=examiner_process, args=(examiner, students_queue, results_queue, questions))
        p.start()
        processes.append(p)

    start_time = time.time()

    elapsed_time = None
    while any(p.is_alive() for p in processes) or not results_queue.empty():
        elapsed_time = time.time() - start_time

        while not results_queue.empty():
            updated_examiner, updated_student, updated_questions = results_queue.get()
            
            for i, e in enumerate(students):
                if e.name == updated_student.name:
                    students[i] = updated_student
            
            for i, e in enumerate(examiners):
                if e.name == updated_examiner.name:
                    examiners[i] = updated_examiner

            questions = updated_questions

        print_status(students, examiners, elapsed_time)
        # time.sleep(1)

    for p in processes:
        p.join()

    print_final_status(students, examiners, elapsed_time, questions)

if __name__ == "__main__":
    main()
