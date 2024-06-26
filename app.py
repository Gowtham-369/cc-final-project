import json
import mysql.connector
import os
import pandas as pd
import shutil
from decimal import *
from flask import Flask, request, render_template
from mysql.connector import errorcode
from static.constants.file_paths import WebAppConstants
from static.constants.app_configurations import AppConfigValues as cf
from static.constants.app_configurations import Queries 
from static.constants.app_configurations import DataBaseConfigValues as dbconf
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config.from_object(__name__) #  loads configuration settings from the Python module identified by __name__

app.config[cf.HOUSEHOLD_FOLDER]=WebAppConstants.HOUSEHOLD_UPLOAD_FILE_PATH;
app.config[cf.TRANSACTIONS_FOLDER]=WebAppConstants.TRANSACTIONS_UPLOAD_FILE_PATH
app.config[cf.PRODUCTS_FOLDER]=WebAppConstants.PRODUCTS_UPLOAD_FILE_PATH;


def initialize():
    if not os.path.exists(app.config[cf.HOUSEHOLD_FOLDER]):
        os.makedirs(app.config[cf.HOUSEHOLD_FOLDER],0o777)
    else:
        shutil.rmtree(app.config[cf.HOUSEHOLD_FOLDER])
        os.makedirs(app.config[cf.HOUSEHOLD_FOLDER],0o777)

    if not os.path.exists(app.config[cf.TRANSACTIONS_FOLDER]):
        os.makedirs(app.config[cf.TRANSACTIONS_FOLDER],0o777)
    else:
        shutil.rmtree(app.config[cf.TRANSACTIONS_FOLDER])
        os.makedirs(app.config[cf.TRANSACTIONS_FOLDER],0o777)

    if not os.path.exists(app.config[cf.PRODUCTS_FOLDER]):
        os.makedirs(app.config[cf.PRODUCTS_FOLDER],0o777)
    else:
        shutil.rmtree(app.config[cf.PRODUCTS_FOLDER])
        os.makedirs(app.config[cf.PRODUCTS_FOLDER],0o777)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
       
        if isinstance(obj, Decimal):
            return str(obj)
            
        return json.JSONEncoder.default(self, obj)


def check_file_extension(filename):
    return filename.split('.')[-1] in cf.ALLOWED_EXTENSIONS

@app.route("/")
def welcome():
    return render_template('login.html')


@app.route('/login', methods =['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST' and str(request.form['username']) !="" and str(request.form['password']) != "":
        username = str(request.form['username'])
        password = str(request.form['password'])
        # print("username", username)
        # print("password", password)
        
        result = execute_select_query(Queries.LOGIN_SELECT_QUERY.format(username,password))
        if (result.shape[0] != 0):
            print("Log In Successfull")
            return render_template('home-page.html', message=message)
        else:
            message = 'Invalid Credentials !'
        
    elif request.method == 'POST':
        message = 'Please Enter Credentials'
    return render_template('login.html', message=message)


@app.route('/dashboard', methods =['GET','POST'])
def dashboard():
    return render_template('home-page.html')


@app.route('/upload-datasets', methods =['GET','POST'])
def upload_datasets():
    return render_template('upload-data.html')


@app.route('/registration', methods =['GET','POST'])
def registration():
    message = ''
    conn = connect_to_database()
    cursor = conn.cursor()
    
    if request.method == 'POST' and str(request.form['username']) !="" and str(request.form['password']) !="" and str(request.form['firstname']) !="" and str(request.form['lastname']) !="" and str(request.form['email']) !="":
        username = str(request.form['username'])
        password = str(request.form['password'])
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        email = str(request.form['email'])
        
        result = execute_select_query(Queries.IS_REGISTERED_SELECT_QUERY.format(username))
        if (result.shape[0] != 0):
            message = 'User already exists with the same username. Please try with a different name'
        else:
            result1 = cursor.execute(Queries.REGISTRATION_INSERT_QUERY, (username, password, firstname, lastname, email))
            conn.commit()
            cursor.close()
            conn.close()
            result2 = execute_select_query(Queries.IS_IN_DATABASE_SELECT_QUERY.format(username, password))
            if (result2.shape[0] != 0):
                message = 'User Registration Done Successfully! Click on Sign In to continue to Login'
                return render_template('registration-success.html', message=message)
    elif request.method == 'POST':
        message = 'Some of the required fields are missing!!'
    
    return render_template('registration.html', message=message)


@app.route('/search-hhm', methods =['GET', 'POST'])
def search_hhm():
    # return render_template('search-hhm.html')
    return load_table("10")


@app.route('/search-hhm-new', methods =['GET','POST'])
def search_hhm_new():
    if request.method == 'POST' and str(request.form['hshd_num']) != "":
        try:
            response = load_table(str(request.form['hshd_num']));
        except:
            message = "Valid HSHD_NUM is required!!"
            return render_template('search-hhm.html', message=message)
    else:
        message = "Valid HSHD_NUM is required!!"
        return render_template('search-hhm.html',message=message)
    return response;


@app.route('/store-uploaded-household-file', methods =['GET','POST'])
def store_uploaded_household_file():
    message = 'Please upload file again!'
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  
        if check_file_extension(f.filename):
            f.save(os.path.join(app.config[cf.HOUSEHOLD_FOLDER],secure_filename(f.filename)))  # this will secure the file
            read_csv_and_load_data(os.path.join(app.config[cf.HOUSEHOLD_FOLDER], secure_filename(f.filename)),"households");
            message='file upload successfull'  # Display this message after uploading
        else:
            message='file extension is not allowed'

    return render_template('upload-data.html',message=message)


@app.route('/store-uploaded-product-file', methods =['GET','POST'])
def store_uploaded_product_file():
    message = 'Please upload file again!'
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  
        if check_file_extension(f.filename):
            f.save(os.path.join(app.config[cf.PRODUCTS_FOLDER],secure_filename(f.filename)))  # this will secure the file
            read_csv_and_load_data(os.path.join(app.config[cf.PRODUCTS_FOLDER], secure_filename(f.filename)),"products");
            message='file upload successfull'  # Display this message after uploading
        else:
            message='file extension is not allowed'

    return render_template('upload-data.html',messageProducts=message)


@app.route('/store-uploaded-transaction-file', methods =['GET','POST'])
def store_uploaded_transaction_file():
    message = 'Please upload file again!'
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  # get the file from the files object
        # Saving he file in the required destination
        if check_file_extension(f.filename):
            f.save(os.path.join(app.config[cf.TRANSACTIONS_FOLDER], secure_filename(f.filename)))  # this will secure the file
            read_csv_and_load_data(os.path.join(app.config[cf.TRANSACTIONS_FOLDER], secure_filename(f.filename)),"transactions");
            message='file upload successfull'  # Display this message after uploading
        else:
            message='file extension is not allowed'

    return render_template('upload-data.html',messageTransactions=message)


def execute_select_query(queryString):
    conn = connect_to_database()
    return pd.read_sql(queryString,conn)


def load_table(hshd_num):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(Queries.LOAD_JOINED_TABLE_QUERY.format(hshd_num));
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('search-hhm-table.html',data=rows)


def connect_to_database():
    config = {
    'host': dbconf.HOST_NAME,
    'user': dbconf.USER_NAME,
    'password': dbconf.PASSWORD,
    'database': dbconf.DATABASE_NAME
    }
    # port : 3306
    try:
        conn = mysql.connector.connect(**config)
        print("Database Connection Successfull")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return conn


def read_csv_and_load_data(csvfilepath,dataFrom):
    conn = connect_to_database()
    cursor = conn.cursor()
    df = pd.read_csv(csvfilepath)
    df.columns = df.columns.str.replace(' ', '')
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    dftotuple = list(df.to_records(index=False))
    if(dataFrom == 'households'):
        for eachtuple in dftotuple:
            try:
                cursor.execute(
                    Queries.HOUSEHOLD_TABLE_INSERT_QUERY,
                    (int(eachtuple.HSHD_NUM), str(eachtuple.L), str(eachtuple.AGE_RANGE), str(eachtuple.MARITAL),
                     str(eachtuple.INCOME_RANGE), str(eachtuple.HOMEOWNER), str(eachtuple.HSHD_COMPOSITION),
                     str(eachtuple.HH_SIZE), str(eachtuple.CHILDREN)));
            except Exception as e:  # works on python 3.x
                print('Failed to upload to ftp: ' + str(e))
    if (dataFrom == 'transactions'):
        for eachtuple in dftotuple:
            try:
                cursor.execute(
                    Queries.TRANSACTIONS_TABLE_INSERT_QUERY,
                    (int(eachtuple.BASKET_NUM), int(eachtuple.HSHD_NUM), str(eachtuple.PURCHASE_),
                     int(eachtuple.PRODUCT_NUM), int(eachtuple.SPEND), int(eachtuple.UNITS), str(eachtuple.STORE_R),
                     int(eachtuple.WEEK_NUM), int(eachtuple.YEAR)));
            except Exception as e:  # works on python 3.x
                print('Failed to upload to ftp: ' + str(e))
    if (dataFrom == 'products'):
        for eachtuple in dftotuple:
            try:
                cursor.execute(
                    Queries.PRODUCTS_TABLE_INSERT_QUERY,
                    (int(eachtuple.PRODUCT_NUM), str(eachtuple.DEPARTMENT), str(eachtuple.COMMODITY),str(eachtuple.BRAND_TY),
                     str(eachtuple.NATURAL_ORGANIC_FLAG)));
            except Exception as e:  # works on python 3.x
                print('Failed to upload to ftp: ' + str(e))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/load-dashboard', methods =['GET','POST'])
def load_dashboard():
    #First Graph(bar Graph)
    first_data = execute_select_query(Queries.FIRST_PLOT_DASHBOARD_QUERY);
    first_data['Spent']=first_data['Spent'].astype(str);
    first_data['household_Size'] = first_data['household_Size'].astype(str);

    #Second Graph(Bar Graph)
    second_data = execute_select_query(
        Queries.SECOND_PLOT_DASHBOARD_FOOD_QUERY);
    second_data['spend'] = second_data['spend'].astype(str);
    second_data['householdsize'] = second_data['householdsize'].astype(str);

    second_dataTwo = execute_select_query(
        Queries.SECOND_PLOT_DASHBOARD_NON_FOOD_QUERY);
    second_dataTwo['spend'] = second_dataTwo['spend'].astype(str);

    #Third Graph(Bar Graph)
    third_data = execute_select_query(
        Queries.THIRD_PLOT_DASHBOARD_QUERY);
    third_data['spend'] = third_data['spend'].astype(str);
    third_data['commodity'] = third_data['commodity'].astype(str);

    #Fourth Graph(Line Graph)
    fourth_data = execute_select_query(
        Queries.FOURTH_PLOT_DASHBOARD_QUERY);
    fourth_data['spend'] = fourth_data['spend'].astype(str);
    fourth_data['year'] = fourth_data['year'].astype(str);

    return render_template("dashboard.html",title='Household Size vs Spend', max=17000,titletwo="Household Size vs Spend Grouped By Product Type",
                           labels=first_data['household_Size'].values.tolist(), values=first_data['Spent'].values.tolist(),
                           labelstwo=second_data['householdsize'].values.tolist(),valuestwo=second_data['spend'].values.tolist(),
                           valuestwotwo=second_dataTwo['spend'].values.tolist(),
                           titlethree="Different Food Items vs Spend",
                           labelsthree=third_data['commodity'].values.tolist(),
                           valuesthree=third_data['spend'].values.tolist(),
                           titlefour="Year vs Spend",
                           labelsfour=fourth_data['year'].values.tolist(),
                           valuesfour=fourth_data['spend'].values.tolist());


initialize()

if __name__ == '__main__':
    app.run()