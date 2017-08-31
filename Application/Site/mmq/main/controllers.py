<<<<<<< HEAD
from flask import Blueprint, render_template, request, url_for, jsonify
from config import mongo
import pandas as pd
import json
from bson import json_util
import retrieve_model as rmodel
from collections import Counter


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    #mongo.db.visits.insert_one({"no":"way"})
    #visits = mongo.db.visits.find_one()
    #return str(visits)
    return render_template('index.html')


@main.route('/predict/')
def get_started():
    down_list = [{'value':1,'name':'1st'},{'value':2,'name':'2nd'},{'value':3,'name':'3rd'},{'value':4,'name':'4th'}]
    quarter_list = [{'value':1,'name':'1st'},{'value':2,'name':'2nd'},{'value':3,'name':'3rd'},{'value':4,'name':'4th'}]
    clock_list = [{'value':15,'name':'<15'}, {'value':14,'name':'<14'}, {'value':13,'name':'<13'},
    {'value':12,'name':'<12'}, {'value':11,'name':'<11'}, {'value':10,'name':'<10'},
    {'value':9,'name':'<9'}, {'value':8,'name':'<8'}, {'value':7,'name':'<7'},
    {'value':6,'name':'<6'}, {'value':5,'name':'<5'}, {'value':4,'name':'<4'},
    {'value':3,'name':'<3'}, {'value':2,'name':'<2'}, {'value':1,'name':'<1'}]
    yards_list = [{'value':0,'name':'inches'}, {'value':1,'name':'1'},
    {'value':2,'name':'2'}, {'value':3,'name':'3'}, {'value':4,'name':'4'},
    {'value':5,'name':'5'}, {'value':6,'name':'6'}, {'value':7,'name':'7'},
    {'value':8,'name':'8'}, {'value':9,'name':'9'}, {'value':10,'name':'10'},
    {'value':11,'name':'11'}, {'value':12,'name':'12'}, {'value':13,'name':'13'},
    {'value':14,'name':'14'}, {'value':15,'name':'15'}, {'value':16,'name':'16'},
    {'value':17,'name':'17'}, {'value':18,'name':'18'}, {'value':19,'name':'19'},
    {'value':20,'name':'20'}, {'value':21,'name':'21'}, {'value':22,'name':'22'},
    {'value':23,'name':'23'}, {'value':24,'name':'24'}, {'value':25,'name':'25'}]
    field_list = range(0,101,1)
    score_list = range(0,61,1)

    down_dict = [{'value':1,'name':'1st'},{'value':2,'name':'2nd'},{'value':3,'name':'3rd'},{'value':4,'name':'4th'}]

    return render_template('predict.html',
=======
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
>>>>>>> master
        down_list=down_list,
        quarter_list=quarter_list,
        clock_list=clock_list,
        yards_list=yards_list,
        field_list=field_list,
<<<<<<< HEAD
        score_list=score_list,
        down_dict=down_dict
    )


@main.route('/results/', methods=['POST'])
def results():
=======
        score_list=score_list
    )

@main.route('/run/', methods=['POST'])
def run():
>>>>>>> master
    down = request.form['down']
    quarter = request.form['quarter']
    clock = request.form['clock']
    yards = request.form['yards']
    field = request.form['field']
    score = request.form['score']
<<<<<<< HEAD
    sign  = request.form['sign']
    guess = request.form['guess']

    score = str(int(score) * int(sign))

    # Store scenario in mongodb
    scenario = {
    'down':     int(down),
    'quarter':  int(quarter),
    'clock':    int(clock),
    'yards':    int(yards),
    'field':    int(field),
    'score':    int(score),
    'guess':    guess
    }

    # Insert the current user's guess into the DB
    print('Puting this into db:', scenario)
    mongo.db.scenarios.insert_one(scenario)

    # Pull User guesses from MongoDB
    #scenarios = mongo.db.scenarios.find()

    # Pull NFL Stats from MongoDB
    #nflstats = mongo.db.nfldata.find()

    guesses = {'pass':'Pass', 'run':'Run', 'punt':'Punt', 'fg':'Field Goal', 'kneel': 'QB Kneel'}

    try:
        return render_template('results.html',
        guess_title = guesses[guess],
=======
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
>>>>>>> master
        down=down,
        quarter=quarter,
        clock=clock,
        yards=yards,
        field=field,
        score=score,
        guess=guess,
<<<<<<< HEAD
        scenarios=[None],#scenarios,
        nflstats=[None]#nflstats
    )
    except Exception as e:
        return "Something went wrong..." + str(e)


@main.route('/stats/')
def tables():
    title = 'Test Table'
    title = rmodel.predict_proba(4,4,1,20,-1)
    table = title

    return render_template('stats.html', table=table, title=title)


@main.route('/data/guesses/')
def guessData():
    guess = request.args.get('guess')
    down = request.args.get('down')
    quarter = request.args.get('quarter')
    clock = request.args.get('clock')
    yards = request.args.get('yards')
    field = request.args.get('field')
    score = request.args.get('score')

    search_dict = request.args.to_dict()

    for key in search_dict:
        #if key != 'guess':
        try:
            search_dict[key] = int(search_dict[key])
        except:
            pass
    print(search_dict)
    s=[data['guess'] for data in mongo.db.scenarios.find(search_dict)]
    options = ['pass', 'run', 'punt', 'fg', 'kneel']
    count = {option:s.count(option) for option in options}
    print(count)
    return json.dumps(count, default=json_util.default)


@main.route('/data/nfl/')
def nflData():
    playtype = request.args.get('PlayType')
    down = request.args.get('down')
    quarter = request.args.get('quarter')
    clock = request.args.get('clock')
    yards = request.args.get('yards')
    field = request.args.get('field')
    score = request.args.get('score')

    search_dict = request.args.to_dict()
    for key in search_dict:
        if key != 'playtype':
            try:
                search_dict[key] = int(search_dict[key])
            except:
                pass

    s=[data["PlayType"] for data in mongo.db.nfldata.find(search_dict)]
    print(s)
    options = ['pass', 'run', 'punt', 'fg', 'kneel']
    count = {option:s.count(option) for option in options}
    print(count)
    return json.dumps(count, default=json_util.default)


@main.route('/api/predict/')
def apiPredict():
    arg_dict = request.args.to_dict()
    for key in arg_dict:
        try:
            arg_dict[key] = int(arg_dict[key])
        except:
            pass
    calculations = [
        {name:rmodel.predict_group_proba(
            arg_dict['quarter'],
            arg_dict['down'],
            arg_dict['yards'],
            arg_dict['clock'],
            arg_dict['field'],
            arg_dict['score'],
            name)
        } for name in ['quarter', 'down', 'yards', 'timeunder', 'yrdline100', 'scorediff']
    ]
    calculations.append({'request':rmodel.predict_proba(
        arg_dict['quarter'],
        arg_dict['down'],
        arg_dict['yards'],
        arg_dict['clock'],
        arg_dict['field'],
        arg_dict['score'],
        False)
    })
    return jsonify(calculations)
=======
        scenarios=scenarios
    )
    except:
        return "fail"
>>>>>>> master
