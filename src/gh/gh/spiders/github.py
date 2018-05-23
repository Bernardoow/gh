# -*- coding: utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = [
        'https://github.com/Bernardoow/Elm-SqlAlchemy-Replace',
    ]

    def parse(self, response):
        url = response.request.url.replace("https://github.com/", "")
        if len(response.css("#raw-url")):
            extensions_file_url = response.request.url.split('.')[-1]
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

        seletor_link = 'table.files.js-navigation-container tbody' \
            ' tr.js-navigation-item td.content a'

        yield {
            'url': url,
            'qty_lines': 0,
            'size_files': 0,
            'is_file': 0,
            'extensions_file_url': '-'
        }

        for a in response.css(seletor_link):
            yield response.follow(a, callback=self.parse)
