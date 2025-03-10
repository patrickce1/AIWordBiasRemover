from openai import OpenAI

client = OpenAI(api_key="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")
import time
from flask import Flask, request, jsonify
import time
import sys

app = Flask(__name__)

assistant_id = "asst_hi8RuTAIkDea4MRzcQ5SE7zl"

def create_thread(ass_id,prompt):

    #create a thread
    thread = openai.beta.threads.create()
    my_thread_id = thread.id
    #create a message
    message = openai.beta.threads.messages.create(
        thread_id=my_thread_id,
        role="user",
        content=prompt
    )
    #run
    run = openai.beta.threads.runs.create(
        thread_id=my_thread_id,
        assistant_id=ass_id,
    ) 
    return run.id, thread.id
def check_status(run_id,thread_id):
    run = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status




@app.route('/CryptoAgent', methods=['POST'])
def return_response():
    data = request.json
    assistant_id = "asst_hi8RuTAIkDea4MRzcQ5SE7zl"
    prompt = data.get('prompt')

    if not all([assistant_id, prompt]):
        return jsonify({'error': 'Missing data'}), 400

    my_run_id, my_thread_id = create_thread(assistant_id, prompt)
    status = check_status(my_run_id, my_thread_id)

    while status != "completed":
        status = check_status(my_run_id, my_thread_id)
        time.sleep(2)

    response = client.chat.completions.retrieve(id=my_run_id)

    if response.choices:
        return jsonify({'response': response.choices[0].message.content}), 200
    else:
        return jsonify({'error': 'No response found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
