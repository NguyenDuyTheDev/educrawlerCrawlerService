import psycopg2
from datetime import datetime
from typing import Any
from databaseAPI import Singleton

class SpiderControler(Singleton):
  def openSpider(self, spider_id):
    current = datetime.now()
    reformatted_current = current.strftime("%m-%d-%Y %H:%M:%S")
    sql_command = '''
      UPDATE public."Spider"
      SET 
      "Status" = 'Running',
      "CrawlStatus" = 'Good', 
      "LastRunDate" = TIMESTAMP '%s',
      "LastEndDate" = TIMESTAMP '%s'
      WHERE "ID" = %s;            
      ''' % (reformatted_current, reformatted_current, spider_id)   
    
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      self.cur.execute("ROLLBACK;")
        
  def closeSpider(self, spider_id):
    sql_command = '''
    SELECT *
    FROM public."Spider"
    WHERE public."Spider"."ID" = %s;
    ''' % (spider_id)
  
    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return
      
      current = datetime.now()
      reformatted_current = current.strftime("%m-%d-%Y %H:%M:%S")
      totalRunTime = current - result[4]
      totalRunTimeAsInt = totalRunTime.seconds + result[6]
        
      sql_command = '''
      UPDATE public."Spider"
      SET "JobId" = '',
      "Status" = 'Available',
      "CrawlStatus" = 'Good', 
      "LastEndDate" = TIMESTAMP '%s',
      "RunTime" = '%s'
      WHERE "ID" = %s;            
      ''' % (reformatted_current, totalRunTimeAsInt, spider_id)   
    except:
      return
    
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      self.cur.execute("ROLLBACK;")

  def writeSpiderHistory(self, spider_id):
    sql_command = '''
    SELECT *
    FROM public."Spider"
    WHERE public."Spider"."ID" = %s;
    ''' % (spider_id)

    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return
      
      LastRunDate = result[4].strftime("%m-%d-%Y %H:%M:%S")
      LastEndDate = result[5].strftime("%m-%d-%Y %H:%M:%S")
      RunTime = result[5] - result[4]
        
      sql_command = '''
      INSERT INTO public."CrawlHistory" ("Url", "RunDate", "EndDate", "RunTime", "SpiderID")
      VALUES ('%s', TIMESTAMP '%s', TIMESTAMP '%s', %s, %s);
      ''' % (result[1], LastRunDate, LastEndDate, RunTime.seconds, spider_id)
    except:
      return
    
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      print("Write Spider History Error")
      self.cur.execute("ROLLBACK;")
      
  def writeWebsiteSpiderHistory(self, spider_id, crawlSuccess, crawlFail):
    sql_command = '''
    SELECT *
    FROM public."Spider"
    WHERE public."Spider"."ID" = %s;
    ''' % (spider_id)

    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return
      
      LastRunDate = result[4].strftime("%m-%d-%Y %H:%M:%S")
      LastEndDate = result[5].strftime("%m-%d-%Y %H:%M:%S")
      RunTime = result[5] - result[4]
        
      sql_command = '''
      INSERT INTO public."CrawlHistory" ("Url", "RunDate", "EndDate", "RunTime", "SpiderID")
      VALUES ('%s', TIMESTAMP '%s', TIMESTAMP '%s', %s, %s);
      ''' % (result[1], LastRunDate, LastEndDate, RunTime.seconds, spider_id)
    except:
      return
    
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      self.cur.execute("ROLLBACK;")
      return
    
    sql_command = '''
    SELECT *
    FROM public."CrawlHistory"
    WHERE "SpiderID" = %s
    ORDER BY "ID" DESC;
    ''' % (spider_id)

    try:
      self.cur.execute(sql_command)
      result = self.cur.fetchone()
      if not(result):
        return
        
      totalPage = crawlSuccess + crawlFail
      sql_command = '''
      INSERT INTO public."WebsiteSpiderHistory" ("ID", "TotalPage", "CrawlSuccess", "CrawlFail")
      VALUES (%s, %s, %s, %s);
      ''' % (result[0], totalPage, crawlSuccess, crawlFail)
    except:
      return
    
    try:
      self.cur.execute(sql_command)
      self.connection.commit()
    except:
      print("Write Spider History Error")
      self.cur.execute("ROLLBACK;")