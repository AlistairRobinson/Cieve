from flask import Flask, render_template
app = Flask(__name__)
questions = [
    {
    'Number': '1',
    'Question': 'What is the capital of Nigeria',
    'Possibleansw':[
        'Lagos',
        'Abuja',
        'Qwara'
    ]
    },

    {
    'Number': '2',
    'Question': 'Whats your name',
    'Possibleansw':[]
    }

]

stages = [
    {

    'id' : '1',
    'desc' : 'First round interview'
    }

]

answers = [
    {
    'Division': 'Tech',
    'Role': 'Intern',
    'Country':'United Kingdom',
    'numberofvacancies': 10,
    'Stages': [
            {
            'StageDesc':"Online application"
        },
        {
            'StageDesc':'Interview'
        }
        ],
    'Skills': [
        {
        'Skill':'Python',
        'Proficiency':10
        },
        {
        'Skill':'HTML',
        'Proficiency': 7
        }
    ]
    }
]

interviews = {}
interviews["Stage 1"] = ['phone call', 3]
interviews["Stage 2"] = ['face to face', 3]
@app.route('/newjob')
def newJob():
    return render_template('cli/createjob.html', stages=stages)

@app.route('/compquestions', methods=('GET', 'POST'))
def compquestions():
        return render_template('compquestions.html', questions=questions)

@app.route('/review')
def review():
    return render_template('cli/review.html', answers=answers, interview=True, interviews= interviews)

@app.route('/selectinterview')
def interviewselect():
    return render_template('selectInterview.html')

if __name__ == '__main__':
    app.run(debug=True)
