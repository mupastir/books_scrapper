# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from bookstoscrapy import settings


def write_to_csv(item):
    writer = csv.writer(open(settings.csv_file_path, 'a'),
                            lineterminator='\n')
    writer.writerow([item[key] for key in item.keys()])


class WriteToCsv(object):
    item_counter = 0

    def process_item(self, item, spider):
        write_to_csv(item)
        return item
