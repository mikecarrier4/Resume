"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
import openaq


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)


@app.route('/')
def root():
    results = Record.query.all()
    return f""" Current Air Quality{results[:1]} """


@app.route('/dangerous')
def dangerous():
    results = DB.session.execute(
        """
        SELECT *
        FROM Pollution_History
        WHERE value > 10
        ORDER BY Value
        LIMIT 10
        """)
    line_list = []
    for row in results:
        line = str(row)
        line_list.append(line)
    return f""" The following were days dangerous air {str(line_list)} """


@app.route('/bad')
def bad():
    results = DB.session.execute(
      """SELECT *
      FROM Pollution_History
      WHERE value > 3.5 AND value < 10
      ORDER BY Value LIMIT 10
      """)
    line_list = []
    for row in results:
        line = str(row)
        line_list.append(line)
    return f""" The following were days with bad air {str(line_list)} """


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    api = openaq.OpenAQ()
    display = get_results(api)
    display.to_sql(name='Pollution_History',
    con=DB.engine, if_exists='append', index=False)
    DB.session.commit()
    return 'Data refreshed!'


@app.route('/reset')
def reset():
    DB.drop_all()
    DB.create_all()
    return redirect('/refresh')


def get_results(api):
    results = api.measurements(city='Los Angeles',
    parameter='pm25',
    df=True)
    print(results.columns)
    print(results.index)
    display = results[['value', 'city']]
    display.reset_index(level=0, inplace=True)
    display.rename(columns={'date.local': 'date'}, inplace=True)
    print(display.head())
    return display


class Record(DB.Model):
    __tablename__ = "Pollution_History"
    __table_args__ = {"sqlite_autoincrement": True}
    index = DB.Column(DB.Integer, primary_key=True)
    date = DB.Column(DB.String, nullable=False)
    value = DB.Column(DB.Integer, nullable=False)
    city = DB.Column(DB.String)

    def __repr__(self):
        return f"""The pm25 reading for 
        {self.city} was
        {self.value} at
        {self.date}"""
