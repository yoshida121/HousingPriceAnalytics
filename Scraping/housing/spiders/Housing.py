import scrapy

from housing.items import HousingItem

class HousingSpider(scrapy.Spider):
    name = 'Housing'
    allowed_domains = ['suumo.jp']
    # start_urls = ['https://suumo.jp/']
    start_urls = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&fw2=&pc=30&po1=25&po2=99&ra=013&rn=0015&ek=001519670&ek=001528860&ek=001527320&ek=001527360&ek=001527380&ek=001534900&ek=001520030&ek=001531910&ek=001519470&ek=001537270&ek=001506640&cb=0.0&ct=7.0&et=9999999&mb=0&mt=9999999&cn=9999999&kz=1&kz=2&tc=0400101&shkr1=03&shkr2=03&shkr3=03&shkr4=03']


    def parse(self, response):
        housings = response.css("div.cassetteitem")

        for house in housings:
            name = house.css("div.cassetteitem_content-title::text").extract()[0]

            age_building = house.css("li.cassetteitem_detail-col3 div::text").extract()
            age = age_building[0]
            building = age_building[1]

            rent = house.css("span.cassetteitem_other-emphasis::text").extract()[0]

            area = house.css("span.cassetteitem_menseki::text").extract()[0]

            floor_str = house.css("tr.js-cassette_link td::text").extract()
            floor_str = [self._clean(s) for s in floor_str]
            floor_str = [s for s in floor_str if s != ""]
            floor = floor_str[0]
            # print(item["floor"])

            floor_plan = house.css("span.cassetteitem_madori::text").extract()[0]
            # print(item["floor_plan"])

            address = house.css("li.cassetteitem_detail-col1::text").extract()[0]

            yield HousingItem(
                name = name,
                age = age,
                building = building,
                rent = rent,
                area = area,
                floor = floor,
                floor_plan = floor_plan,
                address = address,
            )

        next_page = response.css("p.pagination-parts a::attr(href)").extract()[-1]
        if next_page is not  None:
            next_page = response.urljoin(next_page)
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def _clean(self, x: str):
        x = x.replace("\t", "")
        x = x.replace("\n", "")
        x = x.replace("\r", "")
        return x