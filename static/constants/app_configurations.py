class AppConfigValues:
    try:
        HOUSEHOLD_FOLDER = 'Upload_folder_HouseHolds'
        TRANSACTIONS_FOLDER = 'Upload_folder_Transactions'
        PRODUCTS_FOLDER= 'Upload_folder_Products'
        ALLOWED_EXTENSIONS = ['csv']
    except Exception as e:
        print("Upload Folders are not found or extensions are not found")
        raise e
    
class Queries:
    try:
        LOGIN_SELECT_QUERY = "SELECT firstname,lastname,email  FROM users WHERE username = '{}' AND password_hash = '{}'"
        IS_REGISTERED_SELECT_QUERY = "SELECT *  FROM users WHERE username ='{}'"
        IS_IN_DATABASE_SELECT_QUERY = "SELECT firstname,lastname,email  FROM users WHERE username  = '{}' AND password_hash ='{}'"
        REGISTRATION_INSERT_QUERY = """INSERT INTO users (username, password_hash, firstname, lastname, email) values (%s, %s, %s, %s, %s)"""
        LOAD_JOINED_TABLE_QUERY = "Select a.HSHD_NUM,b.BASKET_NUM,b.PURCHASE_,b.PRODUCT_NUM,c.DEPARTMENT,c.COMMODITY,b.SPEND,b.UNITS,b.STORE_R,b.WEEK_NUM,b.YEAR_NUM,a.L,\
    a.AGE_RANGE,a.MARITAL,a.INCOME_RANGE,a.HOMEOWNER,a.HSHD_COMPOSITION,a.HH_SIZE,a.CHILDREN from households as a inner join transactions as b inner join \
    products as c on a.HSHD_NUM=b.HSHD_NUM and b.PRODUCT_NUM=c.PRODUCT_NUM where a.HSHD_NUM='{}' order by a.HSHD_NUM,b.BASKET_NUM,b.PURCHASE_,b.PRODUCT_NUM,c.DEPARTMENT,c.COMMODITY;"
        HOUSEHOLD_TABLE_INSERT_QUERY = """INSERT INTO households (HSHD_NUM,L,AGE_RANGE,MARITAL,INCOME_RANGE,HOMEOWNER,HSHD_COMPOSITION,HH_SIZE,CHILDREN) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        TRANSACTIONS_TABLE_INSERT_QUERY = """INSERT INTO transactions (BASKET_NUM,HSHD_NUM,PURCHASE_,PRODUCT_NUM,SPEND,UNITS,STORE_R,WEEK_NUM,YEAR_NUM) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        PRODUCTS_TABLE_INSERT_QUERY = """INSERT INTO products (PRODUCT_NUM,DEPARTMENT,COMMODITY,BRAND_TY,NATURAL_ORGANIC_FLAG) VALUES (%s,%s,%s,%s,%s)"""
        FIRST_PLOT_DASHBOARD_QUERY = "Select SUM(b.SPEND) as Spent,a.HH_SIZE as household_Size from households as a inner join transactions as b on a.HSHD_NUM=b.HSHD_NUM group by a.HH_SIZE;"
        SECOND_PLOT_DASHBOARD_FOOD_QUERY = "Select SUM(b.SPEND) as spend,a.HH_SIZE as householdsize from households as a inner join transactions as b inner join products as c  on b.PRODUCT_NUM=c.PRODUCT_NUM and a.HSHD_NUM=b.HSHD_NUM and c.DEPARTMENT='FOOD'  group by c.DEPARTMENT,a.HH_SIZE;"
        SECOND_PLOT_DASHBOARD_NON_FOOD_QUERY = "Select SUM(b.SPEND) as spend,a.HH_SIZE as householdsize from households as a inner join transactions as b inner join products as c  on b.PRODUCT_NUM=c.PRODUCT_NUM and a.HSHD_NUM=b.HSHD_NUM and c.DEPARTMENT='NON-FOOD'  group by c.DEPARTMENT,a.HH_SIZE;"
        THIRD_PLOT_DASHBOARD_QUERY = "Select SUM(b.SPEND) as spend,c.COMMODITY as commodity  from households as a inner join transactions as b inner join products as c  on b.PRODUCT_NUM=c.PRODUCT_NUM and a.HSHD_NUM=b.HSHD_NUM and c.DEPARTMENT='FOOD'  group by c.COMMODITY;"
        FOURTH_PLOT_DASHBOARD_QUERY = "Select sum(SPEND) as spend,YEAR_NUM as year from transactions as a group by a.YEAR_NUM;"
    except Exception as e:
        print("queries not found")
        raise e
    
class DataBaseConfigValues:
    try:
        HOST_NAME = 'cc-final-project-server.mysql.database.azure.com'
        USER_NAME = 'sudouser'
        PASSWORD = 'Family@4'
        DATABASE_NAME = 'mydatabase'
    except Exception as e:
        print("Failed to get the Database configuration details")
        raise e