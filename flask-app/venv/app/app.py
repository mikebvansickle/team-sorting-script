from flask import Flask, render_template
import requests
import json
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():

    #Sorts by scores
    def Sort(arr):
        for i in range(0, len(arr)):
            current = arr[i]['score']
            for j in range(i, len(arr)):
                if arr[j]['score'] >= arr[i]['score']:
                    arr[j], arr[i] = arr[i], arr[j]


    teamOne = requests.get("http://138.197.91.29:8000/scores")
    outfile = open("teamdata.txt", "w")
    outfile.write(str(teamOne.text))
    outfile.close()
    dataOne = json.loads(teamOne.text)

    #Adds Location to Richmond teams
    for team in dataOne['standings']:
        team['team'] = '[RVA] ' + team['team']

    #Loads JSON data from file -- Will replace this once
    #other endpoints are up
    with open('teamTwo.json', 'r') as f:
        teamTwo = json.load(f)

    #Adds location to Norfolk team and appends
    #each team to original JSON data
    for team in teamTwo['standings']:
        team['team'] = '[HR] ' + team['team']
        dataOne['standings'].append(team)

    #Loads JSON data from file -- Will replace this once
    #other endpoints are up
    with open('teamThree.json', 'r') as f:
        teamThree = json.load(f)

    #Adds location to Virginia Beach team and appends
    #each team to original JSON data
    for team in teamThree['standings']:
        team['team'] = '[HBG] ' + team['team']
        dataOne['standings'].append(team)

    #Calls sort once all data is in the same dict/list
    Sort(dataOne['standings'])

    j = 0
    for i in range(0, len(dataOne['standings'])):
        if i > 0:
            if dataOne['standings'][i]['score'] == dataOne['standings'][i-1]['score']:
                dataOne['standings'][i]['pos'] = dataOne['standings'][i-1]['pos']
            else:
                dataOne['standings'][i]['pos'] = i+1
        elif i < 1:
            dataOne['standings'][i]['pos'] = i+1

    ##Re-evaluates the position teams based on the sorted order
    #i = 0
    #for team in dataOne['standings']:
    #    i += 1
    #    team['pos'] = i
    #    #print(team)

    teamData = dataOne['standings']
    return render_template("layout.html", header='CTF Sorted Teams', teams=teamData)

if __name__ == "__main__":
    app.run(debug=True)
