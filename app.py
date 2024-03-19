from flask import Flask, request, jsonify
import google.generativeai as genai
import dotenv
import os
from dotenv import load_dotenv
load_dotenv() 

model = genai.GenerativeModel('gemini-pro')

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

def truncate_and_complete_response(response, max_length):
    if len(response) > max_length:
        # Truncate the response to the maximum length
        truncated_response = response[:max_length]
        # Find the last sentence boundary in the truncated response
        last_sentence_boundary = truncated_response.rfind('.')
        if last_sentence_boundary != -1:
            # If a sentence boundary is found, truncate the response to that point
            truncated_response = truncated_response[:last_sentence_boundary + 1]
        return truncated_response
    else:
        return response

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.json['user_input']
    response = model.generate_content(user_input)
    # Truncate and ensure completeness of response
    truncated_response = truncate_and_complete_response(response.text, 200)
    
    if truncated_response:
        return jsonify({"response": truncated_response})
    else:
        return "Sorry, but I think Gemini didn't want to answer that!"

if __name__ == '__main__':
    app.run(debug=True)