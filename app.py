from flask import Flask, request, jsonify, render_template, send_from_directory
import google.generativeai as genai
import textwrap
import os

app = Flask(__name__, template_folder='.', static_folder='.')

# Initialize Google Generative AI
GOOGLE_API_KEY = 'YOUR API HERE'
genai.configure(api_key=GOOGLE_API_KEY)

# Define a function to convert the AI-generated content to Markdown format
def to_markdown(parts):
    formatted_parts = []
    for part in parts:
        text = part.text
        # Replace markdown formatting in the text
        text = text.replace('-', ' *')  # Example for bullets, adjust if needed
        text = text.replace('* ', '*')  # Fix extra spaces around asterisks
        text = text.replace('*', '**')
        text = text.replace('**', '')
        text = text.replace('***', ' ')
        text = text.replace('*****', '\n')  # Use bold formatting for emphasis
        formatted_parts.append(text)
    return textwrap.indent('\n'.join(formatted_parts), '> ', predicate=lambda _: True)

@app.route('/')
def index():
    return render_template('templates/index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    content = to_markdown(response.parts)
    return jsonify({'content': content})

# Ensure that CSS and JS files are correctly served
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
