from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pymysql
import uuid

class Mysqlconnection:
    @staticmethod
    def getProcData(procname, params):
        connection = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', password='ROOT',
            db='powertable', cursorclass=pymysql.cursors.DictCursor
        )
        try:
            response = {}
            record = []
            cursor = connection.cursor()
            cursor.callproc(procname, params)
            result = cursor.fetchall()
            for row in result:
                record.append(row)  
            connection.commit()
            cursor.close()
            response = record
            return response
        except Exception as e:
            response = {'RESULT_CODE': 0, 'RESULT_MESSAGE': 'Something went wrong.. try after sometime..'}
            return response
        finally:
            connection.close()

class Login(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        response = Mysqlconnection.getProcData('login', [username, password])
        
        # Check if login was successful
        if response and response[0].get('RESULT_CODE') == "1":
            # Generate a session ID and store it in the session
            session_id = str(uuid.uuid4())
            request.session["SESSION_ID"] = session_id
            response[0]['SESSION_ID'] = session_id  # Send session ID back to client
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)

def is_authenticated(request):
    session_id = request.session.get("SESSION_ID")
    return bool(session_id)

class Register(APIView):
    def post(self, request):
        if not is_authenticated(request):
            return Response({'RESULT_CODE': 0, 'RESULT_MESSAGE': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        response = Mysqlconnection.getProcData('register_password', [username, password, email])
        return Response(response, status=status.HTTP_200_OK)

class ManageData(APIView):
    def post(self, request):
        if not is_authenticated(request):
            return Response({'RESULT_CODE': 0, 'RESULT_MESSAGE': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        oper = data.get('oper')
        id = data.get('id')
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        country = data.get('country')
        response = Mysqlconnection.getProcData('manage_data', [id, country, name, age, gender, oper])
        return Response(response, status=status.HTTP_200_OK)

class DeleteData(APIView):
    def post(self, request):
        if not is_authenticated(request):
            return Response({'RESULT_CODE': 0, 'RESULT_MESSAGE': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        oper = data.get('oper')
        id = data.get('id')
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')
        country = data.get('country', '')
        response = Mysqlconnection.getProcData('manage_data', [id, country, name, age, gender, oper])
        return Response(response, status=status.HTTP_200_OK)

class GetData(APIView):
    def get(self, request):
        if not is_authenticated(request):
            return Response({'RESULT_CODE': 0, 'RESULT_MESSAGE': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        request_obj = request.GET.dict()
        oper = request_obj.get('oper', 'GET')
        response = Mysqlconnection.getProcData("get_data", [oper])
        return Response(response, status=status.HTTP_200_OK)

class Update(APIView):
    def post(self, request):
        if not is_authenticated(request):
            return Response({'RESULT_CODE': 0, 'RESULT_MESSAGE': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        email = data.get('email')
        password = data.get('password')
        response = Mysqlconnection.getProcData('update_password', [email, password])
        return Response(response, status=status.HTTP_200_OK)
