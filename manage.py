from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
# application=specific imports
from app import db
from app.database.models import User
from app.blister import app

# create instances of the Manager and Migrate classes.
manager = Manager(app)
migrate = Migrate(app, db)

# Allows one to be able to access the User model right
# from python manag.py shell as a function on manager.
# add.command.


def make_shell_context():
    return dict(User=User)

# Allows us to make migrations using the db command
# Allows use to access shell as above.


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
