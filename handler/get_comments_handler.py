#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Comments_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    comments = db.get_comments(params)
    if comments is None:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.COMMENT_LIST] = comments
      resp[KEY.STATUS] = STATUS.OK
    
    self.write(json_encode(resp))

    

