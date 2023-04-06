from models import Apps, Users

def insert_apps(name, context):
    try:
        app = Apps(name=name, context=context)
        app.save()
    except:
        print("App already exists!")

def insert_user(login, password, role):
    try:
        users = Users(login=login, password=password, role=role)
        users.save()
    except:
        print("User already exists!")


def show_all_users():
    users = Users.query.all()
    print(users)

if __name__ == '__main__':
    insert_user('admin1', '1234', 'admin')
    insert_user('user1', '1234', 'user')
    insert_user('user2', '1234', 'user')
    insert_apps('App1', 'user1')
    insert_apps('App2', 'user2')

