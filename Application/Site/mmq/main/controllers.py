from flask import Blueprint, render_template, request, url_for
from config import mongo
import pandas as pd

########################################################
# Setup Pandas Masking Function
# https://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
def mask(df, key, value, operator='=='):
    if type(value) is list:
        if operator == 'not':
            return df[df[key].apply(lambda x: x not in value)]
        else:
            return df[df[key].apply(lambda x: x in value)]
    else:
        if operator == '!=':
            return df[df[key] != value]
        elif operator == '>':
            return df[df[key] > value]
        elif operator == '>=':
            return df[df[key] >= value]
        elif operator == '<':
            return df[df[key] < value]
        elif operator == '<=':
            return df[df[key] <= value]
        else:
            return df[df[key] == value]
# Set Pandas DF Mask funciton
pd.DataFrame.mask = mask

# Pull Large DataFrame
rs_pbp = pd.read_pickle('mmq\main\data\playbyplaydata\\rs_pbp.pkl')
po_pbp = pd.read_pickle('mmq\main\data\playbyplaydata\\po_pbp.pkl')

########################################################
# Flask App
main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    mongo.db.visits.insert_one({"no":"way"})
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

    # Convert mongoDB data to pandas DF
    scenarios_df = pd.DataFrame.from_records(scenarios)
    masks = [
        ['down', down],
        ['quarter', quarter],
        ['clock', clock],
        ['yards', yards],
        ['field', field],
        ['score', score],
        #['guess', guess]
    ]

    # Apply provided masks to the scenarios data
    # Can also be done via mongoDB filtering vs pandas
    for mask in masks:
        scenarios_df = scenarios_df.mask(mask[0], mask[1])
    # Reset the Index and group by the different possible guesses
    scenarios_df = scenarios_df.reset_index(drop=True)
    guesses = scenarios_df.groupby('guess').agg({'_id':len}).reset_index()
    guesses.columns= ['Guess','Count']
    guesses_html = guesses.to_html(classes='table')

    # Pull NFL Stats from MongoDB
    nflstats = guesses_html

    try:
        return render_template('results.html',
        down=down,
        quarter=quarter,
        clock=clock,
        yards=yards,
        field=field,
        score=score,
        guess=guess,
        scenarios=guesses_html,
        nflstats=nflstats
    )
    except:
        return "fail"

@main.route('/stats/')
def tables():
    title = 'Test Table'
    #rs_pbp = pd.read_pickle('mmq\main\data\playbyplaydata\\rs_pbp.pkl')
    #po_pbp = pd.read_pickle('mmq\main\data\playbyplaydata\\po_pbp.pkl')

    rs_pass_attempts = rs_pbp.groupby('posteam').agg({'PassAttempt':sum,'RushAttempt':sum})
    po_pass_attempts = po_pbp.groupby('posteam').agg({'PassAttempt':sum,'RushAttempt':sum})

    table = rs_pass_attempts.to_html(classes='table')

    return render_template('stats.html', table=table, title=title)
