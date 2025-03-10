# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import pathlib


class ImdbPipeline:
    def open_spider(self, spider):
        data_folder = pathlib.Path(__file__).parent.parent / 'data'
        try:
            if not pathlib.Path(data_folder).exists():
                pathlib.Path(data_folder).mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print('PermissionError')
        csv_file_path = pathlib.Path(__file__).parent.parent / 'data' / 'imdb.csv'

        self.file = open(csv_file_path, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            'title',
            'rating',
            'popularity',
            'year',
            'meta_score',
            'tags',
            'budget',
            'first_us_ca'
        ])
    def process_item(self, item, spider):
        self.writer.writerow([
            item['title'],
            item['rating'],
            item['popularity'],
            item['year'],
            item['meta_score'],
            item['tags'],
            item['budget'],
            item['first_us_ca']
        ])
    def close_spider(self, spider):
        self.file.close()
