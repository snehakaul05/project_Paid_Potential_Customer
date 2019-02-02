
#Loading the Libraries 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import datetime as dt
from sklearn.cross_validation import train_test_split

from sklearn.linear_model import LogisticRegression

from flask import Flask, request, redirect, url_for, jsonify,render_template

import pickle
from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)
customer_data = pd.read_csv("usage_data_final.csv")
model_filename = 'finalized_model.sav'
#pickle.dump(model, open(filename, 'wb'))

def dataPrep(): 
    
    print(customer_data.head())
    customer_data['id']= customer_data.index
    customer_data['customer_name'] = customer_data.apply(lambda row: "company"+ str(row.id) , axis=1)
    ## Data Cleaning and filtering 
    #dropping an Column not needed 


dataPrep()
print(customer_data.columns)
print(customer_data.head())
predict_data  = {}

@app.route("/")
def index():
    """Return the homepage."""

    return render_template("index.html",data=predict_data)

@app.route('/predictProspects', methods=['GET', 'POST'])
def predictProspects():
    X = customer_data[['avg_daily_time', 'onboarded_age', 'VM_count ', 'avg_url_count']]
    y = customer_data['potention_buyer']

    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.3, random_state=42)


    model = LogisticRegression()
    model.fit(X_train,y_train)
    predictions = model.predict(X_test)

    from sklearn.metrics import classification_report,confusion_matrix
    print(classification_report(y_test,predictions))
    print(confusion_matrix(y_test,predictions))


    df_results =pd.DataFrame({"Prediction": predictions, "Actual": y_test})
    print(df_results)
    data = df_results.to_dict()
    
    pickle.dump(model, open(model_filename, 'wb'))

    return jsonify(data)
    #return jsonify(data)

@app.route('/predictCustomer')
def predictCustomer():
    X = customer_data[['avg_daily_time', 'onboarded_age', 'VM_count ', 'avg_url_count']]
    y = customer_data['potention_buyer']

    X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.3, random_state=42)


    model = LogisticRegression()
    model.fit(X_train,y_train)
    predictions = model.predict([[83.42,25,49851,183.42]])

    #predictions  = model.predict([[83.42,25,49851,183.42]])
    df_results =pd.DataFrame({"Prediction": predictions})
    print(df_results)
    data = df_results.to_dict()
 

    return jsonify(data)
    #return jsonify(data)
#predictProspects()

@app.route('/loadModelTest')
def loadModelTest():
    loaded_model = pickle.load(open(model_filename, 'rb'))
    

    #print (loaded_model.predict([[71.23,52,41521,122.59]]))
    predictions = loaded_model.predict([[71.23,52,41521,122.59]])

    #predictions  = model.predict([[83.42,25,49851,183.42]])
    df_results =pd.DataFrame({"Prediction": predictions})
    print(df_results)
    data = df_results.to_dict()
 

    return jsonify(data)


@app.route("/allCustomers")
def allCustomers():
    """Return a list of customers."""

    all_customers = list(customer_data['customer_name'])
    #return jsonify(all_customers) 

    dictA= {'customers':all_customers}
    return jsonify(dictA)    

#customer_info

@app.route("/customer_info/<customer>")
def customer_info(customer):
    """Return the customer details  information for a given customer"""

    customer_info ={}
    loaded_model = pickle.load(open(model_filename, 'rb'))
    #company_data = customer_data.loc[customer_data['customer_name'] == customer]
    company_data = customer_data.loc[customer_data['customer_name'] == customer][['avg_daily_time', 'onboarded_age', 'VM_count ', 'avg_url_count']]
    predictions = loaded_model.predict(company_data.values.tolist())
    if (predictions[0] ==0):
        str1 = "Customer is not predicted as potential Buyer"
    else:
        str1 = "Congratulations ,Customer  is a potential Buyer" 
    customer_info = {"Comapany Name " :customer,
                    "Company Age in days "  : float(company_data['onboarded_age'].values[0]),
                    "Avg Daily time spent in mins " : float(company_data['avg_daily_time'].values[0]),
                    "Predicted Value by Model" : str(predictions[0]),
                    "Count of VMs ": float(company_data['VM_count '].values[0]),
                    "Count of URLS ": float(company_data['avg_url_count'].values[0]),
                    "Result " : str1  }

    return jsonify(customer_info)


@app.route('/potentialCustomer/<customer>')
def potentialCustomer(customer):
    loaded_model = pickle.load(open(model_filename, 'rb'))
    #print (loaded_model.predict([[71.23,52,41521,122.59]]))
    company_data = customer_data.loc[customer_data['customer_name'] == customer][['avg_daily_time', 'onboarded_age', 'VM_count ', 'avg_url_count']]
    #textdata.append(customer_data[customer_data['customer_name'] == customer]['avg_daily_time', 'onboarded_age', 'VM_count ', 'avg_url_count'])
    predictions = loaded_model.predict(company_data.values.tolist())
    #predictions  = model.predict([[83.42,25,49851,183.42]])
    df_results =pd.DataFrame({"Prediction": predictions})
    print(df_results)
    data = df_results.to_dict()
    return jsonify(data)

@app.route('/allCustomerData')
def allCustomerData():
    return jsonify(customer_data.to_dict(orient="records")) 

@app.route("/predict/<daily_time>/<age>/<vms>/<url_count>")
def age_group(daily_time,age,vms,url_count):
    """This function predicts the customer from given form values  """
    loaded_model = pickle.load(open(model_filename, 'rb'))
    args = [daily_time,age,vms,url_count]
    argsList  = list(map(float,args))
    predictions = loaded_model.predict([argsList])

    df_results =[]
    if (predictions[0] ==0):
        str1 = " ,Customer is not predicted as potential Buyer"
    else:
        str1 = " ,Congratulations ,Customer  is a potential Buyer" 
    predict_str = "Predicted value is " + str(predictions[0]) + str1      
    df_results.append("Predicted value is " + str(predictions[0]) + str1)

    return jsonify(df_results) 
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)