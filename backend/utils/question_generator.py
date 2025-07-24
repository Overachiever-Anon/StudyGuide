import os
import openai
from ..services.anthropic_client import get_anthropic_client

def generate_questions_from_text(text, chapter_id, exam_id):
    """Generates questions from a given text using an AI model."""
    from ..models import db, Question, Chapter, Exam # Defer import

    try:
        client = get_anthropic_client()
        if not client:
            raise ValueError("Anthropic client not available. Check API key.")

        # This is a simplified example. A real implementation would involve
        # more sophisticated prompting and parsing.
        prompt = f"""Based on the following text, generate 5 multiple-choice questions with 4 options each. Mark the correct answer with an asterisk (*).

Text: {text}

Format your response as a list of questions, like this:
1. What is the capital of France?
- London
- Berlin
- *Paris
- Madrid

2. What is 2+2?
- 3
- *4
- 5
- 6
"""

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        generated_text = message.content[0].text
        questions_data = parse_generated_questions(generated_text)

        for q_data in questions_data:
            question = Question(
                text=q_data['text'],
                options=q_data['options'],
                correct_answer=q_data['correct_answer'],
                chapter_id=chapter_id,
                exam_id=exam_id
            )
            db.session.add(question)
        
        db.session.commit()
        return questions_data

    except Exception as e:
        # In a real app, you'd want more robust error handling and logging
        print(f"Error generating questions: {e}")
        return []

def parse_generated_questions(text):
    """Parses the AI-generated text to extract questions and answers."""
    questions = []
    # This is a very basic parser. A real implementation would be more robust.
    # It assumes questions are numbered and options start with '-'.
    current_question = None
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue

        if line[0].isdigit() and '.' in line:
            if current_question:
                questions.append(current_question)
            current_question = {'text': line.split('.', 1)[1].strip(), 'options': [], 'correct_answer': ''}
        elif line.startswith('-') and current_question:
            option_text = line[1:].strip()
            if option_text.startswith('*'):
                option_text = option_text[1:].strip()
                current_question['correct_answer'] = option_text
            current_question['options'].append(option_text)

    if current_question:
        questions.append(current_question)

    return questions
