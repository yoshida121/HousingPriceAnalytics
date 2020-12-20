import scrapy
import numpy as np

from housing.items import HousingItem

class HousingSpider(scrapy.Spider):
    name = 'Housing_backup'
    allowed_domains = ['suumo.jp']
    # start_urls = ['https://suumo.jp/']
    start_urls = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&fw2=&pc=30&po1=25&po2=99&ra=013&rn=0015&ek=001519670&ek=001528860&ek=001527320&ek=001527360&ek=001527380&ek=001534900&ek=001520030&ek=001531910&ek=001519470&ek=001537270&ek=001506640&cb=0.0&ct=7.0&et=9999999&mb=0&mt=9999999&cn=9999999&kz=1&kz=2&tc=0400101&shkr1=03&shkr2=03&shkr3=03&shkr4=03']

    _duplicate_keys = ["area", "floor", "floor_plan", "rent"]

    def parse(self, response):
        # items = np.emptu(len())

        housings = response.css("div.cassetteitem")
        # print("-"*10 + "  " + "-"*10)
        # print(housings)
        # print("-"*10 + "  " + "-"*10)

        for house in housings:
            item = HousingItem()
            # delete_strings = ["\r", "\t", "\n"]

            item["name"] = house.css("div.cassetteitem_content-title::text").extract()[0]
            # print(item["name"])

            age_building = house.css("li.cassetteitem_detail-col3 div::text").extract()
            item["age"] = age_building[0]
            item["building"] = age_building[1]
            # print(item["tikunen"])

            item["rent"] = house.css("span.cassetteitem_other-emphasis::text").extract()
            # print(item["rent"])

            item["area"] = house.css("span.cassetteitem_menseki::text").extract()

            floor_str = house.css("tr.js-cassette_link td::text").extract()
            floor_str = [self._clean(s) for s in floor_str]
            floor_str = [s for s in floor_str if s != ""]
            item["floor"] = floor_str
            # print(item["floor"])

            item["floor_plan"] = house.css("span.cassetteitem_madori::text").extract()
            # print(item["floor_plan"])

            item["address"] = house.css("li.cassetteitem_detail-col1::text").extract()[0]
            # print(item["address"])

            item = self._split_duplicate(item)
            # print(item)
            yield item[0]

        # next_page = response.css("p.pagination-parts a::attr(href)").extract_first()
        # # print(next_page)
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)

        #     yield scrapy.Request(next_page, callback=self.parse)

    
    def _clean(self, x: str):
        x = x.replace("\t", "")
        x = x.replace("\n", "")
        x = x.replace("\r", "")
        return x

    def _split_duplicate(self, add: dict) -> list:
        add_items = []
        max_length = np.max([len(add[key]) for key in self._duplicate_keys])
    
        for i in range(max_length):
            _tmp_dict = {}
            for key in add.keys():
                if key in self._duplicate_keys:
                    _tmp_dict[key] = add[key][i]
                else:
                    _tmp_dict[key] = add[key]
            add_items.append(_tmp_dict)

        return add_items