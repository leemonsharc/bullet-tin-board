# PITCH LINE:

# What we'll be making is a murder mystery in a simulated proto-internet system where you have to figure out
# who killed your favorite server. On a calm day, in 1981, you get a message asking who killed
# it. Then, you go down a rabbit hole of server-hopping to solve the great mystery, and get revenge.
# What will happen? Will you ever get the server back?

from flask import Flask, request, render_template, jsonify

connected = 0

#STUFF FOR THE FILE EXPLORER
FILE_SYSTEM = {
    'name': 'C:\\',
    'type': 'folder',
    'children': [
        {
            'name': 'SYSTEM',
            'type': 'folder',
            'children': [
                {'name': 'CONFIG.SYS', 'type': 'file'},
                {'name': 'AUTOEXEC.BAT', 'type': 'file'}
            ]
        },
        {
            'name': 'GAMES',
            'type': 'folder',
            'children': [
                {'name': 'FLAPPY.EXE', 'type': 'file'},
                {'name:': 'TICTACTOE.EXE', 'type': 'file'}
            ]
        },
        {
            'name': 'DOCS',
            'type': 'folder',
            'children': [
                {'name': 'README.TXT', 'type': 'file'},
                {'name': 'MANUAL.DOC', 'type': 'file'}
            ]
        },
        {'name': 'COMMAND.COM', 'type': 'file'},
        {'name': 'MSDOS.SYS', 'type': 'file'}
    ]
}
#END OF FILE SYSTEM STUFF

def getLS(dir):
    return dir

def processCommand(command):
    output = ""
    global workingDir
    helpSuggestion = "Invalid command. Type 'help' or'/?' for help."
    cmdSplits = command.split()
    if command == "/?" or command == "help":
        output = """
echo [text]-- writes [text] to the terminal\n
ls-- reads out all of the files in the current directory\n
ls [folder]-- reads out all of the files in [folder]\n
telnet [address]-- connects to the [address]\n
clear-- clears the terminal history\n
cls-- clears the terminal history\n
        """
    elif cmdSplits[0] == "echo":
        if len(cmdSplits) == 2:
            output = cmdSplits[1]
    elif cmdSplits[0] == "ls":
        if len(cmdSplits) > 2:
            output = helpSuggestion
        elif len(cmdSplits) == 1:
            getLS(workingDir)
        elif len(cmdSplits) == 2:
            output = getLS(cmdSplits[1])
        else:
            output = getLS(workingdir)
    elif cmdSplits[0] == "telnet":
        if len(cmdSplits) > 2:
            output = "You have too many arguments. Please use <telnet [address]> to connect to a bulletin board."
        elif len(cmdSplits) == 1:
            output = "You have too few arguments. Please use <telnet [address]> to connect to a bulletin board."
        elif cmdSplits[1] == "tinboard.selfi.net":
                output = "Server Unavalible. Please try again later."
        elif cmdSplits[1] == "zephyr.beepboop.net":
            connected = 1
            output = "Connecting to <zephyr.beepboop.net>..."
        elif cmdSplits[1] == "covert.aether.net":
            connected = 2
            output = "Connecting to <covert.aether.net>..."
        else:
            output = "The server you are looking for does not exist. Please make sure the address you are typing in is correct."
    elif command == "clear" or command == "cls":
        history = []
    else:
        output = helpSuggestion
    return output

def bbsProcessor(command):
    return command


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
    # 0 = disconnected, 1 = zephyr, 2 = covert
    if connected == 0:
        processedCommand = processCommand(command)
    elif connected == 1:
        processedCommand = bbsProcessor(command)
    history.append("> " + command)
    history.append(processedCommand)
    return render_template('index.html', history = history)

#FILE SYSTEM STUFF
@app.route('/api/files')
def get_files():
    return  jsonify(FILE_SYSTEM)

@app.route('/api/file/<path:filepath>')
def get_file_content(filepath):
    return jsonify({
        'name': filepath,
        'content': f'Content of {filepath}\n\nHELPME'
    })

#END OF FILE SYSTEM STUFF

if __name__ == '__main__':
    app.run()

