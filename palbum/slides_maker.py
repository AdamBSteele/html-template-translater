import os
import re
import threading
from bs4 import BeautifulSoup


class slides_image_urls(threading.Thread):

    '''
    This class is explicitly written for creating
    the html pages for the respective images in the
    slides folder that will be created in the folderpath
    which was mentioned (i.e which contains all the photos).
    This class creates number of threads for all the 
    images passed into it and they create html files
    in parallel and without any thread locking system.

    An images's data is entirely different from another.
    So, there is no need to implement thread locking
    system.

    We have implemented threading due to a main reason:
    If the user chooses to upload a folder which has nearly
    150 to 200 photos it can take more time for the whole
    execution for each photo. So, we have implemented this
    functionality in threads which can run in parallel and
    the execution time becomes very less.
    '''

    def __init__(self, soup, previousimage, im, nextimage, album_name, slides_path):
        '''
        __init__ declares all the useful variables 
        to be used in constructing the web pages in 
        the slides folder
        '''
        threading.Thread.__init__(self)
        self.soup = soup
        self.next_image_url = ""
        self.previous_page = previousimage
        self.image = im
        self.previous_image_url = ""
        self.next_page = nextimage
        self.album_name = album_name
        self.slides_path = slides_path
        self.res_path = "../res"
        self.style_path = "../res/style.css"
        self.index_page = "index.html"
        self.to_index_page = "To index page"
        self.to_previous_page = "Previous page"
        self.to_next_page = "Next Page"
        self.at_last_page = "At Last Page"
        self.at_first_page = "At First Page"
        self.image_width = 800
        self.image_height = 600
        self.google_maps = ""
        self.thumbnail_navigation = ""
        self.original_path = ""
        self.comment = ""
        self.homepage_address = ""
        self.credit_text = ""
        self.dict = {}
        self.dict1 = {}
        self.dict2 = {}
        self.file_type = "image"

    def run(self):
        '''
        This is the main method where the thread 
        comes into action. This method starts execution
        of the thread.
        '''

        self.dictionary()
        self.ja_tags_parser()

    def variable_constructor(self, data):
        '''
        The html_soup in this method contains
        parsed html data with the ${variable_names}.
        We change all those ${variable_names} using
        regular expression
        '''

        html_soup = BeautifulSoup(data)
        self.next_image_url = self.next_page.split('.')[0] + ".html"
        self.previous_image_url = self.previous_page.split('.')[0] + ".html"
        image_url = self.image.split('.')[0] + ".html"
        html_soup = self.re_sub(html_soup)
        dest_file = open((os.path.join(self.slides_path, image_url)), 'w')
        dest_file.write(html_soup)
        dest_file.close()

    def re_sub(self, html_soup):
        '''
        All the variables of the template are rendered
        here using regular expression.
        '''

        html_soup = re.sub(r"\${albumTitle}", self.album_name, str(html_soup))
        html_soup = re.sub(
            r"\${previousPage}", self.previous_image_url, str(html_soup))
        html_soup = re.sub(
            r"\${nextPage}", self.next_image_url, str(html_soup))
        html_soup = re.sub(r"\${imagePath}", self.image, str(html_soup))
        html_soup = re.sub(r"\${resPath}", self.res_path, str(html_soup))
        html_soup = re.sub(
            r"\${imageWidth}", str(self.image_width), str(html_soup))
        html_soup = re.sub(
            r"\${title}", self.image.split('.')[0], str(html_soup))
        html_soup = re.sub(
            r"\${imageHeight}", str(self.image_height), str(html_soup))
        html_soup = re.sub(r"\${stylePath}", self.style_path, str(html_soup))
        html_soup = re.sub(r"\${indexPage}", self.index_page, str(html_soup))
        html_soup = re.sub(
            r"\$text.indexPage", self.to_index_page, str(html_soup))
        html_soup = re.sub(
            r"\$text.previousPage", self.to_previous_page, str(html_soup))
        html_soup = re.sub(
            r"\$text.nextPage", self.to_next_page, str(html_soup))
        html_soup = re.sub(
            r"\$text.atLastPage", self.at_last_page, str(html_soup))
        html_soup = re.sub(
            r"\$text.atFirstPage", self.at_first_page, str(html_soup))
        return html_soup

    def dictionary(self):
        '''
        This method helps in declaring dictionaries for all
        the variables being used inside the template and also 
        the variables which we use in the code
        '''

        self.dict = {'${showAlbumTitle}': self.album_name, '${googleMaps}': self.google_maps,
                     '${thumbnailNavigation}': self.thumbnail_navigation, 'originalPath': self.original_path,
                     'comment': self.comment, 'homepageAddress': self.homepage_address, 'creditText': self.credit_text}
        self.dict1 = {
            'nextPage': self.next_page, 'previousPage': self.previous_page, }

    def slides_ja_if(self):
        '''
        This method is used for parsing out the <ja:if> tags.
        In this method, it checks out whether some variables
        are present or not. According to the presence of the
        variables either the tags are replaced with the inner
        html content or the entire <ja:if> tag is removed based
        on the variable presence.
        '''

        for links in self.soup.find_all('ja:if'):
            if links.get('test') in self.dict.keys():
                if self.dict.get(links.get('test')):
                    links.replaceWithChildren()
                else:
                    links.extract()
            elif links.get('test') == '<%=fileCategory == Category.video%>':
                if self.file_type == "image":
                    links.extract()
                else:
                    links.replaceWithChildren()
            elif links.get('exists') in self.dict.keys():
                if self.dict.get(links.get('exists')):
                    links.replaceWithChildren()
                else:
                    links.extract()
            elif links.get('exists') in self.dict1.keys():
                if self.dict1.get(links.get('exists')):
                    links.find_next_sibling("ja:else").extract()
                    links.replaceWithChildren()
                else:
                    links.extract()
        self.ja_tags_parser()

    def slides_ja_else(self):
        '''
        This method is used for parsing of <ja:else>
        tags. Once the <ja:if> tags are parsed out then the
        code search for else tags and replace them with 
        the inner html content.
        '''

        for else_links in self.soup.find_all('ja:else'):
            else_links.replaceWithChildren()
        self.ja_tags_parser()

    def ja_tags_parser(self):
        '''
        Variables in slides.htt file from the source template
        category.video -- if the file is a video;
        ${showalbumtitle} -- the title of the album 
        (i.e the name of the folder); 
        previouspage -- the before image;
        nextpage -- next image; 
        googlemaps -- google maps; 
        thumbnail navigation -- thumbnail navigation;
        originalPath -- Image, maybe with link to original;
        comment -- some sort of comment; 
        homepageaddress -- web site address of the owner 
        if exists; 
        credittext -- developer's own trademark

        Main functionality of this function:
        1) It takes in the the html data and
                does recursion on the data in order to 
                remove all the <ja> tags.

        2) In the first iteration it checks for the
                <ja:if> tags and parse them accordingly
                if the respective variables exist. There
                might be some cases where there can be
                inner <ja:if> tags. In order to parse the
                entire tags we apply recursion on the same
                data again. It check is there exists any <ja:if>
                tags and parses them accordingly.

        3) Once the recursion finds that there are no 
                <ja:if> tags, it goes to the next step; where
                it iterates through the whole data and parses out
                the <ja:else> tags in the same method which was
                mentioned above in the step 2.
        '''

        if self.soup.find('ja:if') != None:
            self.slides_ja_if()
        elif self.soup.find('ja:else') != None:
            self.slides_ja_else()
        else:
            self.variable_constructor(self.soup.prettify())
