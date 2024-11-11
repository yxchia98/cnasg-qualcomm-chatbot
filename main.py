import subprocess
import sys

# prompt = "Hello! how are you?"
# formatted_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\\n\\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
# commands = ['cmd', '/c', 'cd', './genie_bundle/', '&&', 'genie-t2t-run.exe', '-c', 'genie_config.json', '-p', formatted_prompt]

# res = ""

# with subprocess.Popen(commands, stdout=subprocess.PIPE) as p:
#     while True:
#         # Use read1() instead of read() or Popen.communicate() as both blocks until EOF
#         # https://docs.python.org/3/library/io.html#io.BufferedIOBase.read1
#         text = p.stdout.read1().decode("utf-8")
#         res += text
#         print("----------NEXT OUTPUT----------")
#         print(res, flush=True)
#         if not text:
#             break



import gradio as gr

css = """
.app-interface {
    height:80vh;
}7
.chat-interface {
    height: 75vh;
}
.file-interface {
    height: 40vh;
}
"""

def stream_response_genie(message, history):
    formatted_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\\n\\n{message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    commands = ['cmd', '/c', 'cd', './genie_bundle/', '&&', 'genie-t2t-run.exe', '-c', 'genie_config.json', '-p', formatted_prompt]
    res = ""
    with subprocess.Popen(commands, stdout=subprocess.PIPE) as p:
        while True:
            # Use read1() instead of read() or Popen.communicate() as both blocks until EOF
            # https://docs.python.org/3/library/io.html#io.BufferedIOBase.read1
            text = p.stdout.read1().decode("utf-8")
            res += text
            print("----------NEXT OUTPUT----------")
            print(res, flush=True)
            yield res
            if not text:
                break
        return

with gr.Blocks(css=css) as demo:
    gr.Markdown(
    """
    <h1 style="text-align: center;">Hosted NIM Chatbot 💻📑✨</h3>
    """)
    with gr.Row(equal_height=False, elem_classes=["app-interface"]):
        with gr.Column(scale=4, elem_classes=["chat-interface"]):
            test = gr.ChatInterface(fn=stream_response_genie)
            

demo.launch(server_name="0.0.0.0", ssl_verify=False, inline=False)