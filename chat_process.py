import subprocess
import sys


def get_char(process):
    character = process.stdout.read1(1)
    print(
        character.decode("utf-8"),
        end="",
        flush=True,  # Unbuffered print
    )
    return character.decode("utf-8")

def search_for_output(strings, process):
    buffer = ""
    while not any(string in buffer for string in strings):
        buffer = buffer + get_char(process)

    return buffer

# start_commands = ['./ARM64/Debug/ChatApp.exe', '--genie-config', './genie_bundle/genie_config.json', '--base-dir', './genie_bundle/']

start_commands = '.\\ARM64\\Debug\\ChatApp.exe --genie-config .\\genie_bundle\\genie_config.json --base-dir .\\genie_bundle\\'

process = subprocess.Popen(start_commands, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, text=True)


# while True:
#     buffer = ""
#     while True:
#         character = process.stdout.read1(1).decode("utf-8")
#         print(
#             character,
#             end="",
#             flush=True,  # Unbuffered print
#         )
#         buffer += character
#         print(buffer, flush=True)
#         if "User: " in buffer:
#             buffer = ""
#             prompt = input()
#             process.stdin.write(f"{prompt}\n".encode())
#             process.stdin.flush()
#             continue
#         if not character:
#             break

#     buffer = ""
#     process.kill()

buffer = ""
while True:
    c = process.stdout.read(1)
    print(c, flush=True)
    buffer += c
    print(buffer, flush=True)
    if "User: " in buffer:
        buffer = ""
        prompt = input()
        print('flushing...', flush=True)
        process.stdin.write(f"{prompt}\n")
        process.stdin.flush()
        continue

print('broken')

# while True:
#     buffer = ""
#     exit_flag = False
#     for c in iter(lambda: process.stdout.read1(1), b""):
#         character = c.decode("utf-8")
#         print(
#             c.decode("utf-8"),
#             end="",
#             flush=True,
#         )
#         buffer += character
#         if "User: " in buffer:
#             # buffer += process.communicate()[0]
#             print('printing total buffer')
#             print(buffer)
#             print("enter prompt:")
#             prompt = input()
#             process.stdin.write(f"{prompt}\n".encode())
#             process.stdin.flush()
#             buffer = ""


# with subprocess.Popen(start_commands, stdout=subprocess.PIPE, stdin=subprocess.PIPE) as process:
#     buffer = ""
#     while True:
#         character = process.stdout.read1().decode("utf-8")
#         buffer += character
#         # print(
#         #     character,
#         #     end="",
#         #     flush=True,  # Unbuffered print
#         # )
#         print(buffer, flush=True)
#         if "User: " in buffer:
#             buffer = ""
#             prompt = input()
#             process.stdin.write(f"{prompt}\n".encode())
#             process.stdin.flush()
#         if not character:
#             break

#     buffer = ""
#     process.kill()




# with subprocess.Popen(start_commands, stdout=subprocess.PIPE, stdin=subprocess.PIPE) as process:
#     buffer = ""
#     while True:
#         character = process.stdout.read1().decode("utf-8")
#         buffer += character
#         print(
#             character,
#             end="",
#             flush=True,  # Unbuffered print
#         )
#         # print(buffer, flush=True)
#         if "User:" in buffer:
#             print('breaking!')
#             break
#         if not character:
#             break
#     buffer = ""
#     process.stdin.write(f"hello! how are you?\n".encode())
#     process.stdin.flush()
#     # process.stdin.flush()
#     while True:
#         character = process.stdout.read1().decode("utf-8")
#         buffer += character
#         print(
#             character,
#             end="",
#             flush=True,  # Unbuffered print
#         )
#         if "User:" in buffer:
#             print('breaking again! announcing exit prompt')
#             break
#         if not character:
#             break
#     buffer = ""
#     process.stdin.write("exit\n".encode())
#     process.stdin.flush()
#     while True:
#         character = process.stdout.read1().decode("utf-8")
#         buffer += character
#         print(
#             character,
#             end="",
#             flush=True,  # Unbuffered print
#         )
#         if "request." in buffer:
#             break
#         if not character:
#             break

#     buffer = ""
#     process.kill()
#     # search_for_output(["request."], process)