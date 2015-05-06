#!/usr/python

import sys
import random
import string
import hashlib
import MySQLdb


from dbhelper import dbhelper
from  utils import KEY


  
'''
add a new account to database.
@params a dict data:
        includes account and password.
@return -1 indicates params are not complete. Or account is not unique that leads to database fails.
        other number indicates success and the number is the id of the new account.
'''
def add_account(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data:
    return -1
  
  salt = ''.join(random.sample(string.ascii_letters, 8))
  md5_encode = hashlib.md5()
  md5_encode.update(data[KEY.PASSWORD]+salt)
  password = md5_encode.hexdigest()
  sql_account = "insert into account (account, password, salt) values ('%s', '%s', '%s')"
  sql_user = "insert into user (id, nickname) values (%d, '%s')"
  try:
    insert_id = dbhelper.insert(sql_account%(data[KEY.ACCOUNT], password, salt))
    dbhelper.insert(sql_user%(insert_id, data[KEY.ACCOUNT]))
    return insert_id
  except:
    return -1


'''
update information of an account.
@params a dict data:
        includes id and chat_token:
@return True if successfully modify chat_token
        False modification fails.
'''
def update_account(data):
  if KEY.ID in data and KEY.CHAT_TOKEN in data:
    sql = "update account set chat_token = '%s' where id = %d"
    try:
      if dbhelper.execute(sql%(data[KEY.CHAT_TOKEN], data[KEY.ID])) > 0:
        return True
    except:
      return False
  else:
    return False


'''
modify user's information.
@params a dict data:
        options include user's name, nickname, gender, age, phone, location,
        (longitude and latitude), occupation, identity_id.
@return True if successfully modify
        False modification fails.
'''
def update_user(data):
  if KEY.ID not in data:
    return False
  result = True
  
  sql = ""
  if KEY.NAME in data:
    data[KEY.NAME] = MySQLdb.escape_string(data[KEY.NAME].encode("utf8"))
    sql = "update user set name = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.NAME], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.NICKNAME in data:
    data[KEY.NICKNAME] = MySQLdb.escape_string(data[KEY.NICKNAME].encode("utf8"))
    sql = "update user set nickname = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.NICKNAME], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.GENDER in data:
    sql = "update user set gender = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.GENDER], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.AGE in data:
    sql = "update user set age = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.AGE], data[KEY.ID]))
      result &= True
    except:
      result &= False
   
  if KEY.PHONE in data:
    sql = "update user set phone = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.PHONE], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.LOCATION in data:
    data[KEY.LOCATION] = MySQLdb.escape_string(data[KEY.LOCATION].encode("utf8"))
    sql = "update user set location = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LOCATION], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.LONGITUDE in data and KEY.LATITUDE in data:
    sql = "update user set longitude = %f, latitude = %f where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.ID]))
      result &= True
    except:
      result &= False
  elif not (KEY.LONGITUDE not in data and KEY.LATITUDE not in data):
    result &= False

  if KEY.OCCUPATION in data:
    sql = "update user set occupation = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.OCCUPATION], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.IDENTITY_ID in data:
    sql = "update user set identity_id = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.IDENTITY_ID], data[KEY.ID]))
      result &= True
    except:
      result &= False

  return result


'''
get salt of an account.
@params include user's account.
@return salt of an account.
  None if account not exists or database query error.
'''
def get_salt(data):
  if KEY.ACCOUNT not in data:
    return None
  sql = "select salt from account where account = '%s'"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ACCOUNT]))
    if res is None:
      return None
    else:
      return res[0]
  except:
    return None


'''
validate whether password is correct.
@params includes user's account and password.
                      password need to be md5 encode.
@return user's id if password is correct.
         -1 otherwise.
'''
def validate_password(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data or KEY.SALT not in data:
    return -1
  sql = "select id, password from account where account = '%s' and salt = '%s'"
  user_id = -1
  password = None
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ACCOUNT], data[KEY.SALT]))
    if res is not None:
      user_id = res[0]
      password = res[1]
  except:
    pass
  finally:
    if password is None or data[KEY.PASSWORD] is None:
      return -1
    elif password == data[KEY.PASSWORD]:
      return user_id
    else:
      return -1


'''
modify user's password to a new one, but not modify its salt value.
@params include user's account. 
                      new password that encode with salt by md5.
@return true if successfully modify.
           false otherwise.
'''
def modify_password(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data:
    return False
  sql = "update account set password = '%s' where account = '%s'" 
  try:
    n = dbhelper.execute(sql%(data[KEY.PASSWORD], data[KEY.ACCOUNT]))
    if n > 0:
      return True
    else:
      return False
  except:
      return False
  
  
'''
get user's information, which includes user's name, nickname, gender ...... .
@params include user's id.
@return a json includes user's concrete information.
           None if params error or database query error.
'''
def get_user_information(data):
  if KEY.ID not in data:
    return None
  sql = "select * from user where id = %d"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ID]))
    if res is None:
      return None
    else:
      user = {}
      user[KEY.ID] = res[0]
      user[KEY.NAME] = res[1]
      user[KEY.NICKNAME] = res[2]
      user[KEY.GENDER] = res[3]
      user[KEY.AGE] = res[4]
      user[KEY.PHONE] = res[5]
      user[KEY.LOCATION] = res[6]
      user[KEY.LONGITUDE] = float(res[7])
      user[KEY.LATITUDE] = float(res[8])
      user[KEY.OCCUPATION] = res[9]
      user[KEY.REPUTATION] = float(res[10])
      user[KEY.IDENTITY_ID] = res[12]
      user[KEY.IS_VERIFY] = res[14]
      return user
  except:
    return None


'''
launch a help event by launcher.
@params includes user's id and type of help event.
        help event types:
                         0 represents normal question.
                         1 represents nornal help.
                         2 represents emergency.
       other option params includes content of event, longitude and latitude of event.
@return event_id if successfully launches.
        -1 if fails.
'''
def add_event(data): 
  if KEY.ID not in data or KEY.TYPE not in data:
    return -1
  sql = "insert into event (launcher, type, time) values (%d, %d, now())"
  event_id = -1
  try:
    event_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.TYPE]))
    if event_id > 0:
      data[KEY.EVENT_ID] = event_id
      update_event(data)
    return event_id
  except:
    return -1


'''
modify information of a help event.
@params  includes event_id, which is id of the event to be modified.
         option params includes: content of event, longitude and latitude of event, state of event.
@return True if successfully modifies.
        False otherwise.
'''
def update_event(data):
  result = True
  sql = ""
  if KEY.CONTENT in data:
    data[KEY.CONTENT] = MySQLdb.escape_string(data[KEY.CONTENT].encode("utf8"))
    sql = "update event set content = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.CONTENT], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False
  
  if KEY.LONGITUDE in data and KEY.LATITUDE in data:
    sql = "update event set longitude = %f, latitude = %f where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  if KEY.STATE in data:
    if data[KEY.STATE] == 0:
      data[KEY.STATE] = 1
    sql = "update event set state = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.STATE], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  return result


'''
remove a help event by event launcher.
@params includes user's id, which is remover. Actually, only the launcher can remove his/her event.
                 event's id, which represents the event to be removed.
@return True if successfully removes, or remover is not the launcher, actually nothing happens.
        False if fails.
'''
def remove_event(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return False
  sql = "delete from event where id = %d and launcher = %d"
  try:
    dbhelper.execute(sql%(data[KEY.EVENT_ID], data[KEY.ID]))
    return True
  except:
    return False


'''
get information of a help event.
@params includes id of the event to get.
@return concrete information of the event:
        event_id, launcher's id and his/her nickname, content, type, time, longitude and latitude, state, number of followers, number of supporters and group points.
        None indicates fail query.
'''
def get_event_information(data):
  if KEY.EVENT_ID not in data:
    return None
  event_info = None
  sql = "select * from event where id = %d"
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID]))
    if sql_result is not None:
      event_info = {}
      event_info[KEY.EVENT_ID] = sql_result[0]
      event_info[KEY.LAUNCHER_ID] = sql_result[1]
      event_info[KEY.CONTENT] = sql_result[2]
      event_info[KEY.TYPE] = sql_result[3]
      event_info[KEY.TIME] = str(sql_result[4])
      event_info[KEY.LONGITUDE] = float(sql_result[5])
      event_info[KEY.LATITUDE] = float(sql_result[6])
      event_info[KEY.STATE] = sql_result[7]
      event_info[KEY.FOLLOW_NUMBER] = sql_result[8]
      event_info[KEY.SUPPORT_NUMBER] = sql_result[9]
      event_info[KEY.GROUP_PTS] = float(sql_result[10])
      user = {}
      user[KEY.ID] = event_info[KEY.LAUNCHER_ID]
      user = get_user_information(user)
      if user is not None:
        event_info[KEY.LAUNCHER] = user[KEY.NICKNAME]
  except:
    pass
  finally:
    return event_info


'''
get information of a collection of events.
@params includes data, a json that contains user's id and type of events to get.
                 get_event_id_list a method of getting event id list.
@return a array of events. each element is information of an event in json form.
'''
def get_events(data, get_event_id_list):
  event_id_list = get_event_id_list(data)
  event_list = []
  event_info = {}
  for event_id in event_id_list:
    event_info[KEY.EVENT_ID] = event_id
    event_info = get_event_information(event_info)
    if event_info is not None:
      event_list.append(event_info)
  return event_list


'''
get events that launch by user.
@params includes user's id, 
                 option params includes state indicates all events or those starting or ended.
                 type indicates type of events.
@return an array of result event ids.
'''
def get_launch_event_list(data):
  event_id_list = []
  if KEY.ID not in data:
    return event_id_list
  sql = "select id from event where launcher = %d"%data[KEY.ID]
  if KEY.STATE in data:
    if data[KEY.STATE] == 0 or data[KEY.STATE] == 1:      
      sql += " and state = %d"%data[KEY.STATE]
  if KEY.TYPE in data:
    if data[KEY.TYPE] >= 0 and data[KEY.TYPE] <= 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      event_id_list.append(each_id)

  return event_id_list


'''
get user's follow or support events.
@params includes user's id and type of user's state in event.
                 user's state 0 indicates follow, and 1 indicates support.
@return an array of result event ids.
'''
def get_join_event_list(data):
  event_id_list = []
  if KEY.ID not in data:
    return event_id_list
  sql = "select event_id from support_relation where supporter = %d"%data[KEY.ID]
  if KEY.TYPE in data:
    if data[KEY.TYPE] == 1 or data[KEY.TYPE] == 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      event_id_list.append(each_id)

  return event_id_list


'''
manage relation of user and event.
@params
@return
'''
def user_event_manage(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return False
  if KEY.OPERATION not in data:
    return True
  if data[KEY.OPERATION] < 0 or data[KEY.OPERATION] > 2:
    return False
  sql = "select launcher from event where id = %d"
  launcher_id = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID]))
    if sql_result is not None:
      launcher_id = sql_result[0]
  except:
    pass
  if launcher_id is None:
    return False
  if data[KEY.OPERATION] == 0:
    sql = "delete from support_relation where event_id = %d and supporter = %d"%(data[KEY.EVENT_ID], data[KEY.ID])
  else:
    sql = "replace into support_relation (event_id, supportee, supporter, type, time) values (%d, %d, %d, %d, now())"%(data[KEY.EVENT_ID], launcher_id, data[KEY.ID], data[KEY.OPERATION])
  try:
    dbhelper.execute(sql)
  except:
    return False

  #
  # trust and reputation compute here.
  #
  return True


'''
add a new comment to a help event.
@params includes event_id, represents comment belongs to which event,
                 author, user's id, author of comment,
                 content, content of comment.
@return new comment id if succeed,
        -1 otherwise.
'''
def add_comment(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return -1
  if KEY.CONTENT not in data:
    return -1
  sql = "insert into comment (event_id, author, content, time) values (%d, %d, '%s', now())"
  try:
    comment_id = dbhelper.insert(sql%(data[KEY.EVENT_ID], data[KEY.ID], data[KEY.CONTENT]))
    return comment_id
  except:
    return -1


'''
remove a comment from a help event by author him/her self.
@params includes id, indicates author him/her self.
                 event_id, indicates which event the comment belongs to.
                 comment_id, indicates comment itself.
@return True if delete successfully,
        False if fails.
'''
def remove_comment(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data or KEY.COMMENT_ID not in data:
    return False
  sql = "delete from comment where id = %d and event_id = %d and author = %d"
  try:
    dbhelper.execute(sql%(data[KEY.COMMENT_ID], data[KEY.EVENT_ID], data[KEY.ID]))
    return True
  except:
    return False


'''
get comments of a help event.
@params event_id, id of the help event.
@return a list of comments. each comment contain all detail information.
'''
def get_comments(data):
  if KEY.EVENT_ID not in data:
    return None
  comment_list = []
  comment = {}
  sql = "select id from comment where event_id = %d order by time DESC"
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.EVENT_ID]))
    for each_result in sql_result:
      for each_id in each_result:
        comment[KEY.COMMENT_ID] = each_id
        comment = get_comment_info(comment)
        if comment is not None:
          comment_list.append(comment)
    return comment_list
  except:
    return None


'''
get detail information of a comment.
@params includes comment_id, id of comment.
@return information of comment, includes id of comment,
                                         event_id, indicates which event belongs to,
                                         author_id, author's user id,
                                         author, nickname of author,
                                         content, main body of comment,
                                         time, add time of comment.
        None indicates a fail query. Maybe the chosen comment doesn't exist.
'''
def get_comment_info(data):
  if KEY.COMMENT_ID not in data:
    return None
  sql = "select event_id, author, content, time from comment where id = %d"
  comment_info = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.COMMENT_ID]))
    if sql_result is not None:
      comment_info = {}
      comment_info[KEY.COMMENT_ID] = data[KEY.COMMENT_ID]
      comment_info[KEY.EVENT_ID] = sql_result[0]
      comment_info[KEY.AUTHOR_ID] = sql_result[1]
      comment_info[KEY.CONTENT] = sql_result[2]
      comment_info[KEY.TIME] = str(sql_result[3])
      user = {}
      user[KEY.ID] = comment_info[KEY.AUTHOR_ID]
      user = get_user_information(user)
      if user is not None:
        comment_info[KEY.AUTHOR] = user[KEY.NICKNAME]
  except:
    pass
  finally:
    return comment_info


'''
add a static relation between two users. The relation is single direction.
@params includes two users' id, one is called id, the other called user_id.
parameter type indicates type of static relation. two users in one direction could only have one type of relation.
                 type:  0 indicates family relation.
                        1 indicates geography relation.
                        2 indicates career, interest and general friend relation.
@return True if successfully adds.
        False otherwise.
'''
def add_static_relation(data):
  if KEY.ID not in data or KEY.USER_ID not in data or KEY.TYPE not in data:
    return False
  sql = "replace into static_relation (user_a, user_b, type, time) values (%d, %d, %d, now())"
  try:
    n = dbhelper.execute(sql%(data[KEY.ID], data[KEY.USER_ID], data[KEY.TYPE]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


'''
remove a static relation of two user.
@params includes two users' id, one is called id, the other called user_id.
@return True if successfully removes.
        False otherwise.
'''
def remove_static_relation(data):
  if KEY.ID not in data or KEY.USER_ID not in data:
    return False
  sql = "delete from static_relation where user_a = %d and user_b = %d"
  try:
    n = dbhelper.execute(sql%(data[KEY.ID], data[KEY.USER_ID]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


