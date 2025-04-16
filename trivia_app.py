import gradio as gr
import requests
import html
import random

def fetch_trivia_question():
    response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
    data = response.json()
    if data["response_code"] == 0 and data["results"]:
        question = data["results"][0]
        # Unescape HTML entities
        cleaned_question = html.unescape(question["question"])
        correct_answer = html.unescape(question["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in question["incorrect_answers"]]
        
        # Combine and shuffle answers
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)
        
        return {
            "question": cleaned_question,
            "answers": all_answers,
            "correct_answer": correct_answer
        }
    return None

def check_answer(question, correct_answer, user_answer):
    if user_answer == correct_answer:
        return "Correct! 🎉"
    return f"Sorry, the correct answer was: {correct_answer}"

def get_new_question():
    trivia_data = fetch_trivia_question()
    if trivia_data:
        return (
            trivia_data["question"],
            gr.Radio.update(choices=trivia_data["answers"]),
            trivia_data["correct_answer"]
        )
    return "Error fetching question", gr.Radio.update(choices=[]), ""

def submit_answer(question, answer, correct_answer):
    if not answer:
        return "Please select an answer!"
    return check_answer(question, correct_answer, answer)

with gr.Blocks(title="Trivia Quiz") as app:
    gr.Markdown("# 🎯 Trivia Quiz")
    
    question = gr.Textbox(label="Question", interactive=False)
    correct_answer = gr.State("")
    answers = gr.Radio(label="Choose your answer", choices=[])
    
    with gr.Row():
        submit_btn = gr.Button("Submit Answer")
        next_btn = gr.Button("Next Question")
    
    result = gr.Markdown()
    
    # Set up event handlers
    next_btn.click(
        fn=get_new_question,
        outputs=[question, answers, correct_answer]
    )
    
    submit_btn.click(
        fn=submit_answer,
        inputs=[question, answers, correct_answer],
        outputs=result
    )
    
    # Load initial question
    app.load(
        fn=get_new_question,
        outputs=[question, answers, correct_answer]
    )

if __name__ == "__main__":
    app.launch() 