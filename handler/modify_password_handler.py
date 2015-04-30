#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Modify_Password_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    result = db.modify_password(params)
    resp = {}
    if result:
      resp[KEY.STATUS] = STATUS.OK
      resp[KEY.ACCOUNT] = params[KEY.ACCOUNT]
    else:
      resp[KEY.STATUS] = STATUS.ERROR    
   
    self.write(json_encode(resp))

    

