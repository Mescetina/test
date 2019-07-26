# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class ZhaopinPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect("127.0.0.1","root","yuyugood","Zhaopin")
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("use Zhaopin")
        search = f"SELECT * FROM Job WHERE job_url = '{item['job_url']}'"
        self.cursor.execute(search)
        result = self.cursor.fetchone()
        if result == None:
            insert = f"""INSERT INTO Job(job_url, job_title, company, salary, location, post_time, type_of_empl, work_exp, min_edu_qual,
                         num_of_ppl, occup_type, job_desc, co_profile) VALUES ('{item['job_url']}', '{item['job_title']}', '{item['company']}',
                         '{item['salary']}', '{item['location']}', '{item['post_time']}', '{item['type_of_empl']}', '{item['work_exp']}',
                         '{item['min_edu_qual']}', '{item['num_of_ppl']}', '{item['occup_type']}', '{item['job_desc']}', '{item['co_profile']}')"""
            self.cursor.execute(insert)
            self.connection.commit()
        return item
