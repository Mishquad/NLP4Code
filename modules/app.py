from flask import Flask, request, render_template_string
from mistral_wrapper import MistralWrapper

app = Flask(__name__)
mistral_wrapper = MistralWrapper('1')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        answer = mistral_wrapper.generate_completion(user_input)
        return render_template_string('''
            <form method="post">
                <textarea name="user_input" rows="4" cols="50">{{ user_input }}</textarea><br>
                <input type="submit" value="Submit">
            </form>
            <h3>Answer:</h3>
            <p>{{ answer }}</p>
        ''', user_input=user_input, answer=answer)
    return '''
        <form method="post">
            <textarea name="user_input" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(port=5000)
