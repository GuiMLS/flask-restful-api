from flask_restful import Resource

roles = ['DB Analyst', "Frontend", "Backend", "FullStack", "DevOps", "SysAdmin",
         "Cloud Engineer", "Data Analyst", "Data Scientist", "Data Engineer"]
class Roles(Resource):
    def get(self):
        return roles