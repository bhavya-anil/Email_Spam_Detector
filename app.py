from flask import Flask, request, jsonify, render_template
from groq import Groq
import json

app = Flask(__name__)
client = Groq()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    email_content = data.get("email", "")

    if not email_content.strip():
        return jsonify({"error": "Email content is empty"}), 400

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an email spam detection assistant.
Think step-by-step before deciding.

If spam → call function with is_spam="Yes"
If not spam → call function with is_spam="No" and generate reply.
"""
                },
                {
                    "role": "user",
                    "content": email_content
                }
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "spam_detector",
                        "description": "Check whether mail is spam or not",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "is_spam": {
                                    "type": "string",
                                    "enum": ["Yes", "No"]
                                },
                                "reply": {
                                    "type": "string"
                                }
                            },
                            "required": ["is_spam"]
                        }
                    }
                }
            ],
            reasoning_effort="low",
            stream=True
        )

        reasoning_text = ""
        tool_arguments = ""

        for chunk in completion:
            delta = chunk.choices[0].delta

            if hasattr(delta, "reasoning") and delta.reasoning:
                reasoning_text += delta.reasoning

            if delta.tool_calls:
                if delta.tool_calls[0].function.arguments:
                    tool_arguments += delta.tool_calls[0].function.arguments

        result = {"reasoning": reasoning_text}

        if tool_arguments:
            arguments = json.loads(tool_arguments)
            result["is_spam"] = arguments.get("is_spam", "Unknown")
            result["reply"] = arguments.get("reply", "")
        else:
            result["is_spam"] = "Unknown"
            result["reply"] = ""

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
