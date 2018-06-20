# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



class JdPipeline(object):
    def __init__(self):
        self.f = open("comments.txt","w")
        self.cnt = 0

    def process_item(self, item, spider):
        self.cnt+=1
        self.f.write("#"+str(self.cnt)+"\n")
        self.f.write("id:"+str(item["id"])+"\n")
        self.f.write("content:"+item["content"]+"\n")
        self.f.write("score:"+str(item["score"])+"\n")
        self.f.write("time:"+item["time"]+"\n")
        self.f.write('\n')

        return item

    def close_spider(self,spider):
        self.f.close()