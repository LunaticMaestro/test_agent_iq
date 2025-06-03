import gradio as gr
import requests

API_URL = "http://localhost:8000/chat"

def chat_with_agentiq(message, history):
    # Convert Gradio history to ChatML-style format
    messages = []
    for user_msg, agent_msg in history:
        messages.append({"role": "User", "content": user_msg})
        messages.append({"role": "Assistant", "content": agent_msg})
    messages.append({"role": "User", "content": message})

    payload = {
        "messages": messages[-1:],  # no point of sending entire history, as the backend model does not support :(
        "model": "",  # Fill in your model name if required
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 1.0,
        "additionalProp1": {}
    }

    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"[Error: {str(e)}]"

    return reply

demo = gr.ChatInterface(fn=chat_with_agentiq, title="AgentIQ Chat")

demo.launch(server_name="0.0.0.0", server_port=7860)
