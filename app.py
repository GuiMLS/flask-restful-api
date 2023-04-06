from flask import Flask, request
from flask_restful import Resource, Api
from models import Apps, Messages, Users
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)
NO_RIGHTS_RESPONSE = "You do not have the necessary rights to do this task. Please, log on as an administrator!"


@auth.verify_password
def verifying_login(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password).first()


class ManageUsers(Resource):
    @auth.login_required
    def get(self):  # SHOW ALL USERS
        user = auth.current_user()  #  Get current user details
        if user.role == 'admin':  # Check if user role is admin
            users = Users.query.all()
            response = [{'id': i.id, 'login': i.login, 'role': i.role} for i in users]
        else:
            response = NO_RIGHTS_RESPONSE
        return response

    @auth.login_required
    def post(self):  # ADD USER
        user = auth.current_user()  # Get current user details
        if user.role == 'admin': # Check if user role is admin
            data = request.json
            try:
                new_user = Users(login=data['login'], password=data['password'], role=data['role'])
                new_user.save()
                response = {
                    'id': new_user.id,
                    'login': new_user.login,
                    'password': new_user.password,
                    'role': new_user.role
                }
            except KeyError as e:
                response = "The {} field may be missing or poorly written. Please, correct the parameters.".format(
                    str(e))
            except:
                response = "The login {} is in use. Please, choose another one.".format(data['login'])
        else:
            response = NO_RIGHTS_RESPONSE
        return response

    @auth.login_required
    def delete(self):  # DELETE SPECIFIC USER
        user = auth.current_user()  # Get current user details
        data = request.json  # Get the data from body in JSON format
        try:
            name = data['name']
            if user.role == 'admin' or name == user.login:  # Check if user role is admin or if it is the user itself
                user = Users.query.filter_by(login=name).first()
                if user:
                    response = 'The user {} was successfully deleted.'.format(name)
                    user.delete()
                else:
                    response = "The user {} does not exist!".format(name)
            else:
                response = NO_RIGHTS_RESPONSE
        except KeyError as e:
            response = "The {} field may be missing or poorly written. Please, correct the parameters.".format(str(e))
        return response


class ManageApps(Resource):
    @auth.login_required
    def get(self):  # SELECT ALL APPS
        user = auth.current_user()  # Get current user details
        if (
                user.role == 'admin'):
            apps = Apps.query.all()
            response = [{'id': i.id, 'name': i.name, 'context': i.context} for i in apps]
        else:
            response = NO_RIGHTS_RESPONSE
        return response

    @auth.login_required
    def post(self):  # CREATE AN APP
        user = auth.current_user()  # Get current user details
        if user.role == 'admin':
            data = request.json  # Get the data from body in JSON format
            user_exists = Users.query.filter_by(login=data['context']).first()
            if user_exists:
                try:
                    existing_app_context = Apps.query.filter_by(context=data['context']).first()
                    if existing_app_context:
                        response = "The user {} is already assigned to an app!".format(data['context'])
                    else:
                        app = Apps(name=data['name'], context=data['context'])
                        app.save()
                        response = {
                            'id': app.id,
                            'name': app.name,
                            'context': app.context  # assign to a user
                        }
                except KeyError as e:
                    response = "The {} field may be missing or poorly written. Please, correct the parameters.".format(
                        str(e))
                except:
                    response = "The app name {} is in use, please choose another one.".format(data['name'])
            else:
                response = "The user {} does not exist!".format(data['context'])
        else:
            response = NO_RIGHTS_RESPONSE
        return response


class SpecificApp(Resource):
    @auth.login_required
    def get(self, name):  # SELECT SPECIFIC APP
        user = auth.current_user()  # Get current user details
        if user.role == 'admin':
            app_filtered = Apps.query.filter_by(name=name).first()
            try:
                response = {
                    'name': app_filtered.name,
                    'context': app_filtered.context,
                    'id': app_filtered.id
                }
            except AttributeError:
                response = "The App {} was not found.".format(name)
        else:
            response = NO_RIGHTS_RESPONSE
        return response


class ManageMessages(Resource):
    @auth.login_required
    def get(self):  # SHOW MESSAGES
        user = auth.current_user()  # Get current user details
        if user.role == 'admin': # Check if the user have an admin role
            messages = Messages.query.all() # Select all the messages in the database
            response = [{'id': i.id, 'content': i.content, 'from': i.from_user, 'to': i.to_user} for i in
                        messages]  # Show all Messages
        elif user.role == 'user':
            messages_from_user = [{'id': i.id, 'content': i.content, "from": i.from_user, "to": i.to_user} for i in
                                  Messages.query.filter_by(
                                      from_user=user.login)]  # Filter only the messages sent by the user
            messages_to_user = [{'id': i.id, 'content': i.content, "from": i.from_user, "to": i.to_user} for i in
                                Messages.query.filter_by(to_user=user.login)]  # Filter only the messages sent to the user
            messages_all = messages_from_user + messages_to_user  #  Merge the messages
            response = messages_all
        else:
            response = NO_RIGHTS_RESPONSE
        return response

    @auth.login_required
    def post(self):  # ADD MESSAGE
        user = auth.current_user()  # Get current user details
        if user.role == 'user': # Check if the user role is user
            data = request.json #  Get the data from body in JSON format
            to_user = data['to_user']
            user_filtered = Users.query.filter_by(login=to_user).first()
            if user_filtered:
                app = Apps.query.filter_by(context=user.login).first() # Get the app from which the user belongs to
                message = Messages(content=data['content'], app=app, from_user=user.login, to_user=to_user)
                message.save()
                response = "The message was successfully saved!"
            else:
                response = 'The user {} does not exist!'.format(to_user)
        else:
            response = 'You should log in as a user role to send someone a message!'
        return response

    @auth.login_required
    def delete(self):  # DELETE SPECIFIC MESSAGE
        user = auth.current_user()  #  Get the user details
        data = request.json  #  Get the data from body in JSON format
        if user.role == 'admin': #  Check if the current user has an admin role
            try:
                id_data = data['id']
                message_filtered = Messages.query.filter_by(id=id_data).first() # Looks for the message to be deleted filtering it by its ID
                response = 'The Message: {} was successfully deleted'.format(message_filtered.content)
                message_filtered.delete()
            except AttributeError:
                response = 'The id {} has no related messages.'.format(data['id'])
            except KeyError as e:
                response = "The {} field may be missing or poorly written. Please, correct the parameters.".format(
                    str(e))
        else:
            response = NO_RIGHTS_RESPONSE
        return response


#  DESIGNED ROUTES

api.add_resource(SpecificApp, '/app/<string:name>/')  # Specific app's services: GET
api.add_resource(ManageApps, '/app/')  # Lists all existing apps (GET) and Adds new Apps (POST)
api.add_resource(ManageMessages, '/messages/')  # List all messages (GET) and Adds messages (POST)
api.add_resource(ManageUsers, '/users/')  # Lists all Users (GET), Adds new Users (POST) and Delete existing ones (DELETE)

if __name__ == '__main__':
    app.run(debug=False)
