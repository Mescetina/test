import scrapy
from zhaopin.items import ZhaopinItem


class ZhaopinSpider(scrapy.Spider):
    name = "zhaopin"

    def start_requests(self):
        start_url = "https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%91%98&sm=0&p=1"
        yield scrapy.Request(start_url,cookies = {'ZP_OLD_FLAG': "true"},callback = self.parse)

    def parse(self, response):
        job_urls = response.xpath("//td[contains(@class,'zwmc')]//a[1]/@href").extract()
        for job_url in job_urls:
            yield scrapy.Request(job_url,callback = self.parse_job)
        next_page = response.xpath("//li[contains(@class,'pagesDown-pos')]/a/@href").extract_first()
        if next_page != None:
            yield scrapy.Request(next_page,callback = self.parse)

    def parse_job(self, response):
        item = ZhaopinItem()
        item['job_url'] = response.url
        item['job_title'] = response.xpath("//div[contains(@class,'inner-left fl')]/h1/text()").extract_first()
        item['company'] = response.xpath("//div[contains(@class,'inner-left fl')]/h2//text()").extract_first().strip()
        item['salary'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[1]/strong/text()").extract_first().strip()
        item['location'] = "".join(response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[2]/strong//text()").extract())
        item['post_time'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[3]/strong//text()").extract_first()
        item['type_of_empl'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[4]/strong/text()").extract_first()
        item['work_exp'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[5]/strong/text()").extract_first()
        item['min_edu_qual'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[6]/strong/text()").extract_first()
        item['num_of_ppl'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[7]/strong/text()").extract_first().strip()
        item['occup_type'] = response.xpath("//div[contains(@class,'terminalpage-left')]/ul/li[8]/strong//text()").extract_first()
        item['job_desc'] = self.parse_job_desc(response)
        item['co_profile'] = self.parse_co_profile(response)
        yield item

    def parse_job_desc(self, response):
        job_desc_list = response.xpath("//div[contains(@class,'terminalpage-main clearfix')]/div/div[1]//text()[not(ancestor::a)]").extract()
        for i in range(len(job_desc_list)):
            job_desc_list[i] = " ".join(job_desc_list[i].replace("'","\\'").split())
        return " ".join([line.strip() for line in job_desc_list if len(line.strip()) > 0])

    def parse_co_profile(self, response):
        co_profile_list = response.xpath("//div[contains(@class,'terminalpage-main clearfix')]/div/div[2]/*[not(self::h5)]//text()").extract()
        for i in range(len(co_profile_list)):
            co_profile_list[i] = " ".join(co_profile_list[i].replace("'","\\'").split())
        return " ".join([line.strip() for line in co_profile_list if len(line.strip()) > 0])
