
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return False, "No current question."

    try:
        current_question = PYTHON_QUESTION_LIST[current_question_id]
    except Exception as ex:
        return False, "Invalid question ID."

    correct_answer = current_question['answer']
    if answer not in current_question['options']:
        return False, "Invalid answer."

    if 'answers' not in session:
        session['answers'] = []
    
    session['answers'].append({
        'question_id': current_question_id,
        'user_answer': answer,
        'correct_answer': correct_answer,
        'is_correct': answer == correct_answer
    })
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get('answers', [])
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = sum(1 for answer in answers if answer['is_correct'])

    score = (correct_answers / total_questions) * 100
    return "dummy result"
