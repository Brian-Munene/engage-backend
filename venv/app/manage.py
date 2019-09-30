from flask_migrate import Migrate, MigrateCommand
from database import company
from database import survey
from database import  survey_response
from database import user

from flask_script import Manager

from routes import db, app

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
