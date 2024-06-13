import json
import re
from fuzzywuzzy import fuzz, process


def preprocess_text(text: str) -> str:
    """
    Функция для предварительной обработки текста: приведение к нижнему регистру и удаление знаков препинания.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Удаление знаков препинания
    return text


def find_best_match(question: str, all_questions: list) -> str:
    """
    Функция для нахождения наиболее похожего вопроса с использованием fuzzywuzzy.
    """
    preprocessed_question = preprocess_text(question)
    preprocessed_questions = [preprocess_text(q) for q in all_questions]

    closest_matches = process.extract(
        preprocessed_question, preprocessed_questions, limit=1, scorer=fuzz.token_sort_ratio
    )

    if closest_matches:
        best_match_index = preprocessed_questions.index(closest_matches[0][0])
        return all_questions[best_match_index]


def keyword_match(question: str, keywords: list) -> bool:
    """
    Функция для проверки наличия ключевых слов в вопросе с использованием fuzzywuzzy.
    """
    preprocessed_question = preprocess_text(question)
    for keyword in keywords:
        preprocessed_keyword = preprocess_text(keyword)
        # Порог для частичного совпадения
        if fuzz.partial_ratio(preprocessed_question, preprocessed_keyword) > 80:
            return True
    return False


async def answer_for_question(question: str) -> str:
    try:
        with open('assets/questions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        questions_and_answers = data["questions_and_answers"]
        all_questions = [qa["question"] for qa in questions_and_answers]

        # Поиск по ключевым словам с частичным совпадением
        for qa in questions_and_answers:
            if keyword_match(question, qa.get("keywords", [])):
                return qa["question"], qa["answer"]

        # Поиск по формулировке вопроса
        closest_question = find_best_match(question, all_questions)
        if closest_question:
            for qa in questions_and_answers:
                if qa["question"] == closest_question:
                    return qa["question"], qa["answer"]

        return None, "Извините, я не нашёл ответа на ваш вопрос 😔."
    except Exception as _ex:
        print(_ex)
        return None, "Произошла ошибка при обработке вашего вопроса 🥺."
