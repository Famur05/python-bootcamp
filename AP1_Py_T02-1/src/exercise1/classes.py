import random
import time
from typing import List

class Question:
    PHI = (1 + 5 ** 0.5) / 2  # Золотое сечение

    def __init__(self, text):
        self.text = text
        self.words = text.split()
        self.general_correct_answers = 0

    def get_student_answer(self, gender: str) -> str:
        """Симулирует ответ студента на вопрос."""
        probabilities = self._generate_probabilities(gender)
        return random.choices(self.words, weights=probabilities, k=1)[0]

    def get_examiner_answers(self, gender: str) -> list:
        """Симулирует ответы экзаменатора на вопрос с учетом его пола."""
        probabilities = self._generate_probabilities(gender)
        
        chosen_words = []
        remaining_indices = list(range(len(self.words)))

        while remaining_indices:
            word_index = random.choices(remaining_indices, weights=[probabilities[i] for i in remaining_indices], k=1)[0]
            chosen_words.append(self.words[word_index])
            remaining_indices.remove(word_index)

            if random.random() > 1 / 3:
                break
        
        return chosen_words

    def _generate_probabilities(self, gender: str) -> list:
        """Генерирует распределение вероятностей в зависимости от пола."""
        n = len(self.words)
        
        probabilities = []
        remaining = 1
        for i in range(n):
            if i == n - 1:
                prob = remaining
            else:
                prob = remaining / self.PHI
            probabilities.append(prob)
            remaining -= prob

        if gender != 'М':
            probabilities.reverse()
        return probabilities

class Student:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.status = "Очередь"
        self.exam_time = None

    def __str__(self):
        return f"{self.name} ({self.gender})"


class Examiner:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.total_students = 0
        self.failed_students = 0
        self.current_student: Student = None
        self.work_time = 0
        self.on_break = False

    def examine_student(self, student: Student, questions: List[Question]):
        """Симулирует сдачу экзамена студентом."""
        exam_time = random.uniform(len(self.name) - 1, len(self.name) + 1)
        time.sleep(exam_time)
        
        correct_answers = 0

        indices = list(range(len(questions)))
        
        selected_indices = random.sample(indices, 3)

        for index in selected_indices:
            question = questions[index]
            student_answer = question.get_student_answer(student.gender)
            examiner_answers = question.get_examiner_answers(self.gender)
            if student_answer in examiner_answers:
                correct_answers += 1
                question.general_correct_answers += 1

        self.work_time += exam_time
        student.exam_time = exam_time

        result = self.judge(correct_answers, 3 - correct_answers)
        self.total_students += 1
        if not result:
            self.failed_students += 1
        student.status = "Сдал" if result else "Провалил"

    def judge(self, correct: int, incorrect: int) -> bool:
        """Симулирует решение экзаменатора о сдаче экзамена."""
        mood = random.choices(["Плохое", "Нейтральное", "Хорошее"], weights=[1, 5, 2], k=1)[0]
        if mood == "Плохое":
            return False
        elif mood == "Хорошее":
            return True
        return correct > incorrect
