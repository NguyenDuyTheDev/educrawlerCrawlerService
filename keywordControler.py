from datetime import datetime
from typing import Any
from databaseAPI import Singleton

class KeywordControler(Singleton):
  def getKeywordIDByName(self, keyword) -> int:
    sql_command = '''
      SELECT "ID"
      FROM public."Keyword"
      WHERE "Name" = '%s';         
      ''' % (keyword)   
      
    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return -1
        
      return result[0]
    except:
      return -1
  
  def insertKeywordToArticle(self, keyword_id, article_id):
    sql_command = '''
    INSERT INTO public."ArticleKeyword" ("KeywordID", "ArticleID")
    VALUES (%s, %s);
    ''' % (keyword_id, article_id)
    
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      self.cur.execute("ROLLBACK;")