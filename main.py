#main.py
from flask import Flask, request, render_template

def processCommand(command):
    output = ""
    cmdsplits = command.split()
    if command == "/?" or command == "help":
        output = """
echo [text]-- writes [text] to the terminal
        """
    elif cmdsplits[0] == "echo":
        if cmdsplits[1]:
            output = cmdsplits[1]
    else:
        output = "Invalid command. Type 'help' or '/?' for help."
    return output

app = Flask(__name__)
history = []
@app.route('/')
def index():
    global history
    print(history)
    return render_template('index.html', history = history)
@app.route('/', methods=['POST'])
def cmdhistory():
    global history
    command = "".join(request.form['inp'])
    processedCommand = processCommand(command)
    history.append("> " + command)
    history.append(processedCommand)
    return render_template('index.html', history = history)
if __name__ == '__main__':
    app.run()
