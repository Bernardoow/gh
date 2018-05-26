# -*- coding: utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = []

    def parse(self, response):
        url = response.request.url.replace("https://github.com/", "")
        if len(response.css("#raw-url")):
            pieces = response.request.url.split('/')
            extensions_file_url = pieces[-1].split('.')[-1]
            quantity_lines = response.\
                css("div.file-info::text").\
                re_first(r"(\d+) lines")

            size_file, unit = response.\
                css("div.file-info::text").\
                re(r"(\d+\.*\d*)+ (Bytes|KB|MB)")

            yield {
                'url': url,
                'qty_lines': quantity_lines or 0,
                'size_files': size_file,
                'unit': unit,
                'is_file': 1,
                'extensions_file_url': extensions_file_url
            }

        else:

            yield {
                'url': url,
                'qty_lines': 0,
                'size_files': 0,
                'unit': '-',
                'is_file': 0,
                'extensions_file_url': '-'
            }

        seletor_link = 'table.files.js-navigation-container tbody' \
            ' tr.js-navigation-item td.content a'

        for a in response.css(seletor_link):
            yield response.follow(a, callback=self.parse)
