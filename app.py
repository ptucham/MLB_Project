from flask import *
import os
import pitcher_data_pybaseball
import batter_data_pybaseball

app = Flask(__name__, static_url_path='/static')

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
    if request.form['submit'] == 'Show Pitcher Data':
        pitcher_data_pybaseball.main(first_name, last_name, start_date, end_date, team)
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, 'data', 'pitcher_graph_data.json')
        data = json.load(open(json_url))
        return render_template('pitcher_results.html', data=data, fname=first_name, lname=last_name, sdate=start_date, edate=end_date, team=team)
    else:
        batter_data_pybaseball.main(first_name, last_name, start_date, end_date, team)
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, 'data', 'batter_graph_data.json')
        data = json.load(open(json_url)) 
        return render_template('batter_results.html', data=data, fname=first_name, lname=last_name, sdate=start_date, edate=end_date, team=team)