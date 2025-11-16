from flask import Flask, request, render_template, jsonify

connected = 0
logstatus = 0
slotsUnlocked = False

zephyrLSSC = """west-wind -- General chat<br>
fan-fans -- Get coding support and talk about CS projects<br>
boreas -- Smaller general chat"""

zephyrwestwind = """@ire-synth: i told you that wouldn't work!<br>
@tincture: bro, you did not know that beforehand<br>
@tincture: like<br>
@tincture: you said i should have tried it<br>
@ire-synth: ??<br>
@tincture: you supptortde it<br>
@quillit: guys<br>
@tincture: **suportedd<br>
@ire-synth: bro you know opening that file was stuipid<br>
@tincture: **SUPPORTED<br>
@ire-synth: i was being sarcastic<br>
@tincture: bro<br>
@quillit: guys<br>
@tincture: like<br>
@tincture: quillit what??<br>
@ire-synth: quillit.<br>
@ire-synth: quillittttttt<br>
@ire-synth: quillit! it's been two minutes what is going on!<br>
@quillit: srry distracted<br>
@tincture: what's good?<br>
@quillit: tin board is offline<br>
@gig-jig: WHAT<br>
@gig-jig: WHY???<br>
@ire-synth: really?<br>
@tincture: what's tin board?<br>
@quillit: the greatest bbs EVER!<br>
@gig-jig: who shut it down??<br>
@new-12345: Wayfarers of BBS. I have killed your beloved Tin Board. If you ever wish to see it again, you must past through my trails. First, you must gain access to a private BBS using the following hints:<br>
@new-12345: Address: [1].[2].net<br>
@new-12345: Username: [3]<br>
@new-12345: Password: [4]<br>
@new-12345: [1] -> i Can't see how yOu will eVER find This out.<br>
@new-12345: [2] -> There's a new BBS service.<br>
@new-12345: [3] -> Beats rock.<br>
@new-12345: [4] -> Tin Board wouldn't have existed without it.<br>
@MOD: **THIS CHAT IS READ-ONLY UNTIL FUTURE NOTICE.**"""

#covert.aether.net
#user: paper
#pw: fanfans

zephyrfanfans = """@quillit: Have you heard of the Tin Board?<br>
@ant-aunt: Uh. No. What Is It?<br>
@quillit: It's like uh... another place like this. The vibes are different<br>
@quillit: though<br>
@ant-aunt: How?<br>
@quillit: Hard to describe... it just was special.<br>
@quillit: The idea was actually born here though. Some people were brought together, and it wouldn't have existed if those people weren't on and weren't chatting in that chat room at that specific moment. Very, very long time ago in this chat room.<br>
@ant-aunt: Interesting<br>
@quillit: ...i should go log on it<br>
@quillit: wait<br>
@quillit no no no no<br>
@MOD: **THIS CHAT IS READ-ONLY UNTIL FUTURE NOTICE.**"""


zephyrboreas = """@gig-jig: Did you see that new bbs hosting system?<br>
@gig-jib: airther?<br>
@vivir-day: aether?<br>
@gig-jib: Yeah, aether.net<br>
@gig-jib: I don't know how legit it is, but I've seen a lot of new people using it<br>
@vivir-day: might start my own bbs on that soon, idk<br>
@gig-jig: WHAT<br>
@vivir-day: ?<br>
@vivir-day: ?? gig??<br>
@gig-jig: west-wind<br>
@MOD: **THIS CHAT IS READ-ONLY UNTIL FUTURE NOTICE.**"""

#STUFF FOR THE FILE EXPLORER
def get_file_system():
    games_children = [
        {'name': 'FLAPPY.EXE', 'type': 'file'},
        {'name': 'TICTACTOE.EXE', 'type': 'file', 'executable': True}
    ]
    
    if slotsUnlocked:
        games_children.append({'name': 'SLOTS.EXE', 'type': 'file', 'executable': True})
    
    return {
        'name': 'C:\\',
        'type': 'folder',
        'children': [
            {
                'name': 'SYSTEM',
                'type': 'folder',
                'children': [
                    {'name': 'CONFIG.SYS', 'type': 'file'},
                    {'name': 'NETWORK_SAVE.TXT', 'type': 'file'}
                ]
            },
            {
                'name': 'GAMES',
                'type': 'folder',
                'children': games_children
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


def getLS(dir):
    def traverse_folder(folder, path):
        if folder['name'] == path:
            return folder.get('children', [])
        if 'children' in folder:
            for child in folder['children']:
                if child['type'] == 'folder':
                    result = traverse_folder(child, path)
                    if result is not None:
                        return result
        return None

    if dir == 'C:\\':
        return FILE_SYSTEM['children']
    return traverse_folder(FILE_SYSTEM, dir)

#END OF FILE SYSTEM STUFF
def processCommand(command):
    output = ""
    global workingDir
    global history
    global connected
    global logstatus
    helpSuggestion = "Invalid command. Type 'help' or'/?' for help."
    cmdSplits = command.split()
    if command == "":
        output = ""
    elif command == "/?" or command == "help":
        output = """
help (or) /? -- display this help message<br>
echo [text] -- writes [text] to the terminal<br>
ls -- reads out all of the files in the current directory<br>
ls [folder] -- reads out all of the files in [folder]<br>
telnet [address] -- connects to the [address]<br>
clear -- clears the terminal history<br>
cls -- clears the terminal history
        """
    elif cmdSplits[0] == "echo":
        if len(cmdSplits) == 2:
            output = cmdSplits[1]
    elif cmdSplits[0] == "ls":
        if len(cmdSplits) > 2:
            output = helpSuggestion
        elif len(cmdSplits) == 1:
            output = getLS(workingDir)
        elif len(cmdSplits) == 2:
            output = getLS(cmdSplits[1])
    elif cmdSplits[0] == "telnet":
        if len(cmdSplits) > 2:
            output = "You have too many arguments. Please use telnet [address] to connect to a bulletin board."
        elif len(cmdSplits) == 1:
            output = "You have too few arguments. Please use telnet [address] to connect to a bulletin board."
        elif cmdSplits[1] == "tinboard.selfi.net":
                output = "Server Unavalible. Please try again later."
        elif cmdSplits[1] == "zephyr.beepboop.net":
            connected = 1
            logstatus = 1
            output = "Connecting to zephyr.beepboop.net...<br>Please enter in your username."
        elif cmdSplits[1] == "covert.aether.net":
            connected = 2
            logstatus = 1
            output = "Connecting to covert.aether.net...<br>Please enter in your username."
        else:
            output = "The server you are looking for does not exist. Please make sure the address you are typing in is correct."
    else:
        output = helpSuggestion
    return output

# Zephyr Log-in:

#user: blue-fire
#password: i-am-so-cool

#covert aether Log-in

#user: paper
#password: fan-fans

def bbsProcessor(command):
    output = ""
    global workingDir
    global history
    global connected
    global logstatus
    helpSuggestion = "Invalid command. Type 'help' or'/?' for help."
    cmdSplits = command.split()

    #print("BBS PROCESSOR")
    #print(str(connected) + ", " + str(logstatus))

    print(logstatus)
    print

    if logstatus == 0:
        output = "Please enter in your username"
        logstatus = 1
        return
    elif logstatus == 1:
        if connected == 1: #zephyr
            if len(cmdSplits) > 1:
                connected = 0
                logstatus = 0
                output = "Error: No spaces allowed in names. Disconnected."
            elif command == "blue-fire":
                logstatus = 2
                output = "Username found.<br>Please enter in your password"
            else:
                connected = 0
                logstatus = 0
                output = "Username not found. Disconnected."
        elif connected == 2: #covert
            print("connected 2")
            if len(cmdSplits) > 1:
                print("too long")
                connected = 0
                logstatus = 0
                output = "Error: No spaces allowed in names. Disconnected."
            elif command == "paper":
                print("paper")
                logstatus = 2
                output = "Username found.<br>Please enter in your password"
            else:
                print("error")
                connected = 0
                logstatus = 0
                output = "Username not found. Disconnected."
            return output
    elif logstatus == 2:
        if connected == 1: #zephyr
            if len(cmdSplits) > 1:
                connected = 0
                logstatus = 0
                output = "Error: No spaces allowed in names. Disconnected."
            elif command == "i-am-so-cool":
                logstatus = 3
                output = """Password correct! Welcome, blue_fire, to THE ZEPHYRRRRR"""
            else:
                connected = 0
                logstatus = 0
                output = "Error: Incorrect password. Disconnected."
        elif connected == 2: #covert
            if len(cmdSplits) > 1:
                connected = 0
                logstatus = 0
                output = "Error: No spaces allowed in names. Disconnected."
            elif command == "fan-fans":
                logstatus = 3
                output = """Password correct! Welcome, paper, to Covert Aether"""
            else:
                connected = 0
                logstatus = 0
                output = "Error: Incorrect password. Disconnected."
            return
        

    #CONNECTED TO A SERVER

    elif logstatus == 3:
        if command == "help" or command == "/?":
            if connected == 1:
                output = """
help (or) /? -- display this message<br>
ls-sc -- list available subchats<br>
cn-sc [subchat] -- connect to an available subchat<br>
disconnect -- disconnect from Zephyr
                """
            elif connected == 2:
                output = """
help (or) /? -- display this message<br>
ls-sc -- list available subchats<br>
cn-sc [subchat] -- connect to an available subchat<br>
disconnect -- disconnect from Covert Aether
                """
        elif command == "disconnect":
            if connected == 1:
                connected = 0
                logstatus = 0
                output = """Disconnected from zephyr.beepboop.net."""
            elif connected == 2:
                connected = 0
                logstatus = 0
                output = """Disconnected from covert.aether.net."""
        elif connected == 1:
            if command == "ls-sc":
                output = f"""LIST OF SUBCHATS:<br>
{zephyrLSSC}
                """
            elif cmdSplits[0] == "cn-sc":
                if len(cmdSplits) < 1:
                    output = "Error: Too few arguments. Please type cn-sc [subchat] to connect to a subchat."
                if len(cmdSplits) > 2:
                    output = "Error: Too many arguments. Please type cn-sc [subchat] to connect to a subchat."
                elif cmdSplits[1] == "west-wind": #general
                    output = f"""[[#west-wind]]<br>
                    {zephyrwestwind}"""
                elif cmdSplits[1] == "fan-fans": #tech-help
                    output = f"""[[#fan-fans]]<br>
                    {zephyrfanfans}"""
                elif cmdSplits[1] == "boreas":
                    output = f"""[[#boreas]]<br>
                    {zephyrboreas}"""
            
            
            else:
                output = helpSuggestion
        elif connected == 2:
            #all other covert aether commands
            return
    else:
        connected = 0
        logstatus = 0
        output = "Error: Malformed connection. Disconnected."
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
    global connected
    command = "".join(request.form['inp'])
    # 0 = disconnected, 1 = zephyr, 2 = covert
    if connected == 0:
        processedCommand = processCommand(command)
    elif connected == 1:
        processedCommand = bbsProcessor(command)
    elif connected == 2:
        processedCommand = bbsProcessor(command)
    history.append("> " + command)
    history.append(processedCommand)
    return render_template('index.html', history = history)

#FILE SYSTEM STUFF
@app.route('/api/files')
def get_files():
    return jsonify(get_file_system())

@app.route('/api/file/<path:filepath>')
def get_file_content(filepath):
    chat_log = (
        '@jaybird: anyone catch that new album yet? \n'
    '@amaryllisss: yeah picked it up yesterday, snookie u get it? \n'
    '@snookie: oh no not yet \n'
    '@jaybird: how come? you were talking about it all week \n'
    '@snookie: just haven\'t made it 2 the record store \n'
    '@amaryllisss: you\'ve been hard 2 reach lately \n'
    '@snookie: yeah been kind of busy \n'
    '@snookie: got a new cat actually \n'
    '@jaybird: kool, what kind? \n'
    '@snookie: just a tabby \n'
    '@amaryllisss: you ok man? you seem weird \n'
    '@snookie: no yeah i\'m fine, obviously, why would you say that \n'
    '@jaybird: idk you just signed off real quick last time \n'
    '@snookie: oh that? yeah had to take care of somethng \n'
    '@amaryllisss: something or someone came home? lol \n'
    '@snookie: what? no just had to go \n'
    '@snookie: so anyway what\'d you think of the album \n'
    '@jaybird: it\'s chill, 2nd side is better \n'
    '@snookie: cool cool \n'
    '@amaryllisss: you\'re being real short tonight snookie \n'
    '@snookie: sorry just distracted i guess \n'
    '@jaybird: that thing from last week still bothering u? \n'
    '@snookie: what thing \n'
    '@jaybird: never mind, thought u mentioned something \n'
    'END OF SAVED LOG'
    )
    
    content_map = {
        'README.TXT': 'Welcome to Bullet-Tin Board!\n\nThis is a demo file system made for the Bullet-Tin Board project.\n Feel free to explore the files and folders.\n Made @ Parthenon 2025!!!',
        'NETWORK_SAVE.TXT': f'Network Configuration:\n ...\nSaved data:\n COVERT.AETHER.NET\n\n{chat_log}',
        'MANUAL.DOC': 'MANUAL\n======\n\n1. Use the file explorer\n2. Double-click files to open... (pretty self explanitory BTW some files will actually work - take a look)\n3. Enjoy!',
        'CONFIG.SYS': 'DEVICE=HIMEM.SYS\nFILES=40\nBUFFERS=20',
        'AUTOEXEC.BAT': '@ECHO OFF\nPROMPT $P$G\nPATH C:\\DOS;C:\\WINDOWS'    }
    
    filename = filepath.replace('\\', '/').split('/')[-1]
    content = content_map.get(filename, f'Contents of {filename}')
    
    return jsonify({
        'name': filename,
        'content': content
    })

#END OF FILE SYSTEM STUFF

if __name__ == '__main__':
    app.run()
#EOF