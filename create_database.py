import sqlite3 

def database_configuration(): 
    try: 
        conn = sqlite3.connect("database.db") 
        print("Opened database successfully") 

        #conn.execute('DROP TABLE student_information') 
        #print('table dropped ') 
        conn.execute('CREATE TABLE student_information(id INTEGER PRIMARY KEY AUTOINCREMENT, sepal_length NUMERIC, sepal_width NUMERIC, petal_length NUMERIC, petal_width NUMERIC, predicted_result TEXT)')   
        print("Table created successfully") 
        conn.close 
        print("database created successfully")  
    except: 
        print('oops! something woring. database has not created')

