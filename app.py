from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    first_name = request.form['fname']
    last_name = request.form['lname']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    team = request.form['teams']
    return 'Pitcher name: %s %s <br/> Dates: %s through %s<br/> Team: %s <br/> <a href="/">Back Home</a>' % (first_name, last_name, start_date, end_date, team)