import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

app = create_app('development')

migrate = Migrate(app, db)
manager = Manager(app)

# added the db command to the manager 
# so that we can run the migrations from the command line
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
