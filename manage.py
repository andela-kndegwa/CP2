from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db, api
from app.blister_api.models import User
from app.blister_api.endpoints.bucket_lists import ns as bucket_list_namespace
from app.blister_api.endpoints.items import ns as items_namespace
from app.blister_api.endpoints.register_user import ns as register_namespace
from app.blister_api.endpoints.login_user import ns as login_namespace

# create the app
app = create_app('development')

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
    api.add_namespace(bucket_list_namespace)
    api.add_namespace(items_namespace)
    api.add_namespace(register_namespace)
    api.add_namespace(login_namespace)
    manager.run()
