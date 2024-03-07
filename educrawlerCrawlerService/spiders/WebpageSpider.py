from typing import Any, Optional
import scrapy
from scrapy.http import Response
from scrapy.utils.log import configure_logging
from urllib.parse import urlparse, urljoin
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from educrawlerCrawlerService.utils import CssSelectorGenerator, CSSAttributeType, CSSContentType, countExistedTimes, removeEmptySpaceParagraph, removeHTMLTag, removeEmptyLine, countLetterInParagraph, countExistedTimesTokenize
import math

from scrapy import signals

class WebpageSpider(scrapy.Spider):
  name = "WebpageSpider"
  allowed_domains = []
  start_urls = []
  visited = []
  upcomming = []
  allowed_file_format = []
  allowed_keyword = [
    "giáo dục",
    "đại học",
    "trường",
    "học",
    "dạy",
    "phổ thông",
    "tiểu học",
    "mầm non",
    "giáo viên",
    "đào tạo",
    "nghề",
    "sinh viên",
    "học sinh",
    "ngành",
    "khoa",
    "trung học",
    "môn",
    "ngữ văn",
    "bài tập",
    "chuyên",
    "học đường",
    "trải nghiệm",
    "vận động",
    "kĩ năng",
    "kiến trúc",
    "học tập",
    "kĩ năng mềm",
    "rèn luyện",
    "giảng viên",
    "sư phạm",
    "tư duy",
    "phân tích",
    "thực nghiệm",
    "giải quyết vấn đề",
    "toán",
    "tự học",
    "hướng dẫn",
    "đánh giá",
    "kết quả",
  ]

  basic_keyword = [
    "giáo dục",
    "đại học",
    "trường",
    "học",
    "dạy",
    "phổ thông",
    "tiểu học",
    "mầm non",
    "giáo viên",
    "đào tạo",
    "nghề",
    "sinh viên",
    "học sinh",
    "ngành",
    "khoa",
    "trung học",
    "môn",
    "ngữ văn",
    "bài tập",
    "chuyên",
    "học đường",
    "trải nghiệm",
    "vận động",
    "kĩ năng",
    "kiến trúc",
    "học tập",
    "kĩ năng mềm",
    "rèn luyện",
    "giảng viên",
    "sư phạm",
    "tư duy",
    "phân tích",
    "thực nghiệm",
    "giải quyết vấn đề",
    "toán",
    "tự học",
    "hướng dẫn",
    "đánh giá",
    "kết quả",
  ]

  uncrawlable_link = [
    "mailto", "javascript", "commentbox", "tel"
  ] 
  
  custom_settings = {
    'DEPTH_LIMIT': 3
  }
  
  crawl_rule = []
  
  def __init__(
    self, 
    spider_id: int, 
    link: str, 
    keywords: str = "",
    name: Optional[str] = None, 
    crawlRule: str = "",
    **kwargs: Any
    ):   
    super(WebpageSpider, self).__init__(name, **kwargs)

    #self.allowed_file_format = user_settings["ALLOWED_FILE_FORMAT"]

    self.start_urls.append(link)
        
    for url in self.start_urls:
      parsed_uri = urlparse(url)
      domain = '{uri.netloc}'.format(uri=parsed_uri)
      self.allowed_domains.append(domain)
          
    self.download_delay                                     = 2
    self.spider_db_id = spider_id
    self.spider_type = "webpage"
    #self.custom_crawl_rules = custom_crawl_rules
    
    try:
      keywordsAsList = keywords.split(',')
      print(keywordsAsList, type(keywordsAsList))
      if len(keywordsAsList) > 0:
        self.allowed_keyword = keywordsAsList
    except:
      self.allowed_keyword = self.basic_keyword
    print(self.allowed_keyword)
    
    crawlRuleAsList = crawlRule.split(",")
    self.crawl_rule = crawlRuleAsList
    print(self.crawl_rule)

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = super(WebpageSpider, cls).from_crawler(crawler, *args, **kwargs)
    crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    return spider
    
  def start_requests(self):
    for url in self.start_urls:
      yield scrapy.Request(
        url=url, 
        callback=self.parse,
        errback=self.errback_httpbin,
      )
        
  def spider_closed(self, spider):
    pass
          
  def parse(self, response):
    converted_headers = self.convert(response.headers)
    
    if ("text/html" in converted_headers["Content-Type"]):
      academic_keywords = 0
    
      # Crawl Basic Data
      websiteTitle = response.css('title::text').get()
      content   = response.css('p').getall()
      
      user_define_content = []
      for rule in self.crawl_rule:
        if response.css(rule):
          user_define_content = user_define_content + response.css(rule).getall()
      content = content + user_define_content
          
      # Content Checking and Reformatted
      found_keywords = []
      raw_content = " ".join(content)
      raw_content = removeHTMLTag(raw_content)
      raw_content = removeEmptyLine(raw_content)
      raw_content = removeEmptySpaceParagraph(raw_content)
      total_words = countLetterInParagraph(raw_content)
      minimum_keywords = math.floor(total_words * 1.0 / 200)

      # Check academic content      
      for keyword in self.allowed_keyword:
        count = countExistedTimesTokenize(websiteTitle, keyword)
        if count > 0:
          found_keywords.append(keyword)
          academic_keywords += count
      
        count = countExistedTimesTokenize(raw_content, keyword)
        if count > minimum_keywords:
          found_keywords.append(keyword)
          academic_keywords += count
          
      # Check before save
      if (len(self.allowed_keyword) == 0 or (len(self.allowed_keyword) > 0 and academic_keywords > 0)) and (len(raw_content) > 0):
        items = {
          "crawlerType": "webpage",
          "domain": self.allowed_domains[0],
          "url": response.url,
          "academic_keyword": academic_keywords,
          "keywords": found_keywords,
          "title": websiteTitle,
          "reformatted_content": raw_content,
          "total_words": total_words,
          "minimum_keywords": minimum_keywords,
          "spider_id": self.spider_db_id
        }
        yield items
        
  def errback_httpbin(self, failure):
    # log all failures
    self.logger.error(repr(failure))

    if failure.check(HttpError):
      # these exceptions come from HttpError spider middleware
      # you can get the non-200 response
      response = failure.value.response
      self.logger.error("HttpError on %s", response.url)

    elif failure.check(DNSLookupError):
      # this is the original request
      request = failure.request
      self.logger.error("DNSLookupError on %s", request.url)

    elif failure.check(TimeoutError, TCPTimedOutError):
      request = failure.request
      self.logger.error("TimeoutError on %s", request.url)
    
  def convert(self, data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, list):   return data.pop().decode('ascii')
    if isinstance(data, dict):   return dict(map(self.convert, data.items()))
    if isinstance(data, tuple):  return map(self.convert, data)
    return data