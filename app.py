from flask import Flask, render_template, request
from planner import Planner

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    resorts = None
    if request.method == "POST":
        city = request.form.get("city")
        state = request.form.get("state")
        range = request.form.get("range")
        if city and state:
            planner = Planner(city, state)
            resorts = planner.get_mountains(range)
        else:
            resorts = "Must enter a city and a state"
    return render_template("home.html", resorts=resorts)

if __name__=="__main__":
    app.run(debug=True)