# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from databaseAPI import Singleton
from spiderControler import SpiderControler
from articleControler import ArticleControler
from keywordControler import KeywordControler

class EducrawlercrawlerservicePipeline:
  def process_item(self, item, spider):
    return item

class DemoPipeline:
  def __init__(self) -> None:
    self.databaseAPI = Singleton()
  
  def open_spider(self, spider):
    pass
  
  def close_spider(self, spider):
    if spider.spider_type == "demo":
      self.databaseAPI.updateSpiderWhenClosingViaURl(spider.start_urls[0])
    #print("Crawl Url " + spider.start_urls[0] + " Completed!")
    #print("Spider Pineline Is Closing!")

    #pass
  
  def process_item(self, item, spider):
    if item["crawlerType"] != "demo":
      return item
    #print("Demo Pipeline is working!")
    
    isExisted = self.databaseAPI.getArticleByUrl(item["url"])
    #print(isExisted)
    
    # Process Data
    title = ""
    if item["title"] is not None: 
      title = item["title"].replace("'", "").replace('"', '')
    
    # Save
    if isExisted[0] == True:
      self.databaseAPI.editArticle(
        article_id=isExisted[1]["Id"],
        title=title,
        domain=item["domain"],
        url=item["url"],
        content=item["reformatted_content"],
      )
    else:
      self.databaseAPI.createArticle(
        title=title,
        domain=item["domain"],
        url=item["url"],
        content=item["reformatted_content"],        
      )
      
    #print("Save Success")
    return item
  
class WebpagePineline:
  def __init__(self) -> None:
    self.databaseAPI = Singleton()
    self.spiderControler = SpiderControler()
  
  def open_spider(self, spider):
    if spider.spider_type == "webpage":
      self.spiderControler.openSpider(spider.spider_db_id)
  
  def close_spider(self, spider):
    if spider.spider_type == "webpage":
      self.spiderControler.closeSpider(spider.spider_db_id)
      self.spiderControler.writeSpiderHistory(spider.spider_db_id)
      #self.databaseAPI.updateSpiderWhenClosingViaID(spider.spider_db_id)
  
  def process_item(self, item, spider):
    if item["crawlerType"] != "webpage":
      return item
    
    isExisted = self.databaseAPI.getArticleByUrl(item["url"])
    
    title = ""
    if item["title"] is not None: 
      title = item["title"].replace("'", "").replace('"', '')
    
    # Save
    if isExisted[0] == True:
      self.databaseAPI.editArticle(
        article_id=isExisted[1]["Id"],
        title=title,
        domain=item["domain"],
        url=item["url"],
        content=item["reformatted_content"],
        spider_id=spider.spider_db_id
      )
    else:
      self.databaseAPI.createArticle(
        title=title,
        domain=item["domain"],
        url=item["url"],
        content=item["reformatted_content"],       
        spider_id=spider.spider_db_id 
      )
      
    return item
  
class WebsitePineline:
  def __init__(self) -> None:
    self.databaseAPI = Singleton()
    self.spiderControler = SpiderControler()
    self.keywordControler = KeywordControler()
    self.articleControler = ArticleControler()
  
  def open_spider(self, spider):
    if spider.spider_type == "website":
      self.spiderControler.openSpider(spider.spider_db_id)
  
  def close_spider(self, spider):
    if spider.spider_type == "website":
      self.spiderControler.closeSpider(spider.spider_db_id)
      #self.spiderControler.writeSpiderHistory(spider.spider_db_id)
      self.spiderControler.writeWebsiteSpiderHistory(
        spider_id=spider.spider_db_id,
        crawlSuccess=spider.crawl_success,
        crawlFail=spider.crawl_fail
      )

      #self.databaseAPI.updateSpiderWhenClosingViaID(spider.spider_db_id)
      total_article = self.databaseAPI.getSpiderTotalAriticle(spider_id=spider.spider_db_id)
      if total_article[0] == True:
        self.databaseAPI.setSpiderTotalAriticle(spider_id=spider.spider_db_id, total_article=total_article[1])
      self.databaseAPI.increaseWebsiteSpiderCrawl(spider_id=spider.spider_db_id, crawl_success=spider.crawl_success, crawl_fail=spider.crawl_fail)
      
      for keyword in spider.allowed_keyword:
        id = self.keywordControler.getKeywordIDByName(keyword)
        if id != - 1:
          count = self.keywordControler.getTotalArticleContainKeyword(id)
          self.keywordControler.setTotalArticleContainKeyword(id, count)
  
  def process_item(self, item, spider):
    if item["crawlerType"] != "website":
      return item
    
    isExisted = self.databaseAPI.getArticleByUrl(item["url"])
    
    title = ""
    if item["title"] is not None: 
      title = item["title"].replace("'", "").replace('"', '')
    
    # Save
    if len(item["reformatted_content"]) == 0:
      return item
    
    if isExisted[0] == True:
      res = self.databaseAPI.editArticle(
        article_id=isExisted[1]["Id"],
        title=title,
        domain=item["domain"],
        url=item["url"],
        content=item["reformatted_content"],
        spider_id=spider.spider_db_id
      )
      if res[0] == True:
        spider.crawl_success += 1
        
        for keyword in item["keywords"]:
          keyword_id = self.keywordControler.getKeywordIDByName(keyword)
          article_id = self.articleControler.getArticleIDByUrl(item["url"])
          if keyword_id != -1 and article_id != -1:
            article_id = self.keywordControler.insertKeywordToArticle(keyword_id, article_id)
      else:
        spider.crawl_fail += 1

    else:
      res = self.databaseAPI.createArticle(
        title=title,
        domain=item["domain"],
        url=item["url"],
        content=item["reformatted_content"],       
        spider_id=spider.spider_db_id 
      )
      if res[0] == True:
        spider.crawl_success += 1
        
        for keyword in item["keywords"]:
          keyword_id = self.keywordControler.getKeywordIDByName(keyword)
          article_id = self.articleControler.getArticleIDByUrl(item["url"])
          if keyword_id != -1 and article_id != -1:
            article_id = self.keywordControler.insertKeywordToArticle(keyword_id, article_id)
      else:
        spider.crawl_fail += 1
      
    return item