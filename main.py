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


def stream_response_genie(message, history):
    formatted_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\\n\\n{message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    commands = ['cmd', '/c', 'cd', './genie_bundle/', '&&', 'genie-t2t-run.exe', '-c', 'genie_config.json', '-p', formatted_prompt]
    
    genie_version_text = "Using libGenie.so version 1.1.0"
    formatted_prompt_text = f'[PROMPT]: {formatted_prompt}'
    begin_text = "[BEGIN]:"
    end_text = "[END]"
    metrics_text = "[KPIS]"

    res = ""

    with subprocess.Popen(commands, stdout=subprocess.PIPE) as p:
        flags = {
            'version': True,
            'prompt': True,
            'begin': True,
            'end': True,
            'metrics': True,
        }
        while True:
            # Use read1() instead of read() or Popen.communicate() as both blocks until EOF
            # https://docs.python.org/3/library/io.html#io.BufferedIOBase.read1
            text = p.stdout.read1().decode("utf-8")
            res += text
            # check for version text prefix, we dont need it in response
            if flags['version']:
                if genie_version_text in res:
                    res = res.replace(genie_version_text, '')
                    res = res.strip()
                    flags['version'] = False

            # check for prompt text prefix, we dont need it in response
            if flags['prompt']:
                if formatted_prompt_text in res:
                    res = res.replace(formatted_prompt_text, '')
                    res = res.strip()
                    flags['prompt'] = False

            # check for begin text prefix, we dont need it in response
            if flags['begin']:
                if begin_text in res:
                    res = res.replace(begin_text, '')
                    res = res.strip()
                    flags['begin'] = False
            
            # check for end text prefix, we dont need it in response
            if flags['end']:
                if end_text in res:
                    res = res.replace(end_text, '')
                    res = res.strip()
                    flags['end'] = False

            # check for metrics text prefix, we dont need it in response
            if flags['metrics']:
                if metrics_text in res:
                    res = res[:res.index(metrics_text)]
                    # res = res.replace(metrics_text, '')
                    # res = res.strip()
                    flags['metrics'] = False
            yield res
            if not text:
                print(res)
                break
        return

with gr.Blocks(css=css, fill_height=True) as demo:
    gr.Markdown(
    """
    <h1 style="text-align: center;">NPU Chatbot 💻📑✨</h3>
    """)
    with gr.Row(equal_height=False, elem_classes=["app-interface"]):
        with gr.Column(scale=4, elem_classes=["chat-interface"]):
            test = gr.ChatInterface(fn=stream_response_genie)
            

demo.launch(share=False)