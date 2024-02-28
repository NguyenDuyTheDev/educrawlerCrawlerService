from educrawlerCrawlerService.spiders.demoCrawlerURL import DemoCrawlerURL
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

class Crawler:
  def __init__(
    self, 
    links = [],
    rules = [],
    type = "website",
    download_delay = 2,
    depth_limit = 3, 
    concurrent_pdomain = 8, 
    concurrent_pid = 0, 
  ) -> None:  
    self.type   = type
    self.spider = None
    self.settings = {}
    self.settings["LINKS"]                          = links
    self.settings["DOWNLOAD_DELAY"]                 = download_delay
    self.settings["DEPTH_LIMIT"]                    = depth_limit
    self.settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = concurrent_pdomain
    self.settings["CONCURRENT_REQUESTS_PER_IP"]     = concurrent_pid
    self.settings["CUSTOM_CRAWL"]                   = []
    self.custom_crawl = rules

    # Custom Rules: (tag_name, class or id, name, inner)
    
  def init_spider(self):
    if self.spider != None:
      return
    
    spider_default_setting = get_project_settings()    
    self.spider = CrawlerProcess(settings=spider_default_setting)
    #self.spider = CrawlerRunner(settings=spider_default_setting)
    self.spider.crawl(DemoCrawlerURL, link=self.settings["LINKS"][0])

  def get_settings(self):
    return self.settings

  def is_init(self):
    return self.spider != None

  def start_crawling(self):
    if self.spider == None:
      return
    
    self.spider.start()
    self.spider.stop()
    print('Crawl Completed')
    
def main():
  url = "https://giaoduc.net.vn/sinh-vien-nao-thuoc-dien-duoc-mien-giam-hoc-phi-trong-nam-2024-post240994.gd"

  user_settings = {}
  user_settings["LINKS"]                          = [url] 
  user_settings["DOWNLOAD_DELAY"]                 = 2
  user_settings["DEPTH_LIMIT"]                    = 3
  user_settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = 8
  user_settings["CONCURRENT_REQUESTS_PER_IP"]     = 0
  rules = []
  rules.append(("p", None, None, None, None))
  
  crawler = Crawler(
    links             =user_settings["LINKS"],
    rules             =rules,
    type              ="demo",
    download_delay    =user_settings["DOWNLOAD_DELAY"],
    depth_limit       =user_settings["DEPTH_LIMIT"],
    concurrent_pdomain=user_settings["CONCURRENT_REQUESTS_PER_DOMAIN"],
    concurrent_pid    =user_settings["CONCURRENT_REQUESTS_PER_IP"]
  )
  crawler.init_spider()
  crawler.start_crawling()    
  
if __name__ == '__main__':
  main()
  
#scrapy crawl demoCrawlerURL -a link='https://giaoduc.net.vn/de-kiem-tra-giua-ky-cuoi-ky-trong-huyen-tinh-chung-de-co-con-phu-hop-post240982.gd'
#curl http://localhost:6800/schedule.json -d project=default -d spider=demoCrawlerURL -d link='https://giaoduc.net.vn/sinh-vien-nao-thuoc-dien-duoc-mien-giam-hoc-phi-trong-nam-2024-post240994.gd'


#Spider 15
#scrapy crawl demoCrawlerURL -a link='https://giaoduc.net.vn/mot-so-dia-phuong-lam-khong-dung-quy-dinh-ve-tuyen-thang-uu-tien-vao-lop-10-post241074.gd'

#scrapy crawl WebpageSpider -a spider_id=15 -a link='https://giaoduc.net.vn/mot-so-dia-phuong-lam-khong-dung-quy-dinh-ve-tuyen-thang-uu-tien-vao-lop-10-post241074.gd'
#scrapy crawl WebpageSpider -a spider_id=16 -a link='https://giaoduc.net.vn/chi-tiet-diem-chuan-cac-nganh-cua-hoc-vien-tai-chinh-5-nam-qua-post241010.gd'
#scrapy crawl WebsiteSpider -a spider_id=16 -a link='https://giaoduc.net.vn/chi-tiet-diem-chuan-cac-nganh-cua-hoc-vien-tai-chinh-5-nam-qua-post241010.gd'

#curl https://educrawlercrawlerservice.onrender.com//schedule.json -d project=default -d spider=WebsiteSpider -d link='https://giaoduc.net.vn/chi-tiet-diem-chuan-cac-nganh-cua-hoc-vien-tai-chinh-5-nam-qua-post241010.gd' -d spider_id=16

#scrapy crawl WebsiteSpider -a spider_id=16 -a link='https://giaoduc.net.vn/chi-tiet-diem-chuan-cac-nganh-cua-hoc-vien-tai-chinh-5-nam-qua-post241010.gd' -a graphDeep=1 -a delay=2.0