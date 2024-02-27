# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from databaseAPI import Singleton

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
  
  def open_spider(self, spider):
    pass
  
  def close_spider(self, spider):
    if spider.spider_type == "webpage":
      self.databaseAPI.updateSpiderWhenClosingViaID(spider.spider_db_id)
  
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
  
  def open_spider(self, spider):
    pass
  
  def close_spider(self, spider):
    if spider.spider_type == "website":
      self.databaseAPI.updateSpiderWhenClosingViaID(spider.spider_db_id)
  
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