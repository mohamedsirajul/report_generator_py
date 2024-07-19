from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from requests.exceptions import RequestException
# import pyttsx3

app = Flask(__name__)
CORS(app)

# Set your OpenAI GPT-3 API key (Replace this with a secure way to get your API key)
api_key = "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"
openai.api_key = api_key

# Initialize the text-to-speech engine
# engine = pyttsx3.init()

def generate_prompt_response(prompt):
    try:
        # Check for a specific prompt and provide a custom response
        if prompt.lower() == "req":
            return "Sure, how can I help you with your request?"

        # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Updated from "engine" to "model"
            messages=[
                {'role': 'assistant', 'content': 'hi'},
                {'role': 'user', 'content': 'my name is siraj'},
                {'role': 'assistant', 'content': 'ok'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=150
        )

        print(response)
        # Extract the generated text from the response
        generated_text = response['choices'][0]['message']['content']
        print(generated_text)
        
         # Convert the generated text to speech
        # engine.say(generated_text)
        # engine.runAndWait()
        return generated_text

    except openai.error.OpenAIError as e:
        app.logger.error(f"OpenAI API Error: {e}")
        return None
    except RequestException as e:
        app.logger.error(f"Request Exception: {e}")
        return None
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return None

@app.route('/api/generate-response', methods=['POST'])
def api_generate_response():
    try:
        data = request.get_json() 
        prompt = data.get('prompt', '')

        if not prompt:
            return jsonify({'error': 'Invalid prompt'}), 400

        generated_response = generate_prompt_response(prompt)

        
        if generated_response is not None:
            return jsonify({'response': generated_response})
        else:
            return jsonify({'error': 'Failed to generate a response'}), 500

    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=5000)
