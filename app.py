from flask  import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "jfk"

@app.route("/")
def home_page():
	title = satisfaction_survey.title
	instruction = satisfaction_survey.instructions
	return render_template("home.html", title=title, instruction=instruction)


saved = {}
count = 0
for q in satisfaction_survey.questions:
	question = q.question
	choices = q.choices
	allow_text = q.allow_text
	saved[count] = [question, choices, allow_text]
	count += 1


@app.route("/questions/<int:id>")
def get_question(id):
	title = satisfaction_survey.title
	instruction = satisfaction_survey.instructions
	if len(responses) != id:
		flash(f"please don't play me with me right now, you're on question number {id}")
		return redirect(f"/questions/{len(responses)}")
	if id < count:
		current = saved[id]
	else:
		return redirect("/thanks")
	return render_template("form.html", title=title, instruction=instruction, question=current[0], choices=current[1], allow_text=current[2])


responses = {}

@app.route("/answer", methods=["POST"])
def save_answer():
	answer = request.form["answer"]
	responses[len(responses)] = answer
	if count < len(responses):
		return redirect("/thanks")
	print(responses)
	return redirect(f"/questions/{len(responses)}")


@app.route("/thanks")
def give_thanks():
	title = satisfaction_survey.title
	return render_template("thanks.html", title=title)
