import sqlite3
import mysql.connector
import pandas as pd
import shutil
import json
import os
from mysql.connector import errorcode
from flask import Flask, request, g, render_template, send_file
from werkzeug.utils import secure_filename
from decimal import *

DATABASE = '/tmp/db.example'

app = Flask(__name__)
app.config.from_object(__name__) #  loads configuration settings from the Python module identified by __name__

app.config['Upload_folder_HouseHolds']="/tmp/static/UploadFiles/Households";
app.config['Upload_folder_Transactions']="/tmp/static/UploadFiles/Transactions";
app.config['Upload_folder_Products']="/tmp/static/UploadFiles/Products";


if not os.path.exists(app.config['Upload_folder_HouseHolds']):
   os.makedirs(app.config['Upload_folder_HouseHolds'],0o777)
else:
   shutil.rmtree(app.config['Upload_folder_HouseHolds'])
   os.makedirs(app.config['Upload_folder_HouseHolds'],0o777)

if not os.path.exists(app.config['Upload_folder_Transactions']):
   os.makedirs(app.config['Upload_folder_Transactions'],0o777)
else:
    shutil.rmtree(app.config['Upload_folder_Transactions'])
    os.makedirs(app.config['Upload_folder_Transactions'],0o777)


if not os.path.exists(app.config['Upload_folder_Products']):
   os.makedirs(app.config['Upload_folder_Products'],0o777)
else:
    shutil.rmtree(app.config['Upload_folder_Products'])
    os.makedirs(app.config['Upload_folder_Products'],0o777)



allowed_extensions = ['csv']

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
       
        if isinstance(obj, Decimal):
            return str(obj)
            
        return json.JSONEncoder.default(self, obj)


def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions

'''
def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])
'''

'''
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db
'''

'''
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
'''
        
'''
def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows
'''
    
'''
def commit():
    get_db().commit()

'''

@app.route("/")
def hello():
    return render_template('login.html')


@app.route('/login', methods =['POST', 'GET'])
def login():
    message = ''
    '''
    # Test database connection
    conn = connecttoDataBase()
    print(conn)
    conn.close()
    '''
    if request.method == 'POST' and str(request.form['username']) !="" and str(request.form['password']) != "":
        username = str(request.form['username'])
        password = str(request.form['password'])
        # print("username", username)
        # print("password", password)
        
        result = executeselectquery("SELECT firstname,lastname,email  FROM users WHERE username  ='"+username+"' AND password_hash = '"+password+"'" )
        if (result.shape[0] != 0):
            print("Logged in Successfully")
            return render_template('HomePage.html', message=message)
        else:
            message = 'Invalid Credentials !'
        
    elif request.method == 'POST':
        message = 'Please enter Credentials'
    return render_template('login.html', message=message)


# '''
@app.route('/dashboard', methods =['GET','POST'])
def dashboard():
    return render_template('HomePage.html')
# '''

# '''
@app.route('/uploaddatasets', methods =['GET','POST'])
def uploaddatasets():
    return render_template('UploadData.html')
# '''


@app.route('/registration', methods =['GET','POST'])
def registration():
    message = ''
    # '''
    conn = connecttoDataBase()
    cursor = conn.cursor()
    
    if request.method == 'POST' and str(request.form['username']) !="" and str(request.form['password']) !="" and str(request.form['firstname']) !="" and str(request.form['lastname']) !="" and str(request.form['email']) !="":
        username = str(request.form['username'])
        password = str(request.form['password'])
        firstname = str(request.form['firstname'])
        lastname = str(request.form['lastname'])
        email = str(request.form['email'])
        
        result = executeselectquery("SELECT *  FROM users WHERE Username  ='"+username+"'")
        if (result.shape[0] != 0):
            message = 'User has already registered!'
        else:
            result1 = cursor.execute("""INSERT INTO users (username, password_hash, firstname, lastname, email) values (%s, %s, %s, %s, %s)""", (username, password, firstname, lastname, email))
            conn.commit()
            cursor.close()
            conn.close()
            result2 = executeselectquery( "SELECT firstname,lastname,email  FROM users WHERE username  = '"+username+"' AND password_hash ='"+ password+"'")
            if (result2.shape[0] != 0):
                message = 'User Registration Completed Successfully! Click Login.'
                return render_template('registrationSuccess.html', message=message)
    elif request.method == 'POST':
        message = 'Some of the fields are missing!!'
    # '''
    return render_template('registration.html', message=message)



@app.route('/searchhhm', methods =['GET', 'POST'])
def searchhhm():
    return loadtable("10");
    # return render_template('SearchHHM.html')


# '''
@app.route('/searchhhmnew', methods =['GET','POST'])
def searchhhmnew():
    if request.method == 'POST' and str(request.form['hshd_num']) != "":
        try:
            response=loadtable(str(request.form['hshd_num']));
        except:
            message = "Valid HSHD_NUM is required!!"
            return render_template('SearchHHM.html', message=message)
    else:
        message = "Valid HSHD_NUM is required!!"
        return render_template('SearchHHM.html',message=message)
    return response;

# '''


# '''
@app.route('/storeuploadedhouseholdfile', methods =['GET','POST'])
def storeuploadedhouseholdfile():
    message = 'Please upload file again!!'
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  
        if check_file_extension(f.filename):
            f.save(os.path.join(app.config['Upload_folder_HouseHolds'],secure_filename(f.filename)))  # this will secure the file
            readCSVandloaddata(os.path.join(app.config['Upload_folder_HouseHolds'], secure_filename(f.filename)),"households");
            message='file uploaded successfully'  # Display thsi message after uploading
        else:
            message='The file extension is not allowed'

    return render_template('UploadData.html',message=message)
# '''

# '''
@app.route('/storeuploadedProductfile', methods =['GET','POST'])
def storeuploadedProductfile():
    message = 'Please upload file again!!'
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  
        if check_file_extension(f.filename):
            f.save(os.path.join(app.config['Upload_folder_Products'],secure_filename(f.filename)))  # this will secure the file
            readCSVandloaddata(os.path.join(app.config['Upload_folder_Products'], secure_filename(f.filename)),"products");
            message='file uploaded successfully'  # Display thsi message after uploading
        else:
            message='The file extension is not allowed'

    return render_template('UploadData.html',messageProducts=message)
# '''

# '''
@app.route('/storeuploadedTransactionfile', methods =['GET','POST'])
def storeuploadedTransactionfile():
    message = 'Please upload file again!!'
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  # get the file from the files object
        # Saving he file in the required destination
        if check_file_extension(f.filename):
            f.save(os.path.join(app.config['Upload_folder_Transactions'], secure_filename(f.filename)))  # this will secure the file
            readCSVandloaddata(os.path.join(app.config['Upload_folder_Transactions'], secure_filename(f.filename)),"transactions");
            message='file uploaded successfully'  # Display thsi message after uploading
        else:
            message='The file extension is not allowed'

    return render_template('UploadData.html',messageTransactions=message)
# '''



def executeselectquery(queryString):
    conn = connecttoDataBase()
  
    return pd.read_sql(queryString,conn)

# '''
def loadtable(hshd_num):

    conn = connecttoDataBase()
    cursor = conn.cursor()
    cursor.execute("""Select a.HSHD_NUM,b.BASKET_NUM,b.PURCHASE_,b.PRODUCT_NUM,c.DEPARTMENT,c.COMMODITY,b.SPEND,b.UNITS,b.STORE_R,b.WEEK_NUM,b.YEAR_NUM,a.L,
    a.AGE_RANGE,a.MARITAL,a.INCOME_RANGE,a.HOMEOWNER,a.HSHD_COMPOSITION,a.HH_SIZE,a.CHILDREN from households as a inner join transactions as b inner join 
    products as c on a.HSHD_NUM=b.HSHD_NUM and b.PRODUCT_NUM=c.PRODUCT_NUM where a.HSHD_NUM="""+hshd_num+" order by a.HSHD_NUM,b.BASKET_NUM,b.PURCHASE_,b.PRODUCT_NUM,c.DEPARTMENT,c.COMMODITY;");
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('SearchHHMTable.html',data=rows)
# '''

# '''
def connecttoDataBase():
    config = {
    'host': 'cc-final-project-server.mysql.database.azure.com',
    'user': 'sudouser',
    'password': 'Family@4',
    'database': 'mydatabase'
    }
    # port : 3306
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return conn;
# '''

# '''
def readCSVandloaddata(csvfilepath,dataFrom):
    conn = connecttoDataBase()
    cursor = conn.cursor()
    df = pd.read_csv(csvfilepath)
    df.columns = df.columns.str.replace(' ', '')
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    dftotuple = list(df.to_records(index=False))
    if(dataFrom=='households'):
        for eachtuple in dftotuple:
            try:
                cursor.execute(
                    """INSERT INTO households (HSHD_NUM,L,AGE_RANGE,MARITAL,INCOME_RANGE,HOMEOWNER,HSHD_COMPOSITION,HH_SIZE,CHILDREN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (int(eachtuple.HSHD_NUM), str(eachtuple.L), str(eachtuple.AGE_RANGE), str(eachtuple.MARITAL),
                     str(eachtuple.INCOME_RANGE), str(eachtuple.HOMEOWNER), str(eachtuple.HSHD_COMPOSITION),
                     str(eachtuple.HH_SIZE), str(eachtuple.CHILDREN)));
            except Exception as e:  # work on python 3.x
                print('Failed to upload to ftp: ' + str(e))
    if (dataFrom == 'transactions'):
        for eachtuple in dftotuple:
            try:
                cursor.execute(
                    """INSERT INTO transactions (BASKET_NUM,HSHD_NUM,PURCHASE_,PRODUCT_NUM,SPEND,UNITS,STORE_R,WEEK_NUM,YEAR_NUM) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (int(eachtuple.BASKET_NUM), int(eachtuple.HSHD_NUM), str(eachtuple.PURCHASE_),
                     int(eachtuple.PRODUCT_NUM), int(eachtuple.SPEND), int(eachtuple.UNITS), str(eachtuple.STORE_R),
                     int(eachtuple.WEEK_NUM), int(eachtuple.YEAR)));
            except Exception as e:  # work on python 3.x
                print('Failed to upload to ftp: ' + str(e))
    if (dataFrom == 'products'):
        for eachtuple in dftotuple:
            try:
                cursor.execute("""INSERT INTO products (PRODUCT_NUM,DEPARTMENT,COMMODITY,BRAND_TY,NATURAL_ORGANIC_FLAG) VALUES (%s,%s,%s,%s,%s)""",
                    (int(eachtuple.PRODUCT_NUM), str(eachtuple.DEPARTMENT), str(eachtuple.COMMODITY),str(eachtuple.BRAND_TY),
                     str(eachtuple.NATURAL_ORGANIC_FLAG)));
            except Exception as e:  # work on python 3.x
                print('Failed to upload to ftp: ' + str(e))
    conn.commit()
    cursor.close()
    conn.close()

# '''

# '''
def readCSVFileandStoretoAzure(csvfilename,dataFrom):
    conn = connecttoDataBase()
    cursor = conn.cursor()
    
    # store large files in storage manager 
    # keep them out of app context
    # Get the path to the CSV file
    csv_path = os.path.join(app.root_path, 'static', 'data', '400_households.csv')

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.replace(' ', '')
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    dftotuple = list(df.to_records(index=False))
    for eachtuple in dftotuple:
        try:
            cursor.execute(
                """INSERT INTO households (HSHD_NUM,L,AGE_RANGE,MARITAL,INCOME_RANGE,HOMEOWNER,HSHD_COMPOSITION,HH_SIZE,CHILDREN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (int(eachtuple.HSHD_NUM), str(eachtuple.L), str(eachtuple.AGE_RANGE), str(eachtuple.MARITAL),
                 str(eachtuple.INCOME_RANGE), str(eachtuple.HOMEOWNER), str(eachtuple.HSHD_COMPOSITION),
                 str(eachtuple.HH_SIZE), str(eachtuple.CHILDREN)));
        except Exception as e:  # work on python 3.x
            print('Failed to upload to ftp: ' + str(e))
    
    conn.commit()
    cursor.close()
    conn.close()

# '''


# '''
@app.route('/loadDashboard', methods =['GET','POST'])
def loadDashboard():
    #First Graph(bar Graph)
    data=executeselectquery("Select SUM(b.SPEND) as Spent,a.HH_SIZE as household_Size from households as a inner join transactions as b on a.HSHD_NUM=b.HSHD_NUM group by a.HH_SIZE;");
    data['Spent']=data['Spent'].astype(str);
    data['household_Size'] = data['household_Size'].astype(str);

    #Second Grapgh(Bar Graph)
    Seconddata = executeselectquery(
        "Select SUM(b.SPEND) as spend,a.HH_SIZE as householdsize from households as a inner join transactions as b inner join products as c  on b.PRODUCT_NUM=c.PRODUCT_NUM and a.HSHD_NUM=b.HSHD_NUM and c.DEPARTMENT='FOOD'  group by c.DEPARTMENT,a.HH_SIZE;");
    Seconddata['spend'] = Seconddata['spend'].astype(str);
    Seconddata['householdsize'] = Seconddata['householdsize'].astype(str);

    SeconddataTwo = executeselectquery(
        "Select SUM(b.SPEND) as spend,a.HH_SIZE as householdsize from households as a inner join transactions as b inner join products as c  on b.PRODUCT_NUM=c.PRODUCT_NUM and a.HSHD_NUM=b.HSHD_NUM and c.DEPARTMENT='NON-FOOD'  group by c.DEPARTMENT,a.HH_SIZE;");
    SeconddataTwo['spend'] = SeconddataTwo['spend'].astype(str);

    Threedata = executeselectquery(
        "Select SUM(b.SPEND) as spend,c.COMMODITY as commodity  from households as a inner join transactions as b inner join products as c  on b.PRODUCT_NUM=c.PRODUCT_NUM and a.HSHD_NUM=b.HSHD_NUM and c.DEPARTMENT='FOOD'  group by c.COMMODITY;");
    Threedata['spend'] = Threedata['spend'].astype(str);
    Threedata['commodity'] = Threedata['commodity'].astype(str);

    Fourthdata = executeselectquery(
        "Select sum(SPEND) as spend,YEAR_NUM as year from transactions as a group by a.YEAR_NUM;");
    Fourthdata['spend'] = Fourthdata['spend'].astype(str);
    Fourthdata['year'] = Fourthdata['year'].astype(str);

    return render_template("Dashboard.html",title='Household Size vs Spent', max=17000,titletwo="Spent vs Householdsize vs Product Department",
                           labels=data['household_Size'].values.tolist(), values=data['Spent'].values.tolist(),
                           labelstwo=Seconddata['householdsize'].values.tolist(),valuestwo=Seconddata['spend'].values.tolist(),
                           valuestwotwo=SeconddataTwo['spend'].values.tolist(),
                           titlethree="Spent(Commodity:Food) vs Different Food Items",
                           labelsthree=Threedata['commodity'].values.tolist(),
                           valuesthree=Threedata['spend'].values.tolist(),
                           titlefour="Spent vs YEAR",
                           labelsfour=Fourthdata['year'].values.tolist(),
                           valuesfour=Fourthdata['spend'].values.tolist());
# '''


if __name__ == '__main__':
    app.run()