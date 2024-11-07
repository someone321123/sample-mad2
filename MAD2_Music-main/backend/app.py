#IMPORTING ALL NECESSARY PACKAGES FOR FLASK, SQLALCHEMY, ETC=========================================================================================
import os, time, base64, uuid
from flask import Flask, request, jsonify #FLASK PACKAGES & FUNCTIONS
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from sqlalchemy.orm import relationship
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy #FLASK-SQLALCHEMY PACKAGES & FUNCTIONS
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, distinct
from sqlalchemy.orm import relationship, backref
from flask_cors import CORS
from celery import Celery, Task, shared_task


#CREATING FLASK APP AND INITIALISING DATABASE=========================================================================================================
current_directory = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) #APP CREATED
app.config['SECRET_KEY'] = 'XYZ2024' 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(current_directory, 'MAD2DB.sqlite3')
app.config['SECURITY_PASSWORD_SALT'] = 'saltsecurity'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy()
db.init_app(app) #DATABASE INITIALISED
api = Api(app)
CORS(app)
app.app_context().push()
def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object("config")
    return celery_app
celery_app = celery_init_app(app)


#CREATING MODELS FOR DATABASE USING CLASS & DB.MODEL======================================================================================================
class Songs(db.Model):
    __tablename__ = 'songs'
    SID = Column(Integer,primary_key=True, nullable=False, unique=True, autoincrement=True) #Song ID
    Sartist = Column(String) #Song Artist
    Sname = Column(String) #Song Name/Title
    Salb = Column(String) #Song Album
    Sgenre = Column(String)
    Surl = Column(String)

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True,autoincrement=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def get_id(self):
        return str(self.ID)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True) 

class Ratings(db.Model):
    __tablename__='ratings'
    ID = Column(Integer, primary_key=True, autoincrement=True)  # Ratings ID
    Rater = Column(Integer)  # ID of Rater
    Rated = Column(Integer)  # Rating given
    RsongID = Column(String)  # Song ID

class Playlists(db.Model):
    __tablename__ = 'playlists'
    ID = Column(Integer, primary_key=True,autoincrement=True)
    PlaylistName = Column(String, nullable=False)
    Listener = Column(Integer, nullable=False)  # IFD (playlist creator)
    SID = Column(Integer)  # Song IDS in playlist

datastore=SQLAlchemyUserDatastore(db, Users, Role)
app.security = Security(app,datastore)


def calculate_average_rating(ratings):
    if not ratings:
        return 0
    total_ratings = sum([int(rating.Rated) for rating in ratings])
    average_rating = total_ratings / len(ratings)
    return average_rating

def dataurl(dataurl):
        _, data = dataurl.split(",", 1)
        binary_data = base64.b64decode(data)
        unique_id = uuid.uuid4().hex[:6]  
        timestamp = int(time.time())
        filename = f"Song_{timestamp}-{unique_id}.mp3"
        parent = os.path.dirname(current_directory)
        path = os.path.join(parent, "frontend/src/assets/Music", filename)
        with open(path, "wb") as file:
            file.write(binary_data)
        return filename


#CREATING API RESOURCES========================================================================================================================
api = Api(app,prefix='/api')

class SongAPI(Resource):
    def get(self):
        songs=Songs.query.all()
        return songs

    def post(self):
        args = request.get_json()
        print(args['url'], "sachin")
        new_song = Songs(**args)
        db.session.add(new_song)

        db.session.commit()
        return {"message": "Song added successfully"}, 201 

    def delete(self):
        args = request.get_json()
        to_delete = Songs.query.filter_by(**args).first()
        if to_delete:
            db.session.delete(to_delete)
            db.session.commit()
            return {"message": "Song deleted successfully"}
        else:
            return {"message": "Song not found"}, 404 
        
class UserApi(Resource):
    def get(self):
        user=Users.query.all()
        return user

    def post(self):
        args = request.get_json()
        try:
            datastore.create_user(email=args.get("email"),password=args.get("password"),username=args.get("username"))
            db.session.commit()
            role = Role.query.filter_by(name='User').first()
            user = Users.query.filter_by(email=args.get("email")).first()
            datastore.add_role_to_user(user=user,role=role)
            db.session.commit()
            return {"stat": True, "message": "User registered successfully"}, 201 
        except:
            return {"stat": False, "message": "Username already exists"}, 200

    def delete(self):
        args = request.get_json()
        try:
            user=datastore.find_user(username=args.get("username"))
            role=datastore.find_role('User')
            print('USER',user)
            datastore.remove_role_from_user(user, role)
            datastore.delete_user(user)
            db.session.commit()
            return {"message": "User deleted successfully"}
        except:
            return {"message": "User not found"}, 404 
        
api.add_resource(SongAPI,"/songapi")
api.add_resource(UserApi,"/userapi")

#API TO FETCH SPECIFIC DATA============================================================================================================================

@app.post("/login-user")
def login_user_creator():
    args=request.get_json()
    u=args.get("username")
    user=datastore.find_user(username=u)
    if user is None:
        return {"message": "User not found", "stat": False}
    if user.password==args.get("password"):
        return {"token": user.get_auth_token(),
                "username": user.username,
                "id": user.id,
                "role": user.roles[0].name,
                "stat": True}, 200
    else:
        return jsonify({"message": "Invalid Password"}), 401
    
@app.post("/login-admin")
def login_admin():
    args=request.get_json()
    pword=args.get("password")
    adm_token=args.get("adm_token")
    admin=datastore.find_user(username="Admin")
    if admin is None:
        return {"message": "Admin not found", "stat": False}
    if admin.password==pword and adm_token=="TOKEN_FOR_ADMIN":
        return {"token": admin.get_auth_token(),
                "username": admin.username,
                "role": admin.roles[0].name,
                "stat": True}, 200
    else:
        return {"message": "Invalid Password or Token", "stat": False}
    
@app.route('/get-data')
def get_data():
    gen=Songs.query.with_entities(getattr(Songs, "Sgenre")).distinct().all()
    alb=Songs.query.with_entities(getattr(Songs, "Salb")).distinct().all()
    feat=Songs.query.with_entities(getattr(Songs, "Sartist")).distinct().all()
    genre_list=[i[0] for i in gen]
    album_list=[i[0] for i in alb]
    featured_artists=[i[0] for i in feat]
    return jsonify({
        'genre_list': genre_list,
        'album_list': album_list,
        'featured_artists' : featured_artists
    })


@app.route('/search')
def search():
    query = request.args.get('query')
    results = {'song': [], 'genre': [], 'album': [], 'artist': []}
    song_results = Songs.query.filter(Songs.Sname.like(f'%{query}%')).all()
    for song in song_results:
        song_dict = {
            'SID': song.SID,
            'Sname': song.Sname,
            'Sartist': song.Sartist,
            'Salb': song.Salb,
            'Sgenre': song.Sgenre,
            'Surl': song.Surl
        }
        results['song'].append(song_dict)
    genre_results = Songs.query.filter(Songs.Sgenre.like(f'%{query}%')).all()
    for song in genre_results:
        genre_dict = {
            'SID': song.SID,
            'Sname': song.Sname,
            'Sartist': song.Sartist,
            'Salb': song.Salb,
            'Sgenre': song.Sgenre,
            'Surl': song.Surl
        }
        results['genre'].append(genre_dict)
    album_results = Songs.query.filter(Songs.Salb.like(f'%{query}%')).all()
    for song in album_results:
        album_dict = {
            'SID': song.SID,
            'Sname': song.Sname,
            'Sartist': song.Sartist,
            'Salb': song.Salb,
            'Sgenre': song.Sgenre,
            'Surl': song.Surl
        }
        results['album'].append(album_dict)
    artist_results = Songs.query.filter(Songs.Sartist.like(f'%{query}%')).all()
    for song in artist_results:
        artist_dict = {
            'SID': song.SID,
            'Sname': song.Sname,
            'Sartist': song.Sartist,
            'Salb': song.Salb,
            'Sgenre': song.Sgenre,
            'Surl': song.Surl
        }
        results['artist'].append(artist_dict)
    print(results)
    if any(results.values()):
        return jsonify({'results': results})
    else:
        return jsonify({'message': 'No results found'})


@app.post('/rating-songs')
def rate_song():
    args=request.get_json()
    sid=args.get('sid')
    id=args.get('id')
    value=args.get('value')
    existing_rating=Ratings.query.filter_by(Rater=id, RsongID=sid).first()
    if existing_rating:
        existing_rating.Rated=value
    else:
        new_rating=Ratings(Rater=id, RsongID=sid, Rated=value)
        db.session.add(new_rating)
    db.session.commit()
    average_rating=Ratings.query.filter_by(RsongID=sid).with_entities(db.func.avg(Ratings.Rated)).scalar()
    return jsonify({'average_rating': average_rating})

@app.route('/get-songs')
def get_song():
    typ = request.args.get('type')
    arg = request.args.get('arg')
    if typ == "genre":
        gen = Songs.query.filter_by(Sgenre=arg).all()
        genre_data = [{'SID': song.SID, 'Sname': song.Sname, 'Sartist': song.Sartist, 'Salb': song.Salb, 'Sgenre': song.Sgenre,'Surl': song.Surl} for song in gen]
        return jsonify(genre_data)
    elif typ == "album":
        alb = Songs.query.filter_by(Salb=arg).all()
        album_data = [{'SID': song.SID, 'Sname': song.Sname, 'Sartist': song.Sartist, 'Salb': song.Salb, 'Sgenre': song.Sgenre,'Surl': song.Surl} for song in alb]
        return jsonify(album_data)    
    elif typ == "artist":
        art = Songs.query.filter_by(Sartist=arg).all()
        artist_data = [{'SID': song.SID, 'Sname': song.Sname, 'Sartist': song.Sartist, 'Salb': song.Salb, 'Sgenre': song.Sgenre,'Surl': song.Surl} for song in art]
        return jsonify(artist_data)
    elif typ == "all":
        all = Songs.query.all()
        all_data = [{'SID': song.SID, 'Sname': song.Sname, 'Sartist': song.Sartist, 'Salb': song.Salb, 'Sgenre': song.Sgenre,'Surl': song.Surl} for song in all]
        return jsonify(all_data)
    
    
@app.route('/get-favs')
def get_favourites():
    id = request.args.get('id')
    favs = Ratings.query.filter_by(Rated=5,Rater=id).all()
    ids=[song.RsongID for song in favs]
    sgs = Songs.query.filter(Songs.SID.in_(ids)).all()
    favdata = [{'SID': song.SID, 'Sname': song.Sname, 'Sartist': song.Sartist, 'Salb': song.Salb, 'Sgenre': song.Sgenre,'Surl': song.Surl} for song in sgs]
    return jsonify(favdata)

@app.route('/get-plays')
def get_playlists():
    id = request.args.get('id')
    plays = Playlists.query.filter_by(Listener=id).all()
    names = Playlists.query.filter_by(Listener=id).with_entities(distinct(Playlists.PlaylistName)).all()
    lists = [name[0] for name in names]
    playlist_songs = {name: [] for name in lists}
    for playlist in plays:
        playlist_name = playlist.PlaylistName
        playlist_id = playlist.SID
        playlist_songs[playlist_name].append(playlist_id)
    playlist_data = {}
    for playlist_name, playlist_ids in playlist_songs.items():
        sgs = Songs.query.filter(Songs.SID.in_(playlist_ids)).all()
        songs = [{'SID': song.SID, 'Sname': song.Sname, 'Sartist': song.Sartist, 'Salb': song.Salb, 'Sgenre': song.Sgenre,'Surl': song.Surl} for song in sgs]
        playlist_data[playlist_name] = songs
    return jsonify({'playlists': playlist_data})
    
@app.post('/create-playlist')
def create_playlist():
    args=request.get_json()
    uid=args.get('userid')
    plname=args.get('plname')
    sel=args.get('selected')
    for i in sel:
           new_play=Playlists(Listener=uid, SID=i, PlaylistName=plname)
           db.session.add(new_play)
    db.session.commit()
    return jsonify({'message': "Playlist created successfully"}), 201

@app.post('/add-song')
def add_song():
    args=request.get_json()
    name=args.get('name')
    artist=args.get('username')
    album=args.get('album')
    genre=args.get('genre')
    data=args.get('url')
    new=dataurl(data)
    url=new
    song=Songs.query.filter_by(Sname=name).first()
    try:
        if song:
            print(song, 'EXISTS')
            song.Surl=url
            song.Sgenre=genre
            song.Salbum=url
        else:
           new_song=Songs(Sartist=artist, Sname=name, Salb=album, Sgenre=genre, Surl=url)
           db.session.add(new_song)
           print('ADDED')
        db.session.commit()
        return jsonify({'message': "Song added successfully"}), 201
    except:
        return jsonify({'message': "Error adding song"})
    
    
@app.post('/delete-song')
def delete_song():
    id=request.json.get('id')
    to_delete=Songs.query.filter_by(SID=id).first()
    if to_delete is None:
        return {'message': 'Error deleting song'}
    else:
        db.session.delete(to_delete)
        db.session.commit()
        return jsonify({'message': 'Song deleted successfully'})
    

@app.post('/user-upgrade')
def upgrade_to_creator():
    args = request.get_json()
    id = args.get('id')
    user = Users.query.filter_by(id=id).first()
    if user:
        creator_role = Role.query.filter_by(name='Creator').first()
        if creator_role:
            role=datastore.find_role('User')
            datastore.remove_role_from_user(user, role)
            datastore.add_role_to_user(user, creator_role)
            db.session.commit()
            return {'message': 'User upgraded to creator successfully'}, 201
    else:
        return {'error': 'User not found'}, 404

import matplotlib.pyplot as plt

@app.route('/admin-stats')   
def admin_appstats():
    user_users = Users.query.join(RolesUsers).join(Role).filter(Role.name == 'User').all()
    num_user_users = len(user_users)
    creator_users = Users.query.join(RolesUsers).join(Role).filter(Role.name == 'Creator').all()
    num_creator_users = len(creator_users)
    num_songs = Songs.query.count()
    gen = Songs.query.with_entities(getattr(Songs, "Sgenre")).distinct().all()
    alb = Songs.query.with_entities(getattr(Songs, "Salb")).distinct().all()
    feat = Songs.query.with_entities(getattr(Songs, "Sartist")).distinct().all()
    genlen = len([i[0] for i in gen])
    alblen = len([i[0] for i in alb])
    artlen = len([i[0] for i in feat])
    sn = Songs.query.all()
    ratings_dict = {}
    for song in sn:
        ratings = Ratings.query.filter_by(RsongID=song.SID).all()
        average_rating = calculate_average_rating(ratings)
        ratings_dict[song.SID] = {
            'average_rating': average_rating
        }
    highest_rated_songs = []
    for song_id, song_info in ratings_dict.items():
        if song_info['average_rating'] >= 4:
            song = next((song for song in sn if song.SID == song_id), None)
            if song:
                highest_rated_songs.append({
                    'SID': song_id,
                    'Sname': song.Sname,
                    'Sartist': song.Sartist,
                    'Surl': song.Surl,
                    'average_rating': song_info['average_rating']
                })
    results = {
        'us': num_user_users,
        'cr': num_creator_users,
        'sgs': num_songs,
        "highest_rated_songs": highest_rated_songs,
        "genlen": genlen, 
        "alblen": alblen,
        "artlen": artlen,
    }
    return jsonify(results)

#CELERY TASKS=======================================================================================================================================

@celery_app.task(ignore_result=False)
def sayhello():
    return "HELLO THERE"

@app.get('/sayhello')
def sayhello_view():
    print('IN ROUTER')
    t = sayhello.delay()
    result = t.wait()
    return {"task_id": t.id}

if __name__=="__main__":
    app.run(debug=True)