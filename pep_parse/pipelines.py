import csv
import datetime as dt

from collections import defaultdict

from pep_parse.settings import DATETIME_FORMAT


class PepParsePipeline:

    def open_spider(self, spider):
        self.status_count_dict = defaultdict(int)

    def process_item(self, item, spider):
        self.status_count_dict[item['status']] += 1
        return item

    def close_spider(self, spider):
        time = dt.datetime.now().strftime(DATETIME_FORMAT)
        with open(f'results/status_summary_{time}.csv', mode='w',
                  newline='', encoding='utf-8') as file:
            summary_writer = csv.writer(file)
            summary_writer.writerow(('Статус', 'Количество'))
            summary_writer.writerows(self.status_count_dict.items())
            summary_writer.writerow(
                ('Total', sum(self.status_count_dict.values()))
            )
