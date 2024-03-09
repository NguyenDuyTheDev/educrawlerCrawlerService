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
      
  def getTotalArticleContainKeyword(self, keyword_id):
    sql_command = '''
      SELECT count(*)
      FROM public."ArticleKeyword"
      WHERE "KeywordID" = %s;         
      ''' % (keyword_id)   
      
    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return -1
        
      return result[0]
    except:
      return -1
    
  def setTotalArticleContainKeyword(self, keyword_id, total):
    sql_command = '''
        UPDATE public."Keyword"
        SET "TotalArticles" = %s
        WHERE "ID" = %s;            
      ''' % (total, keyword_id)   
      
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      self.cur.execute("ROLLBACK;")