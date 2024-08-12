import json
import os
from flask import Flask, request, Response
from flask_basicauth import BasicAuth
import psycopg2

app = Flask(__name__)
app.config["BASIC_AUTH_USERNAME"] = os.environ["PGRESTPY_SANDBOX_USERNAME"]
app.config["BASIC_AUTH_PASSWORD"] = os.environ["PGRESTPY_SANDBOX_PASSWORD"]

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def status():
  return 'pgrest.py is running'
  

@app.route('/sql', methods=["POST"])
@basic_auth.required
def sql():
    def format_column(x):
        if dict_to_json_bool and isinstance(x, dict):
            return json.dumps(x)
        else:
            return str(x)
    #
    prefix_str = request.args.get("prefix") if request.args.get("prefix") else ""
    column_delimiter_str = request.args.get("column_delimiter") if request.args.get("column_delimiter") else ","
    row_delimiter_str = request.args.get("row_delimiter") if request.args.get("row_delimiter") else "\n"
    suffix_str = request.args.get("suffix") if request.args.get("suffix") else ""
    dict_to_json_bool = False if request.args.get("dict_to_json") == "false" else True
    #
    response_dict = request.get_json()
    sql_str = response_dict["sql"]
    output_str = ""
    connection = None
    try:
        connection = psycopg2.connect(user="root", host=os.environ["PGRESTPY_DB_HOST"], port=os.environ["PGRESTPY_DB_PORT"], database=os.environ["PGRESTPY_DB_DATABASE"])
        #
        cursor = connection.cursor()
        cursor.execute(sql_str)
        #
        tuple_list = cursor.fetchall()
        #
        row_str_list = [column_delimiter_str.join([format_column(x) for x in tuple]) for tuple in tuple_list]
        output_str = f"{prefix_str}{row_delimiter_str.join(row_str_list)}{suffix_str}"

    except psycopg2.Error as error:
        print("Error connecting to PostgreSQL", error)
        return Response(error.pgerror, status=400)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

    return output_str


def run(port_int):
    app.run(host="0.0.0.0", port=port_int)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
