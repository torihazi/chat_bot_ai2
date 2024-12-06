# ai_server/app.py
from flask import Flask, request, Response
from openai import OpenAI
import os
import httpx

app = Flask(__name__)
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    http_client=httpx.Client()
)

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    
    def generate():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            
            for chunk in response:
                if chunk and hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
        except Exception as e:
            yield str(e)

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)