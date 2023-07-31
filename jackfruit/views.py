from urllib import response

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pymysql


class Register(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        response = Mysqlconnection.getProcData('register_password',[username,password,email])
        return Response(response, status=status.HTTP_200_OK)

class managdata(APIView):
    def post(self, request):
        data = request.data
        oper = data.get('oper')
        id = data.get('id')
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        country = data.get('country')
        responce = Mysqlconnection.getProcData('manage_data',[id,country,name,age,gender,oper])
        return Response(responce, status=status.HTTP_200_OK)

class deleteData(APIView):
    def post(self, request):
        data = request.data
        oper = data.get('oper')
        id = data.get('id')
        name = data.get('name','')
        age = data.get('age','')
        gender = data.get('gender','')
        country = data.get('country','')
        responce = Mysqlconnection.getProcData('manage_data',[id,country,name,age,gender,oper])
        return Response(responce, status=status.HTTP_200_OK)

class getdata(APIView):
    def get(self, request):
        requestObj = request.GET.dict()
        oper = requestObj.get('oper','GET')
        response = Mysqlconnection.getProcData("get_data", [oper])
        return Response(response, status=status.HTTP_200_OK)


class update(APIView):
    def post(self,request):
        data=request.data
        email = data.get('email')
        password = data.get('password')
        responce = Mysqlconnection.getProcData('update_password',[email,password])
        return Response(responce, status=status.HTTP_200_OK)

class login(APIView):
    def post(self,request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        responce = Mysqlconnection.getProcData('login',[username,password])
        print(responce)
        # if response['RESULT_CODE'] == "1":
        #     request.session["SESSION_ID"] = response['SESSIONID']
        return Response(responce, status=status.HTTP_200_OK)


class Mysqlconnection():
    def getProcData(procname, params):
        connection = pymysql.connect(host='127.0.0.1',port=3306, user='root',password='imman9965@', db='imman',cursorclass=pymysql.cursors.DictCursor)
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
            response = {'RESULT_CODE':0,'RESULT_MESSAGE':'Something went wrong.. try after sometime..'}
            return response
        finally:
            connection.close()