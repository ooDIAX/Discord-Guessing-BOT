import logging
from logging.handlers import RotatingFileHandler
import os
import flask
import psycopg2

import data_handler
from dotenv import load_dotenv



# create logger
def init_logging(logger):
    # logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    handler_rot_file = RotatingFileHandler(filename='web-app.log', encoding='utf-8', mode='a')
    handler_rot_file.setLevel(logging.DEBUG)
    handler_rot_file.setFormatter(log_formatter)

    logger.addHandler(handler_rot_file)

    # handler_console = logging.StreamHandler()
    # handler_console.setLevel(logging.DEBUG)
    # handler_console.setFormatter(log_formatter)

#    logger.addHandler(handler_console)

    return logger


# to run the app:
# python3 -m flask --app webapp run --debug -p 8888 -h 0.0.0.0

app = flask.Flask(__name__)

# main route
@app.route('/')
def index():
    history = data_handler.get_history()

    return flask.render_template('main.html', history = history)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():

    # connect to the PostgreSQL server
    logging.info('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST_EXTERNAL'),
                            database=os.getenv('POSTGRES_DB'),
                            user=os.getenv('POSTGRES_USER'),
                            password=os.getenv('POSTGRES_PASSWORD'))

    logging.info('Connected.')

    # read products from database
    logging.info('Reading data...')
    cur = conn.cursor()
    cur.execute('SELECT * FROM leaderboard ORDER BY score DESC')
    
    rows = cur.fetchall()

    # render products template
    html = flask.render_template('leaderboard.html', products=rows)

    # close the communication with the PostgreSQL
    cur.close()
    conn.close()
    logging.info('Done.')

    return html


if __name__ == '__main__':
    logger = init_logging(logging.root)
    logging.info('Program started')

    # read environment variables
    load_dotenv()

    app.run(debug=True, port=8888, host='0.0.0.0')