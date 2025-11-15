from flask import Flask, request, render_template
app = Flask(__name__)
history = []
@app.route('/')
def index():
    global history
    print(history)
    return render_template('index.html', history = history)
@app.route('/submit', methods=['POST'])
def cmdhistory():
    global history
    joinedword = ">" + "".join(request.form['inp'])
    history.append(joinedword)
    return """
    <!DOCTYPE html>
    <head>
        <meta http-equiv="refresh" content="0; URL=/" />
    </head>
    """
if __name__ == '__main__':
    app.run()
