import os
from bs4 import BeautifulSoup
import re

class index:

    def index_parser(self):
        if self.soup.find('ja:if') is not None:
            self.soup_ja_if()
        elif self.soup.find('ja:else') is not None:
            self.soup_ja_else()
        elif self.soup.find('ja:include') is not None:
            self.soup_include()
        elif self.soup.find('ja:rowiterator') is not None:
            self.soup_row_iterator()
        elif self.soup.find('ja:coliterator') is not None:
            self.soup_col_iterator()
        else:
            self.variable_constructor()

    def __init__(self, sp, dir, images, album_name):
        self.soup = sp
        self.dir = dir
        self.images = images
        self.album_tags = ""
        self.album_description = ""
        self.album_name = album_name
        self.folder_level = ""
        self.previous_page = ""
        self.parent_index_page = ""
        self.icon_path = ""
        self.folder = ""
        self.credit_text = ""
        self.next_page = ""
        self.google_maps = ""
        self.homepage_address = ""
        self.comment = ""
        self.total_indexes = ""

    def dictionary(self):
        dict = {'${showAlbumTitle}': self.album_name,
                '<%=level==0 && !homepageAddress.equals(': self.folder_level,
                'totalIndexes': self.total_indexes,
                'albumTags': self.album_tags,
                'albumDescription': self.album_description,
                'folder': self.folder,
                'iconPath': self.icon_path,
                'parentIndexPage': self.parent_index_page,
                'comment': self.comment,
                'homepageAddress': self.homepage_address,
                'creditText': self.credit_text}
        return dict

    def soup_ja_if(self):
        dict = self.dictionary()
        dict1 = {'previousIndexPage': self.previous_page,
                 'nextIndexPage': self.next_page}
        for links in self.soup.find_all('ja:if'):
            if links.get('test') in dict.keys():
                if dict.get(links.get('test')):
                    links.replaceWithChildren()
                else:
                    links.extract()
            elif links.get('exists') in dict.keys():
                if dict.get(links.get('exists')):
                    links.replaceWithChildren()
                else:
                    links.extract()
            elif links.get('exists') in dict1.keys():
                if dict1.get(links.get('exists')):
                    links.find_next_sibling("ja:else").extract()
                    links.replaceWithChildren()
                else:
                    links.extract()
        self.index_parser()

    def soup_ja_else(self):
        for else_links in self.soup.find_all('ja:else'):
            else_links.replaceWithChildren()
        self.index_parser()

    def soup_include(self):
        for include_links in self.soup.find_all('ja:include'):
            if include_links.get('page') == 'header.inc':
                include_links.extract()
            elif include_links.get('page') == 'footer.inc':
                include_links.extract()
        self.index_parser()

    def row_iterator(self, i):
        img_tag = self.soup.find_all('img')[i + 1]
        img = img_tag.wrap(self.soup.new_tag('a', href="${closeupPath}"))
        td = img.wrap(self.soup.new_tag('td'))
        coliterator = td.wrap(self.soup.new_tag('ja:coliterator'))
        coliterator.wrap(self.soup.new_tag('tr'))

    def col_iterator(self, tag, i):
        img_tag = tag.find_all('img')[i + 1]
        img = img_tag.wrap(self.soup.new_tag('a', href="${closeupPath}"))
        img.wrap(self.soup.new_tag('td'))

    def calculate_abs_length(self, value):
        if (value / 4) > round(value / 4):
            return (round(value / 4) + 1)
        elif (value / 4) < round(value / 4):
            return (round(value / 4))
        else:
            return (round(value / 4))

    def soup_row_iterator(self):
        length = self.calculate_abs_length(len(self.images))
        row_tag = self.soup.find('ja:rowiterator')
        for j in range(length - 1):
            new2 = self.soup.new_tag(
                'img', src="${thumbPath}", width="${thumbWidth}",
                height="${thumbHeight}", alt="${title}", title="${title}")
            row_tag.find_all('tr')[j].insert_after(new2)
            self.row_iterator(j)
        row_tag.replaceWithChildren()
        html = BeautifulSoup(self.soup.prettify())
        self.index_parser()

    def soup_col_iterator(self):
        tag = self.soup.find('ja:coliterator')
        for i in range(3):
            new2 = self.soup.new_tag(
                'img', src="${thumbPath}",
                width="${thumbWidth}", height="${thumbHeight}",
                alt="${title}", title="${title}")
            tag.find_all('td')[i].insert_after(new2)
            self.col_iterator(tag, i)
        tag.replaceWithChildren()
        self.index_parser()

    def remove_remain_tags(self, s):
        index_url = "index" + ".html"
        album = "album"
        if s.find('img', src="${thumbPath}"):
            s.find('img', src="${thumbPath}").parent.parent.extract()
            self.remove_remain_tags(s)
        else:
            dest_file = open((os.path.join(self.dir, index_url)), 'w')
            dest_file.write(s.prettify())
            dest_file.close()

    def variable_constructor(self):
        self.soup = re.sub(r"\${resPath}", "res", str(self.soup))
        self.soup = re.sub(r"\${stylePath}", "res/style.css", str(self.soup))
        self.soup = re.sub(r"\${albumTitle}", self.album_name, str(self.soup))
        for im in self.images:
            self.soup = re.sub(
                r"\${title}", im.split('.')[0], str(self.soup), 2)
            self.soup = re.sub(r"\${thumbWidth}", str(124), str(self.soup), 1)
            self.soup = re.sub(r"\${thumbHeight}", str(93), str(self.soup), 1)
            self.soup = re.sub(
                r"\${thumbPath}", 'thumbs/' + str(im), str(self.soup), 1)
            self.soup = re.sub(
                r"\${closeupPath}",
                'slides/' + im.split('.')[0] + str('.html'), str(self.soup), 1)
        s = BeautifulSoup(self.soup)
        self.remove_remain_tags(s)

    def index_parser(self):
        if self.soup.find('ja:if') is not None:
            self.soup_ja_if()
        elif self.soup.find('ja:else') is not None:
            self.soup_ja_else()
        elif self.soup.find('ja:include') is not None:
            self.soup_include()
        elif self.soup.find('ja:rowiterator') is not None:
            self.soup_row_iterator()
        elif self.soup.find('ja:coliterator') is not None:
            self.soup_col_iterator()
        else:
            self.variable_constructor()
