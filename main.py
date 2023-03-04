from flask import Flask, request
import os
import openai
import json

# flask --app main --debug run

# replace with your own openai key
with open('../openai.key') as f:
    openai.api_key = f.read().strip()

app = Flask(__name__)


BASE_PROMPT = """Create a response document with content that matches the following URL path: 
    `{{URL_PATH}}`

The first line is the Content-Type of the response.
The following lines is the returned data.
In case of a html response, add relative href links with to related topics.
{{OPTIONAL_DATA}}

Content-Type:
"""

@app.route("/", methods = ['POST', 'GET'])
@app.route("/<path:path>", methods = ['POST', 'GET'])
def catch_all(path=""):

    # is this a POST request with data?
    if request.form:
        prompt = BASE_PROMPT.replace("{{OPTIONAL_DATA}}", f"form data: {json.dumps(request.form)}")
    else:
        prompt = BASE_PROMPT.replace("{{OPTIONAL_DATA}}", f"")

    prompt = prompt.replace("{{URL_PATH}}", path)
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    
    ai_data = response.choices[0].text

    print(ai_data)

    content_type = ai_data.splitlines()[0]
    response_data = "\n".join(ai_data.splitlines()[1:])
    return response_data, 200, {'Content-Type': content_type}

