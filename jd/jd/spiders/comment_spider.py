import scrapy,json,re
from jd.items import CommentItem

'''
usage：
cd jd
scrapy crawl comment_spider 
'''

class CommentSpider(scrapy.Spider):
    name = "comment_spider"
    # allowed_domains = ["jd.com"]
    product_id = input("请输入商品id：")
    # 26482700253 5155905
    if(not product_id.isdigit()):
        print("输入id有误！")
        exit(-1)

    url = "https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=6&page=0&pageSize=10".format(product_id)
    start_urls = []
    start_urls.append(url)

    def parse(self, response):
        if(response.status == 200):
            js = json.loads(response.body.decode("gbk"))
            comments = js["comments"]
            max_page = int(js["maxPage"])
            url = response.url
            now_page = int(re.findall("page=(\w+)", url)[0])

            if (now_page + 1 <= max_page):
                url = re.sub(r"page=\d+", "page=" + str(now_page + 1), url)
                yield scrapy.Request(url, callback=self.parse)

            for each in comments:
                item = CommentItem()

                item["id"] = each["id"]
                item["content"] = each["content"]
                item["score"] = each["score"]
                item["time"] = each["creationTime"]

                yield item
