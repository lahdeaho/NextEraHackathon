#!/usr/bin/env python

from flask import Flask, render_template, send_file, Response, abort, jsonify
from flask_bootstrap import Bootstrap

from project import config
from project.models import *

import sys
import os
import shutil
import datetime

app = Flask(__name__)
Bootstrap(app)

# All views below
@app.route("/home")
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/layout")
def layout():
    return render_template('layout-template.html')

# API
@app.route('/cameraimages/<string:cam_id>/<string:yyyy>/<string:mmmm>/<string:dd>/<string:hh>/<string:mm>', methods=['GET'])
def get_cameraimage(cam_id, yyyy, mmmm, dd, hh, mm):
    filepath = "";
    if (len(cam_id) > 0 and len(yyyy) > 0 and len(mmmm) > 0 and len(dd) > 0 and len(hh) > 0 and len(mm) > 0):
        #'/mnt/azureshare2/data/src/img_2019-04-13_15:40:01/weathercam.digitraffic.fi/C1050102.jpg'
        #/mnt/azureshare2/data/images/traffic/C1453409/img/201904200510.jpg
        azure_dir = "data/images/traffic/%s/img" % (cam_id)
        azure_path = "%s/%s" % (azure_share, azure_dir)
        filename = "%s%s%s%s%s.jpg" % (yyyy, mmmm, dd, hh, mm);
        filepath = "%s/%s_%s" % (share_root, cam_id, filename);
        if (not os.path.exists(filepath)):
            try:
                file_service.get_file_to_path(azure_share, azure_dir, filename, filepath);
            except:
                try:
                    os.remove(filepath);
                except:
                    print("cannot remove", filepath);
                abort(404);
    else:
        abort(404);
   
    return send_file(filepath, mimetype='image/jpg')

@app.route('/imagevalidation/<string:cam_id>/<string:yyyy>/<string:mmmm>/<string:dd>/<string:hh>/<string:mm>/<string:valid>', 
           methods=['GET'])
def set_imagevalidation(cam_id, yyyy, mmmm, dd, hh, mm, valid):
    filepath = "/data/src/traffic/webapp/project/data/labels.csv"; # TODO: relatiivinen sijainti
    if (not os.path.exists(filepath)):
        with open(filepath, "w") as fo:
            fo.write("camera;filename;created;label");
            fo.write("\n");
    if (len(cam_id) > 0 and len(yyyy) > 0 and len(mmmm) > 0 and len(dd) > 0 and len(hh) > 0 and len(mm) > 0 and len(valid) > 0):
        filename = "%s%s%s%s%s.jpg" % (yyyy, mmmm, dd, hh, mm);
        d = datetime.datetime.now().replace(microsecond=0).isoformat();
        with open(filepath, "a") as fo:
            fo.write("%s;%s;%s;%s\n" % (cam_id, filename, d, valid));

    else:
        abort(404);
   
    resp = jsonify(success=True);
    return resp

@app.route('/islabeled/<string:cam_id>/<string:yyyy>/<string:mmmm>/<string:dd>/<string:hh>/<string:mm>', 
           methods=['GET'])
def get_islabeled(cam_id, yyyy, mmmm, dd, hh, mm):
    islabeled = 0;
    if (len(cam_id) > 0 and len(yyyy) > 0 and len(mmmm) > 0 and len(dd) > 0 and len(hh) > 0 and len(mm) > 0):   
        filename = "%s%s%s%s%s.jpg" % (yyyy, mmmm, dd, hh, mm);

    else:
        abort(404);
   
    resp = jsonify(islabeled=islabeled);
    return resp

@app.route('/getmapdata', methods=['GET'])
def get_masks():
    masks = [];
    for rootdir, dirs, files in os.walk("/data/src/traffic/webapp/project/static/img/masks"):
        for f in files:
            masks.append(f[5:13]);    
    resp = jsonify(masks=masks);
    return resp

# Error Pages
@app.errorhandler(500)
def error_page(e):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404




