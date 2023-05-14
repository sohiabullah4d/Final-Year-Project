from flask import Flask

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db' : 'FYPDatabase.db',
    'host': 'mongodb://localhost:27017/FYPDatabase'
}

app.config['SECRET_KEY'] = '99d5a8a07ee30c0074b6b3ccfcaf9116'



from JournalRecommendationSystem import routes