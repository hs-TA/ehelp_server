#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Add_Comment_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    comment_id = db.add_comment(params)
    if comment_id > 0:
      comment_info = {}
      comment_info[KEY.COMMENT_ID] = comment_id
      resp = db.get_comment_info(comment_info)
      if resp is None:
        resp = {}      
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

