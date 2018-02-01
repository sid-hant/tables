# importing libraries to use
from flask import Flask, render_template, request, session, make_response, redirect
from src.common.database import Database
from src.models.player import Player
from src.models.points import Points
from src.models.room import Room
from src.models.player_all import Player_All


# initializing the flask app
app = Flask(__name__)

# secret key
app.secret_key = 'sid'


# initializing the database
@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home_temp():
    if request.method == 'POST':
        if session['_id'] is None:
            return render_template('login.html')
        else:
            return redirect('/dashboard')
    else:
        if session['_id'] is None:
            return render_template('login.html')
        else:
            return redirect('/dashboard')


@app.route('/login')
def login_p():
    if request.method == 'POST':
        if session['_id'] is None:
            return render_template('login.html')
        else:
            return redirect('/dashboard')
    else:
        if session['_id'] is None:
            return render_template('login.html')
        else:
            return redirect('/dashboard')


@app.route('/register')
def register_redirect():
    if request.method == 'POST':
        if session['_id'] is None:
            return render_template('register.html')
        else:
            return redirect('/dashboard')
    else:
        if session['_id'] is None:
            return render_template('register.html')
        else:
            return redirect('/dashboard')


@app.route('/auth/register', methods=['POST', 'GET'])
def register_room():
    password = request.form['password']
    password_2 = request.form['confirm_password']
    name = request.form['name']
    if len(password) >= 8 and len(name) < 20 and password == password_2:
        room = Room(password, name)
        room.save_to_mongo()
        session['_id'] = room._id
        point = Points(room._id, 3, 1)
        point.save_to_mongo()
        return redirect('/dashboard')
    else:
        session['_id'] = None
        return render_template('registeration-failed.html')


@app.route('/delete-room', methods=['POST', 'GET'])
def delete_room():
    password = request.form['password']
    password_2 = request.form['confirm_password']
    room = Room.find_by_id(session['_id'])
    if password == room.password and password_2 == room.password:
        room.remove_room()
        session['_id'] = None
        return redirect('/')
    else:
        return redirect('/dashboard-error')


@app.route('/auth/login', methods=['POST', 'GET'])
def login_room():
    room_id = request.form['room_id']
    password = request.form['password']
    if Room.login_valid(room_id, password):
        Room.login(room_id)
        return redirect('/dashboard')
    else:
        session['_id'] = None
        return render_template('login-failed.html')


@app.route('/dashboard', methods=['GET','POST'])
def dashboard_template():
    if session['_id'] is None:
        return redirect('/login')
    else:
        room = Room.find_by_id(session['_id'])
        matches = room.get_matches()
        room = Room.find_by_id(session['_id'])
        players = room.get_players()
        top_five_matches = []
        for match in matches:
            top_five_matches.append(match)
            if len(top_five_matches) == 5:
                break
        return render_template('dashboard.html', room_id=session['_id'], matches=top_five_matches,
                               players=players, room_name=room.name.upper())


@app.route('/dashboard-error', methods=['GET','POST'])
def dashboard_error_template():
    if session['_id'] is None:
        return redirect('/login')
    else:
        room = Room.find_by_id(session['_id'])
        matches = room.get_matches()
        room = Room.find_by_id(session['_id'])
        players = room.get_players()
        top_five_matches = []
        for match in matches:
            top_five_matches.append(match)
            if len(top_five_matches) == 5:
                break
        return render_template('dashboard-failed.html', room_id=session['_id'], matches=top_five_matches,
                               players=players, room_name=room.name.upper())


@app.route('/players/add', methods=['GET', 'POST'])
def create_new_player():
    if request.method == 'GET':
        return redirect('/dashboard')
    else:
        name = request.form['player_name']
        password = request.form['password']
        _id = session['_id']
        name = name.upper()
        room = Room.find_by_id(_id)
        if room.password == password and name is not None:
            room.new_player(name, _id)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard-error')

@app.route('/end-season', methods=['GET', 'POST'])
def end_season():
    if request.method == 'GET':
        return redirect('/dashboard')
    else:
        password = request.form['password']
        _id = session['_id']
        room = Room.find_by_id(_id)
        if room.password == password:
            room.end_season()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard-error')


@app.route('/setting/points', methods=['GET','POST'])
def change_points():
    if request.method == 'GET':
        return make_response(dashboard_template)
    else:
        ppw = request.form['ppw']
        ppd = request.form['ppd']
        password = request.form['password']
        _id = session['_id']
        room = Room.find_by_id(_id)
        if room.password == password and ppw is not None and ppd is not None:
            points = Points.get_points(_id)
            points.ppd = ppd
            points.ppw = ppw
            points.update_mongo()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard-error')


@app.route('/players/remove', methods=['GET', 'POST'])
def remove_player():
    if request.method == 'GET':
        return redirect('/dashboard')
    else:
        name = request.form['player_name']
        password = request.form['password']
        _id = session['_id']
        room = Room.find_by_id(_id)
        if room.password == password and name is not None:
            player = Player.find_by_name(name)
            player.remove_from_mongo()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard-error')

@app.route('/stats', methods=['GET', 'POST'])
def stat():
    if request.method == 'GET':
        return redirect('/dashboard')
    else:
        name = request.form['player_name']
        _id = session['_id']
        room = Room.find_by_id(_id)
        player = Player.find_by_name(name)
        playerAll = Player_All.find_by_name(name)
        current_rate = ((player.wins / player.games_played) * 100)
        ovr_rate = ((playerAll.wins / playerAll.games_played) * 100)
        matches = room.get_matches()
        player_match = []
        for match in matches:
            if match.p1 == player.name or match.p2 == player.name and name is not None:
                player_match.append(match)
        return render_template('stat.html', player=player, matches=player_match, playerAll=playerAll, current_rate=current_rate, ovr_rate=ovr_rate)


@app.route('/matches/add', methods=['GET', 'POST'])
def match_add():
    if request.method == 'GET':
        return redirect('/dashboard')
    else:
        p1 = request.form['p1']
        p2 = request.form['p2']
        p1score = request.form['p1score']
        p2score = request.form['p2score']
        password = request.form['password']
        _id = session['_id']
        room = Room.find_by_id(_id)
        if room.password == password and p1 is not None and p2 is not None and p1 != p2:
            room.new_match(p1,p2,p1score,p2score,_id)
            room.update_table(p1,p2,p1score,p2score)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard-error')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['_id'] = None

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

