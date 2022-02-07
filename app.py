import pickle
import numpy as np 
from crypt import methods
from flask import Flask, render_template, request 

import sqlite3 as sql 
# calling create_database.py file for creating database 
import create_database



app = Flask(__name__) 

# model loading 
file_name = "logistic_model.sav"
loaded_model = pickle.load(open(file_name, 'rb'))

# creating database 
create_database.database_configuration()

def prediction(s_l, s_w, p_l, p_w, loaded_model): 
    pre_data = np.array([s_l, s_w, p_l, p_w]) 
    pre_data_reshape = pre_data.reshape(1, -1) 
    pred_result = loaded_model.predict(pre_data_reshape)  
    return pred_result[0]


@app.route('/')
def input_data(): 
    return render_template('input.html') 


@app.route('/result', methods=["POST", "GET"]) 
def input(): 
    if request.method == "POST": 
        try: 
            s_l = request.form['sepal_length']
            s_w = request.form['sepal_width']
            p_l = request.form['petal_length'] 
            p_w = request.form['petal_width'] 

            # predicted result 
            predicted_result = prediction(s_l, s_w, p_l, p_w, loaded_model)  

            # saving data into sqlite database 
            with sql.connect("database.db") as con: 
                cur = con.cursor() 
                cur.execute('INSERT INTO student_information (sepal_length, sepal_width, petal_length, petal_width, predicted_result) VALUES(?, ?, ?, ?, ?)', (s_l, s_w, p_l, p_w, predicted_result))  
                con.commit()  
                msg = 'Record successfully added'  
        except: 
            con.rollback() 
            msg = 'error in inserting dataset' 
        finally: 

            return render_template('result.html', predicted = predicted_result, msg = msg) 
            con.close() 
        

if __name__ == '__main__': 
    app.run(debug=True) 


