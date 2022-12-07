from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

debug = DebugToolbarExtension(app)


@app.route('/')
def survey_start():
    """Start survey"""
    return render_template('survey.html', survey = survey)

@app.route('/start', methods =["POST"])
def start_survey():
    """Clear response list"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route('/answer', methods =["POST"])
def handle_question():
    """Get question answer, save it and redirect to next question """
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):

        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display current question"""
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", question_num = qid, question = question)

@app.route('/complete')
def complete():
    return render_template("complete.html")