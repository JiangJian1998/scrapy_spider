import scrapy,json,re,os
from jd.items import CommentItem
import scrapy.settings,scrapy.crawler
'''
usage：
cd jd
scrapy crawl comment_spider 
'''

class CommentSpider(scrapy.Spider):
    name = "comment_spider"
    # allowed_domains = ["jd.com"]

    def __init__(self, settings, *args, **kwargs):
        super(CommentSpider, self).__init__(*args, **kwargs)
        save_dir = settings.get('SAVE_DIR')#获取存储路径
        # 创建存储文件夹
        if not os.path.exists(save_dir):
            print("创建目录：" + save_dir)
            os.mkdir(save_dir)
        # 输入商品id并且存入到pid变量
        product_id = input("请输入商品id：")  # example id: 26482700253 5155905
        if (not product_id.isdigit()):
            print("输入id有误！")
            exit(-1)
        self.pid = product_id
        # 初始化爬取列表
        self.start_urls = []
        for i in range(1, 4):  # 遍历好评差评中评
            url = "https://sclub.jd.com/comment/productPageComments.action?" \
                  "productId={}&score={}&sortType=6&page=0&pageSize=10" \
                .format(product_id, i)
            self.start_urls.append(url)

    #重写from_crawler方法，方便使用settings
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider


    # 爬取处理
    def parse(self, response):
        if(response.status == 200):
            js = json.loads(response.body.decode("gbk"))#使用json模块处理
            comments = js["comments"]#当前json地址所有评论
            max_page = int(js["maxPage"])
            url = response.url
            now_page = int(re.findall("page=(\w+)", url)[0])

            # 将下一个json地址加入爬取队列，直到达到最大页
            if (now_page + 1 <= max_page):
                url = re.sub(r"page=\d+", "page=" + str(now_page + 1), url)
                yield scrapy.Request(url, callback=self.parse)

            # 将目标信息保存
            for each in comments:
                item = CommentItem()

                item["id"] = each["id"]
                item["content"] = each["content"]
                item["score"] = each["score"]
                item["time"] = each["creationTime"]

                yield item

