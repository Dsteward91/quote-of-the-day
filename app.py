from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://aqvcwbzttqgkyf:d64ebcf4393016991c94d76c1e6c3b6f530e46ee71d4350fb6d7a6f4d24ed079@ec2-44-193-188-118.compute-1.amazonaws.com:5432/d1c9ks7e6hm82e"
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String, nullable = False)
    author = db.Column(db.String)
    def __init__(self,text, author):
        self.text = text
        self.author = author

class Date(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.Integer, nullable = False)
    quote = db.Column(db.Integer, nullable = False)
    def __init__(self,day, quote):
        self.day = day
        self.quote = quote

class QuoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "author")
quote_schema = QuoteSchema()
multiple_quote_schema = QuoteSchema(many = True)

class DateSchema(ma.Schema):
    class Meta:
        fields = ("id", "day", "quote")
date_schema = DateSchema()
@app.route("/quote/add", methods=["POST"])
def add_quote():
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")
    post_data = request.get_json()
    text = post_data.get("text")
    author = post_data.get("author")
    record = Quote(text, author)
    db.session.add(record)
    db.session.commit()
    return jsonify(quote_schema.dump(record))
@app.route("/quote/get/<id>", methods=["GET"])
def get_quote_by_id(id):
    record = db.session.query(Quote).filter(Quote.id == id).first()
    return jsonify(quote_schema.dump(record))

@app.route("/date/add", methods=["POST"])
def create_initial_date():
    record_check = db.session.query(Date).first()
    if record_check is not None:
        return jsonify("ERROR: Date has already been added.")
    if request.content_type != "application/json":
        return jsonify("ERROR Data must be sent as JSON.")
    post_data = request.get_json()
    day = post_data.get("day")
    quote = post_data.get("quote")
    record = Date(day,quote)
    db.session.add(record)
    db.session.commit()
    return jsonify(date_schema.dump(record))

@app.route("/date/get", methods= ["GET"])
def get_date():
    record = db.session.query(Date).first()
    return jsonify(date_schema.dump(record))

@app.route("/date/update", methods=["PUT"])
def update_date():
    record = db.session.query(Date).first()
    if record is None:
        return jsonify("Error Date has not been initialized.")

    if request.content != "application/json":
        return jsonify("Error:Data must be sent as json")

        put_date = request.get_json()
        day = put_data.get("day")
        quote = posy_data.get("quote")
        print(day)

        all_quotes = db.session.query(Quote).all()
        current_quote = db.session.query(Quote).filter(Quote.id == reocrd.quote).first()
        current_quote_index = all_qoutes.index(cureent_quote)
        if current_quote_index < len(all_quotes):
            next_quote = all_quotes[current_quote_index + 1]
        else:
            next_quote = all_quotes[0]

        record.day = day
        record.quote = next_quote.id
        db.session.commit()

        return jsonify(date_schema.dump(record))


if __name__ == "__main__":
    app.run(debug=True)