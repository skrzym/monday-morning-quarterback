from flask import Blueprint, render_template, request, url_for
from config import mongo
import pandas as pd
import json
from bson import json_util
import retrieve_model as rmodel


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    #mongo.db.visits.insert_one({"no":"way"})
    #visits = mongo.db.visits.find_one()
    #return str(visits)
    return render_template('index.html')


@main.route('/getstarted/')
def get_started():
    down_list = ['1st','2nd','3rd','4th']
    quarter_list = ['1st','2nd','3rd','4th']
    clock_list = ['> 15 min', '> 10 min', '> 5 min', '> 2 min', '< 2 min', '< 1 min']
    yards_list = ['inches', 'goal', '1', '2', '3', '4', '5', '6', '7' ,'8', '9', '10', '> 10']
    field_list = range(0,105,5)
    score_list = range(0,61,1)

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
    sign  = request.form['sign']
    guess = request.form['guess']

    score = score * int(sign)

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

    # Insert the current user's guess into the DB
    mongo.db.scenarios.insert_one(scenario)

    # Pull User guesses from MongoDB
    #scenarios = mongo.db.scenarios.find()

    # Pull NFL Stats from MongoDB
    #nflstats = mongo.db.nfldata.find()


    try:
        return render_template('results.html',
        down=down,
        quarter=quarter,
        clock=clock,
        yards=yards,
        field=field,
        score=score,
        guess=guess,
        scenarios=[None],#scenarios,
        nflstats=[None]#nflstats
    )
    except:
        return "fail"


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
    quarter = request.args.get('qtr')
    clock = request.args.get('clock')
    yards = request.args.get('yards')
    field = request.args.get('field')
    score = request.args.get('score')

    search_dict = request.args.to_dict()

    for key in search_dict:
        if key != 'guess':
            try:
                search_dict[key] = int(search_dict[key])
            except:
                pass

    s=[data for data in mongo.db.scenarios.find(search_dict)]

    return json.dumps(s, default=json_util.default)


@main.route('/data/nfl/')
def nflData():
    playtype = request.args.get('PlayType')
    down = request.args.get('down')
    quarter = request.args.get('qtr')
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

    s=[data for data in mongo.db.nfldata.find(search_dict)]

    return json.dumps(s, default=json_util.default)


@main.route('/api/predict/')
def apiPredict():
    arg_dict = request.args.to_dict()
    for key in arg_dict:
        try:
            arg_dict[key] = int(arg_dict[key])
        except:
            pass

    return rmodel.predict_proba(
        arg_dict['qtr'],
        arg_dict['down'],
        arg_dict['yards'],
        arg_dict['clock'],
        arg_dict['field'],
        arg_dict['score']
    )
