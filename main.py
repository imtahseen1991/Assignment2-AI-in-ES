"""
Creating flask application for CRUD methods
Developer: Tahseen Siddiqi
"""

# Importing the modules
from flask import Flask, jsonify, request
from dbconnection import connection
import logging

logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.INFO)

app = Flask(__name__)
cursor = connection()


@app.route("/basic")
def basic_app():
    return "Created a basic flask app"


@app.route("/read", methods=["GET"])
def read():
    cursor.execute("""SELECT * FROM assignment3""")
    values = cursor.fetchone()
    values = {"Student_ID": values[0], "First_name": values[1], "Second_name": values[2],
              "DOB": values[3], "Amount_Due": values[4]}
    logging.info(values)
    return values


@app.route("/create", methods=["POST"])
def create():
    student_id = request.json['STUDENT_ID']
    first_name = request.json['FIRST_NAME']
    last_name = request.json['LAST_NAME']
    dob = request.json['DOB']
    amount_due = request.json['AMOUNT_DUE']
    query = "INSERT INTO assignment3 (student_id, first_name, last_name, dob, amount_due) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, student_id, first_name, last_name, dob, amount_due)
    cursor.commit()
    cursor.close()
    response = {"message": "Post created Successfully"}
    logging.info(response, 201)
    return jsonify(response), 201


@app.route("/create/<int:student_id>", methods=["PUT"])
def update(student_id):
    dob=request.json["DOB"]
    query = "UPDATE assignment3 SET DOB=? where STUDENT_ID=?"
    cursor.execute(query, dob, student_id)
    cursor.commit()
    response={"message": "Post updated"}
    return jsonify(response)


@app.route("/delete/<int:student_id>", methods=["DELETE"])
def delete(student_id):
    query = "DELETE FROM assignment3 WHERE STUDENT_ID = ?"
    cursor.execute(query, student_id)
    cursor.commit()
    cursor.close()
    response = {"message": f"Post with ID {student_id} deleted successfully."}
    return jsonify(response), 200

@app.route("/return", methods=["GET"])
def get_all_rows():
    dict={}
    cursor.execute("SELECT * FROM assignment3")
    values = cursor.fetchall()
    result = []
    for row in values:
        # Convert each row to a dictionary
        row_dict = {
            'STUDENT_ID': row[0],
            'FIRST_NAME': row[1],
            'LAST_NAME': row[2],
            'DOB': row[3],
            'AMOUNT_DUE': row[4]
            # Add more columns as necessary
        }
        result.append(row_dict)

    return jsonify({'data': result})


if __name__ == "__main__":
    app.run(debug=True)
