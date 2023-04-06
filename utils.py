from models import Apps, Users

# Insere dados na tabela app
def insert_apps(name, context):
    try:
        app = Apps(name=name, context=context)
        app.save()
    except:
        print("App already exists!")

# Realiza consulta na tabela app
def show_apps():
    apps = Apps.query.all()
    print(apps)
    app = Apps.query.filter_by(name='Rafael').first()
    print(app.context)

# Altera dados na tabela app
def alter_app():
    app = Apps.query.filter_by(name='Galleani').first()
    app.name = 'Felipe'
    app.save()

# Exclui dados na tabela app
def delete_app():
    app = Apps.query.filter_by(name='Felipe').first()
    app.delete()

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
    #show_all_users()
    insert_apps('App1', 'user1')
    insert_apps('App2', 'user2')
    #alter_app()
    #delete_app()
    #show_apps()

