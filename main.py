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
@quillit: The idea was actually born here though. Some people were brought together, and it wouldn't have existed if those people weren't on and weren't chatting in that chat room at that specific moment. Very, very long time ago in this chat room. I wonder if I can salvage any data from it from my NETWORK SAVE<br>
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

aetherLSSC = """eurus -- no description<br>
notos -- no description<br>
bigapl -- no description<br>"""

aethereurus = """@snookie: sorry guys my cat knocked over my drink again<br>
@amarylisss: lol again?<br>
@snookie: yeah he's been a real troublemaker lately<br>
@quillit: hey has anyone been able to get on tin board?<br>
@amarylisss: no it's still down<br>
@snookie: what's tin board?<br>
@gig-jig: only the best bbs that ever existed<br>
@snookie: oh interesting. my cat just jumped on my keyboard<br>
@quillit: snookie your cat sounds like a menace<br>
@snookie: he is but i love him<br>
@amarylisss: what's his name?<br>
@snookie: whiskers. very original i know<br>
@gig-jig: tin board has been offline for like a week now<br>
@snookie: huh weird. anyway brb cat problems<br>
@quillit: yeah someone's holding it hostage or something<br>
@amarylisss: that's wild<br>
@snookie: ok back he was trying to eat my headphone cord<br>
@amarylisss: snookie you said you knew about tin board earlier?<br>
@snookie: no i asked what it was<br>
@quillit: you seemed really interested when gig mentioned it though<br>
@snookie: i mean it sounded cool i guess<br>
@snookie: wait did i say something? my cat was walking on my keys<br>
@amarylisss: ...right<br>
@gig-jig: anyway if anyone figures out the tin board thing let me know<br>
@snookie: yeah let me know too. for curiosity."""

aethernotos = """@vivir-day: reminder that Server maintenance is scheduled for next tuesday<br>
@ant-aunt: thanks for the heads up<br>
@vivir-day: also the music swap meet is happening this weekend if anYone waNts to participate<br>
@jaybird: i'll bring some recOrds<br>
@ant-aunt: what time?<br>
@vivir-day: starts at 2pm, goes until wheNever<br>
@jaybird: sounds good<br>
@ant-aunt: communitY server went down again btw<br>
@vivir-day: seriously? that's the third tiMe this mOnth<br>
@ant-aunt: yeah so the school kids are stuck watching the old vcr tapes For movie day<br>
@jaybird: at least those still work<br>
@vivir-day: has anyone else noticed the police have Been aRound mOre?<br>
@ant-aunt: yeah they've been asking abOut electronics<br>
@jaybird: they came by the radio shacK yesterday asking queStions<br>
@vivir-day: what kind of quesTions?<br>
@jaybird: who's been buying whAt, if anyone's been acTing WeIrd<br>
@ant-aunt: i heard someone in Town might've been doing something sketcHy on their computer<br>
@vivir-day: like what?<br>
@ant-aunt: no idea but the copS seem pretty interested<br>
@jaybird: weird times<br>
@vivir-day: newsletter goes out friday, send me any announcements by thursday<br>
@ant-aunt: will do"""

aetherbigapl = """@tech-wizard: JUST FINISHED MY 4TH CELSIUS<br>
@code-goblin: bro it's 2pm calm down<br>
@tech-wizard: PARTHENON IS IN 3 DAYS I NEED TO BE READY<br>
@byte-knight: why is there only celsius left<br>
@code-goblin: WHERE DID ALL THE ALANI GO<br>
@tech-wizard: AND NO MONSTER??? THIS IS A CRISIS<br>
@byte-knight: parthenon is gonna be insane this year<br>
@code-goblin: if i see one more game where everyone just dies i'm gonna lose it<br>
@tech-wizard: what's wrong with death games?<br>
@code-goblin: there's been 50 OF THEM IN THE LAST 3 DAYS<br>
@byte-knight: skill issue<br>
@code-goblin: SKILL ISSUE??? they're ALL THE SAME!<br>
@tech-wizard: hey does anyone have starbursts<br>
@byte-knight: random but yeah i have some<br>
@tech-wizard: can i have the pink ones<br>
@byte-knight: absolutely not<br>
@code-goblin: the disrespect<br>
@tech-wizard: FINE keep your pink starbursts<br>
@code-goblin: anyway back to these death games<br>
@byte-knight: just don't play them?<br>
@code-goblin: but what if one of them is actually good<br>
@tech-wizard: they're not<br>
@code-goblin: yeah you're probably right<br>
@byte-knight: anyone got access to that new board?<br>
@tech-wizard: which one<br>
@byte-knight: cascade.underground.net<br>
@code-goblin: never heard of it<br>
@byte-knight: user is [VIEW NOTOS] password is [REDACTED] [VIEW C:\SYSTEM CONFIG]<br>
@tech-wizard: *CHUGS CELSIUS* STOP SPEAKING IN RIDDLES<br>
@code-goblin: dude you're gonna have a heart attack<br>
@tech-wizard: WORTH IT FOR PARTHENON"""

cascadeLSSC = """babble -- no description<br>
the-mountains -- no description<br>
ocean-view -- no description"""

cascadebabble = """@MOD: Messages deleted.<br>
@byte-knight: WHAT
@fifififi: WHAT
@vivir-day: WHAT
@ire-synth: crazy thing to admitt on cascade
@snookie: mistyped ssorryp
@snookie: cat
@fifififi: craziest mistype ever???
@cave-caave: no shot that was a mistype
@ire-synth: snookie????
@snookie: wwonrg chanell
@vivir-day: snookie what are you UP to?????
@snookie: jst cat
@ire-synth: bro just admit it already
@MOD: Message deleted.
@ire-synth: we all know it
@ire-synth: you can't hide it forever.
@MOD: User ire-synth has been banned.
@cave-caave: HELLO??????
@fifififi: craziest cascade night of my life
@vivir-day: ?????
@ant-aunt: waht did i miss
@vivir-day: ant-aunt check ocean-view then ocean view"""

cascadethemountains = """@snookie: does this picture look good
@MOD: [DELETED PLEASE VIEW IN [documents]] cattu.jpg
@gig-jig: bro? what is that image??
@snookie: what do you think
@gig-jig: ???
@cave-caave: wdym 'does this look good'
@snookie: does it look good
@cave-caave: your cat looks great man i don know what you tell ya
@snookie: good."""

cascadeoceanview = """@snookie: i think i need to shut down tin board
@cvs: ? why?
@snookie: you know why.
@kingmimi: oh the police
@cvs: police???
@jaybird: 

"""

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
                    {'name': 'MANUAL.DOC', 'type': 'file'},
                    {'name': 'cattu.PNG', 'type': 'file'}
                ]
            },
            {'name': 'COMMAND.COM', 'type': 'file'},
            {'name': 'MSDOS.SYS', 'type': 'file'}
        ]
    }

#END OF FILE SYSTEM STUFF
def processCommand(command):
    output = ""
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
telnet [address] -- connects to the [address]<br>
        """
    elif cmdSplits[0] == "echo":
        if len(cmdSplits) == 2:
            output = cmdSplits[1]
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
        elif cmdSplits[1] == "cascade.underground.net":
            connected = 3
            logstatus = 1
            output = "Connecting to cascade.underground.net...<br>Please enter in your username."
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

#cascade.underground.net

#user: stream
#password: waterfall

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
        elif connected == 3: #cascade
            if len(cmdSplits) > 1:
                connected = 0
                logstatus = 0
                output = "Error: No spaces allowed in names. Disconnected."
            elif command == "stream":
                logstatus = 2
                output = "Username found.<br>Please enter in your password"
            else:
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
        elif connected == 3: #cascade
            if len(cmdSplits) > 1:
                connected = 0
                logstatus = 0
                output = "Error: No spaces allowed in names. Disconnected."
            elif command == "waterfall":
                global slotsUnlocked
                slotsUnlocked = True
                logstatus = 3
                output = """Password correct! Welcome, stream, to Cascade~"""
            else:
                connected = 0
                logstatus = 0
                output = "Error: Incorrect password. Disconnected."
        
        

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
            elif connected == 3:
                output = """
help (or) /? -- display this message<br>
ls-sc -- list available subchats<br>
cn-sc [subchat] -- connect to an available subchat<br>
disconnect -- disconnect from Cascade
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
            elif connected == 3:
                connected = 0
                logstatus = 0
                output = """Disconnected from cascade.underground.net."""



        elif connected == 1:
            if command == "ls-sc":
                output = f"""LIST OF SUBCHATS:<br>
{zephyrLSSC}
                """
            elif cmdSplits[0] == "cn-sc":
                if len(cmdSplits) < 1:
                    output = "Error: Too few arguments. Please type cn-sc [subchat] to connect to a subchat."
                elif len(cmdSplits) > 2:
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

            if command == "ls-sc":
                output = f"""LIST OF SUBCHATS:<br>
{aetherLSSC}
                """
            elif cmdSplits[0] == "cn-sc":
                if len(cmdSplits) < 1:
                    output = "Error: Too few arguments. Please type cn-sc [subchat] to connect to a subchat."
                elif len(cmdSplits) > 2:
                    output = "Error: Too many arguments. Please type cn-sc [subchat] to connect to a subchat."
                elif cmdSplits[1] == "eurus":
                    output = f"""~#eurus~<br>
                    {aethereurus}"""
                elif cmdSplits[1] == "notos":
                    output = f"""~#notos~<br>
                    {aethernotos}"""
                elif cmdSplits[1] == "bigapl":
                    output = f"""~#bigapl~<br>
                    {aetherbigapl}"""
        
        elif connected == 3:
            if command == "ls-sc":
                output = f"""LIST OF SUBCHATS:<br>
                {cascadeLSSC}"""
            elif cmdSplits[0] == "cn-sc":
                if len(cmdSplits) < 1:
                    output = "Error: Too few arguments. Please type cn-sc [subchat] to connect to a subchat."
                if command == "cn-sc":
                    output = "Error: Too few arguments. Please type cn-sc [subchat] to connect to a subchat."
                elif len(cmdSplits) > 2:
                    output = "Error: Too many arguments. Please type cn-sc [subchat] to connect to a subchat."
                elif cmdSplits[1] == "babble":
                    output = f"""*#babble*<br>
                    {cascadebabble}"""
                elif cmdSplits[1] == "the-mountains":
                    output = f"""*#the-mountains*<br>
                    {cascadethemountains}"""
                elif cmdSplits[1] == "ocean-view":
                    output = f"""*#ocean-view*<br>
                    {cascadeoceanview}"""
            else:
                output = helpSuggestion

            
    else:
        connected = 0
        logstatus = 0
        output = "Error: Malformed connection. Disconnected."
    return output

app = Flask(__name__)
history = []
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def api_command():
    global connected
    # Accept form-encoded or JSON payloads
    data = request.get_json(silent=True)
    if data and 'command' in data:
        command = data['command']
    else:
        # fallback to form data
        command = request.form.get('inp', '')
    command = "".join(command)
    if connected == 0:
        processedCommand = processCommand(command)
    elif connected in (1,2,3):
        processedCommand = bbsProcessor(command)
    else:
        processedCommand = processCommand(command)
    return jsonify({'response': processedCommand})

#FILE SYSTEM STUFF
@app.route('/api/files')
def get_files():
    return jsonify(get_file_system())

@app.route('/api/file/<path:filepath>')
def get_ffile_content(filepath):
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
        'README.TXT': 'Welcome to Bullet-Tin Board!\n\nThis is a demo file system made for the Bullet-Tin Board project.\n PASS: i-am-so-cool\n USER: blue-fire\n Made @ Parthenon 2025!!!',
        'NETWORK_SAVE.TXT': f'Network Configuration:\n ...\nSaved data:\n COVERT.AETHER.NET\n\n{chat_log}',
        'MANUAL.DOC': 'MANUAL\n======\n\n1. Use the file explorer\n2. Double-click files to open... (pretty self explanitory BTW some files will actually work - take a look)\n3. Enjoy!',
        'CONFIG.SYS': 'WATTAGE USED = 42\nALLOCATED RAM =670\nTEMP FILES = 38\nECC ENABLED = TRUE\nROUTER = CONNECTED\nFIRMWARE UPDATED = YES\nANTIVIRUS = ENABLED\nLATENCY = 40.107ms\nLAN = DISABLED', 
        'AUTOEXEC.BAT': '@ECHO OFF\nPROMPT $P$G\nPATH C:\\DOS;C:\\WINDOWS'    }
    
    filename = filepath.replace('\\', '/').split('/')[-1]
    content = content_map.get(filename, f'Contents of {filename}')
    
    return jsonify({
        'name': filename,
        'content': content
    })
    
@app.route('/api/file/<path:filepath>')
def get_file_content(filepath):
    filename = filepath.replace('\\', '/').split('/')[-1]
    
    if filename.upper().endswith('.PNG') or filename.upper().endswith('.BMP') or filename.upper().endswith('.JPG'):
        return jsonify({
            'name': filename,
            'type': 'image',
            'url': url_for('static', filename='cattu.PNG')  # Direct reference
        })

    
    
    content_map = {
        'README.TXT': '...',
    }
    
    content = content_map.get(filename, f'Contents of {filename}')
    return jsonify({
        'name': filename,
        'content': content
    })
#END OF FILE SYSTEM STUFF

if __name__ == '__main__':
    app.run()
#EOF
