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

dates = [
    {
    'day':'Tuesday 21 Decemebr',
    'startTime': '14:00',
    'endTime': '15:00'
    },
    {
    'day':'Saturday 25 Decemebr',
    'startTime': '14:00',
    'endTime': '15:00'
    }

]
@app.route('/newjob')
def newJob():
    return render_template('cli/createjob.html', stages=stages)

@app.route('/selectint')
def selectint():
    return render_template('apl/interview.html', dates=dates)

@app.route('/compquestions', methods=('GET', 'POST'))
def compquestions():
        return render_template('compquestions.html', questions=questions)

@app.route('/review')
def review():
    return render_template('review.html', answers=answers, interview=True)

@app.route('/selectinterview')
def interviewselect():
    return render_template('selectInterview.html')

if __name__ == '__main__':
    app.run(debug=True)
