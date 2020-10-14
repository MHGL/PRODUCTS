# -*- coding:utf-8 -*-
import os
import sys
import time
import json
import flask
import logging
import optparse
import datetime
import tornado.wsgi
import tornado.httpserver

from main import audio_detect
from download import download


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Obtain the flask app object
app = flask.Flask(__name__)

@app.route('/migu/music_pattern/v1.0', methods=['GET', 'POST'])
def detector():
    start_time = time.time()
    try:
        path = flask.request.form['path']
    except:
        path = None
    try:
        url = flask.request.form['url']
    except:
        url = None
    try:
        file = flask.request.files['file']
    except:
        file = None

    # mode: debug
    try:
        debug = flask.request.form['debug']
    except:
        debug = False

    try: 
        flag = False
        if path and not url and not file:
            assert os.path.exists(path), "Invalid local path"
            debug or allowed_filename(path)
        elif url and not path and not file:
            filename = f"download-{str(time.time()).split('.')[-1]}.mp3"
            download(url, filename)
            flag = True
            path = filename
        elif file and not path and not url:
            debug or allowed_filename(file.filename)
            filename = f"upload-{str(time.time()).split('.')[-1]}.wav"
            file.save(filename)
            flag = True
            path = filename 
        else:
            raise Exception("Invalid request message, keys must be one of [path, url, file]")
        receive_time = time.time()
        logging.info(f"Audio file receive cost: {receive_time-start_time}")
        beat_times, vocals_rhythm_times, accompaniment_rhythm_times = audio_detect(path)                               
        logging.info("Audio processing cost: {time.time() - start_time}")
        args = (beat_times, vocals_rhythm_times, accompaniment_rhythm_times)
    except Exception as e:
        args = (str(e), )
    finally:
        if flag:
            os.remove(filename)
        result = packResult(args) 
    return flask.make_response(result)

def allowed_filename(filename):
    flag = '.' in filename and filename.split('.')[-1].lower() in ['mp3', 'wav']
    if flag:
        return flag
    raise Exception("Invalid filename extension")

def packResult(args):
    respDict = {}
    if len(args) == 3:
        respDict['beat_times'] = args[0]
        respDict['vocals_rhythm_times'] = args[1]
        respDict['accompaniment_rhythm_times'] = args[2]
        logging.info('detect result >>> beat_times:{}'.format(respDict['beat_times']))
        logging.info('detect result >>> vocals_rhythm_times:{}'.format(respDict['vocals_rhythm_times']))
        logging.info('detect result >>> accompaniment_rhythm_times:{}'.format(respDict['accompaniment_rhythm_times']))
    else:
        respDict['Error'] = args[0]
        logging.info('detect result >>> Error: {}'.format(respDict['Error']))

    json_resp = json.dumps(respDict, ensure_ascii=False)
    return json_resp


def start_tornado(app, port=10080):
    http_server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    logging.info("Tornado server starting on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()


def start_from_terminal(app):
    """
    Parse command line options and start the server.
    """
    parser = optparse.OptionParser()
    parser.add_option(
    '-d', '--debug',
    help="enable debug mode",
    action="store_true", default=False)
    parser.add_option(
    '-p', '--port',
    help="which port to serve content on",
    type='int', default=10080)

    opts, args = parser.parse_args()

    # Initialize classifier
    # app.coco_demo = loadPth(CONFIG_FILE,MODEL_WEIGHT)

    if opts.debug:
        app.run(debug=True, host='0.0.0.0', port=opts.port)
    else:
        start_tornado(app, opts.port)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    start_from_terminal(app)
