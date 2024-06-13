import json
import difflib


async def answer_for_question(question: str) -> str:
    with open('assets/questions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    questions_and_answers = data["questions_and_answers"]
    all_questions = [qa["question"] for qa in questions_and_answers]
    keywords_list = [qa["keywords"] for qa in questions_and_answers]
    
    # Поиск по ключевым словам
    keywords_matches = []
    for keywords in keywords_list:
        for keyword in keywords:
            if keyword in question.lower():
                keywords_matches.append(keyword)
    
    # Поиск по формулировке вопроса
    closest_matches = difflib.get_close_matches(question, all_questions, n=2, cutoff=0.6)
    if closest_matches:
        closest_question = closest_matches[0]
        for qa in questions_and_answers:
            if qa["question"] == closest_question:
                return qa["answer"]
    
    if keywords_matches:
        for qa in questions_and_answers:
            if any(keyword in qa["keywords"] for keyword in keywords_matches):
                return qa["answer"]
    
    return "Извините, я не нашел ответа на ваш вопрос."
