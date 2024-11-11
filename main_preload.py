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
    height: 90vh;
}
.chat-interface {
    height: 80vh;
}
.file-interface {
    height: 40vh;
}
"""

start_commands = '.\\ARM64\\Debug\\ChatApp.exe --genie-config .\\genie_bundle\\genie_config.json --base-dir .\\genie_bundle\\'

process = subprocess.Popen(start_commands, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

def stream_response_genie(message, history):
    flags = {
        'assistant': True,
        'user': True,
        'generating': True
    }
    buffer = ""
    process.stdin.write(f"{message}\n".encode())
    process.stdin.flush()
    while True:
        c = process.stdout.read1().decode(errors='ignore')
        # print(c, flush=True)
        sys.stdout.flush()
        buffer += c
        # print(buffer, flush=True)
        sys.stdout.flush()
        if flags['assistant']:
            if "Assistant:" in buffer:
                # print('flushing...', flush=True)
                sys.stdout.flush()
                buffer = buffer.replace("Assistant:", '')
                buffer = buffer.strip()
                flags['assistant'] = False
        if flags['user']:
            if "User:" in buffer:
                # print('flushing...', flush=True)
                sys.stdout.flush()
                buffer = buffer.replace("User:", '')
                buffer = buffer.strip()
                flags['user'] = False
                flags['generating'] = False

        if not flags['generating']:
            sys.stdout.flush()
            yield buffer
            break
        if buffer:
            yield buffer

    return

buffer = ""

while True:
    c = process.stdout.read1().decode(errors='ignore')
    print(c, flush=True)
    sys.stdout.flush()
    buffer += c
    # print(buffer, flush=True)
    sys.stdout.flush()
    if "User: " in buffer:
        # print('flushing...', flush=True)
        sys.stdout.flush()
        break

with gr.Blocks(css=css, fill_height=True) as demo:
    gr.Markdown(
    """
    <h1 style="text-align: center;">NPU Chatbot 💻📑✨</h3>
    """)
    with gr.Row(equal_height=False, elem_classes=["app-interface"]):
        with gr.Column(scale=4, elem_classes=["chat-interface"]):
            test = gr.ChatInterface(fn=stream_response_genie)
            

demo.launch(share=False)