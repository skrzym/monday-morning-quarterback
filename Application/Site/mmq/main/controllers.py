from flask import Blueprint, render_template, request, url_for
from config import mongo

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    mongo.db.visits.insert_one({"foo":"bar"})
    visits = mongo.db.visits.find_one()
    return str(visits)
    #return render_template('index.html')

@main.route('/getstarted/')
def get_started():
    down_list = ['1st','2nd','3rd','4th']
    quarter_list = ['1st','2nd','3rd','4th']
    clock_list = ['> 15 min', '> 10 min', '> 5 min', '> 2 min', '< 2 min', '< 1 min']
    yards_list = ['inches', 'goal', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', '10', '> 10']
    field_list = range(0,105,5)
    score_list = range(-60,61,1)

    return render_template('getstarted.html',
        down_list=down_list,
        quarter_list=quarter_list,
        clock_list=clock_list,
        yards_list=yards_list,
        field_list=field_list,
        score_list=score_list
    )

@main.route('/run/', methods=['POST'])
def run():
    down = request.form['down']
    quarter = request.form['quarter']
    clock = request.form['clock']
    yards = request.form['yards']
    field = request.form['field']
    score = request.form['score']
    guess = request.form['guess']

    # Store scenario in mongodb
    scenario = {
    'down':     down,
    'quarter':  quarter,
    'clock':    clock,
    'yards':    yards,
    'field':    field,
    'score':    score,
    'guess':    guess
    }
    mongo.db.scenarios.insert_one(scenario)
    scenarios = mongo.db.scenarios.find()

    try:
        return render_template('results.html',
        down=down,
        quarter=quarter,
        clock=clock,
        yards=yards,
        field=field,
        score=score,
        guess=guess,
        scenarios=scenarios
    )
    except:
        return "fail"
