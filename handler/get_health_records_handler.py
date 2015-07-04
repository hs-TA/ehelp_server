#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Health_Records_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    records = db.get_health_records(params)
    if records is None:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.HEALTH_LIST] = records
      resp[KEY.STATUS] = STATUS.OK
    
    self.write(json_encode(resp))

    

