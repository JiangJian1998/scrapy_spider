# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

class JdPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings,crawler.spider)

    def __init__(self,settings,spider):
        save_dir = settings.get("SAVE_DIR")
        pid = spider.pid
        # 商品文件夹路径
        self.dirname = save_dir+pid+'/'
        if not os.path.exists(self.dirname):
            print("创建目录："+self.dirname)
            os.mkdir(self.dirname)

    def process_item(self, item, spider):
        # 定义存储方式，可以任意定制

        pid = spider.pid#获取商品id
        # 默认评论表，若在表中则不会爬取
        ban_default =["您没有填写内容，默认好评",
                      "此用户未填写评价内容"]
        for ban in ban_default:
            if(str(item["content"]) == ban):
                return item

        # 不同评分文件写入
        file_name = pid+"-"+str(item["score"])+".txt"
        fpath = self.dirname+file_name
        f = open(fpath, "a+")
        f.write("content:"+item["content"]+"\n")
        f.write("score:"+str(item["score"])+"\n")
        f.close()
        # all文件写入
        file_name = pid+"-all.txt"
        fpath = self.dirname + file_name
        f = open(fpath, "a+")
        f.write("content:" + item["content"] + "\n")
        f.write("score:" + str(item["score"]) + "\n")
        f.close()

        # 可以使用各种自定义存储方式，如
        # self.cnt+=1
        # self.f.write("#"+str(self.cnt)+"\n")
        # self.f.write("id:"+str(item["id"])+"\n")
        # self.f.write("content:"+item["content"]+"\n")
        # self.f.write("score:"+str(item["score"])+"\n")
        # self.f.write("time:"+item["time"]+"\n")
        # self.f.write('\n')

        return item

    def close_spider(self,spider):
        # self.f.close()
        pass

