import psycopg2
from datetime import datetime
from typing import Any
from databaseAPI import Singleton

class ArticleControler(Singleton):
  def getArticleIDByUrl(self, url) -> int:
    sql_command = '''
      SELECT "Id"
      FROM public."Article"
      WHERE "Url" = '%s';         
      ''' % (url)   
      
    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return -1
        
      return result[0]
    except:
      return -1