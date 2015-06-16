#/usr/bin/python
#-*-coding:utf-8-*-
'''
Created on Jun 14, 2015

@author: zhangchao
'''
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from TBBKAnalysis.items import TbbkanalysisItem
from scrapy.item import Item

class TBBKSpider(Spider):
    name='TBBKSpider'
    download_delay=4
    allowed_domains=['taobao.com']
    start_urls=[
        'http://s.taobao.com' 
        ]
    
    def parse(self, response):
        if response.url=='http://s.taobao.com':
            print "********************response url:%s******************" % response.url
            url="http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1#J_relative"
                
            log.msg('page 1', level=log.INFO)
            yield Request(url,callback=self.parse)
            
        else:
            sel=Selector(response)
            shops=sel.xpath('//div[@class="grid"]/div[@class="items g-clearfix"]')
            print "*************response url:%s******************" %response.url
            print "*************shops :*****************" ,shops
            for shop in shops:
                item=TbbkanalysisItem()
                shop_name = shop.xpath('div[@class="row row-3 g-clearfix"]/div[@class="shop"]/a/span[last()]/text()').extract()
                shop_address =shop.xpath('div[@class="row row-3 g-clearfix"]/div[@class="shop"]/div[@class="location"]/text()').extract()
                shop_istmall =shop.xpath('div[@class="row row-4"]/div[@class="feature-icons icon-has-more"]/ul/text()').extract()
                shop_istmall= eval(shop_istmall[0])
                
                if shop_istmall['isTmall']==1:
                    shop_istmall='is_tmall'
                else:
                    shop_istmall='not_tmall'
                    
                goods_price = shop.xpath('div[@class="irow row-1 g-clearfix"]/div[@class="price g_price g_price-highlight"]/text()').extract()
                #取出其中的空格
                goods_price = goods_price[0].strip()
                goods_sale_num = shop.xpath('div[@class="irow row-1 g-clearfix"]/div[@class="deal-cnt"]/text()').extract()
                goods_sale_num=''.join([s for s in goods_sale_num[0] if s.isdigit()])
                goods_name = shop.xpath('div[@class="row row-2 title"]/a/span[@class="H"]').extract()
                
                #编码
                item["shop_name"] = [n.encode("utf-8") for n in shop_name]
                item["shop_address"] = [a.encode("utf-8") for a in shop_address]
                #非list类型
                item["shop_istmall"] = shop_istmall
                item["goods_price"] = goods_price
                item["goods_sale_num"] = goods_sale_num
                item["goods_name"] = [na.encode("utf-8") for na in goods_name]
                
                yield  item
                    
#             next_page_urls = [
#                 "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=176",
#                 "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=132",
#                 "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=88",
#                 "http://s.taobao.com/search?spm=a230r.1.8.3.5li7hV&promote=0&sort=sale-desc&%22_%5C%22initiative_id=tbindexz_20140701&tab=all&q=%C1%AC%D2%C2%C8%B9%CF%C4&suggest=0_1&s=44"
#                 ]
#             print "*******************next page**********************"
#             log.msg("Next page", level=log.INFO)
#             
#             
#             for next_page_url in next_page_urls:
#                 yield Request(next_page_url, callback=self.parse)      
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                

                