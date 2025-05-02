from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__, template_folder="templates")
client = MongoClient('localhost', 27017)
db = client['employee_management']
collection = db['employees']

@app.route('/')
def index():
    employees = collection.find()
    return render_template('index.html', employees=employees)

@app.route('/update/<employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    if request.method == 'POST':
        filter_query = {'_id': ObjectId(employee_id)}
        name = request.form['name']
        designation = request.form['designation']
        salary = request.form['salary']
        update_data = {'$set': {'name': name, 'designation': designation, 'salary': salary}}
        collection.update_one(filter_query, update_data)
        return redirect(url_for('index'))
    else:
        employee = collection.find_one({'_id': ObjectId(employee_id)})
        return render_template('update.html', employee=employee)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    designation = request.form['designation']
    salary = request.form['salary']
    collection.insert_one({'name': name, 'designation': designation, 'salary': salary})
    return redirect(url_for('index'))

@app.route('/delete/<employee_id>')
def delete_employee(employee_id):
    collection.delete_one({'_id': ObjectId(employee_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
