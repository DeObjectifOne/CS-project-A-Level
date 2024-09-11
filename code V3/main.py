from website import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

#used to run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)