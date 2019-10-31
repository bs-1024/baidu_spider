# -*- encoding:utf-8 -*-

"""
@python: 3.7
@Author: xiaobai_IT_learn
@Time: 2019-10-31 10:00
"""
import os
import re
import threading
import time
from queue import Queue
import requests

IMAGE_PATH = './baidu_image_threading'


class BaiduImageSpider(object):
    def __init__(self, key_word):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36'
        }
        self.key_word = key_word
        self.url_queue = Queue()
        self.num = 1
        self._file()

    def _file(self):
        """
        创建文件夹
        :return:
        """
        if not os.path.exists(IMAGE_PATH):
            os.mkdir(IMAGE_PATH)

    def get_url_list(self):
        """
        url列表
        :return:
        """
        for i in range(30):
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result' \
                  '&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={}' \
                  '&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=girl&pn={}&rn=30'\
                    .format(self.key_word, self.key_word, i*30)
            self.url_queue.put(url)

    def spider_baidu_image(self):
        """
        爬虫
        :param url:
        :return:
        """
        while True:
            url = self.url_queue.get()
            html = requests.get(url, headers=self.headers)
            html_str = html.content.decode()
            image_list = re.findall(r"\"thumbURL\":\"(.*?)\",\"middleURL\"", html_str)
            for image_url in image_list:
                try:
                    content = requests.get(image_url, headers=self.headers).content
                except Exception as e:
                    print(e)
                    continue
                file_path = IMAGE_PATH + '/' + str(self.num) + '.jpg'
                print(self.num)
                with open(file_path, 'wb') as f:
                    f.write(content)
                self.num += 1
            self.url_queue.task_done()

    def run(self):
        thread_list = []
        t_url = threading.Thread(target=self.get_url_list, daemon=True)
        thread_list.append(t_url)
        for i in range(3):
            t_spider = threading.Thread(target=self.spider_baidu_image, daemon=True)
            thread_list.append(t_spider)
        for t in thread_list:
            t.start()
        self.url_queue.join()


if __name__ == '__main__':
    key_word = input('输入要查询的关键字：')
    start_time = time.time()
    spider_baidu_image = BaiduImageSpider(key_word)
    spider_baidu_image.run()
    print(time.time() - start_time)
























