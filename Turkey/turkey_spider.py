#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
import logging
import locale
import dateutil.parser
import re
import dateparser
from datetime import datetime, date
import random
import time
import csv
import urllib2

locale.setlocale(locale.LC_ALL, '')

class AllSpider(scrapy.Spider):
    name = 'all'

    custom_settings = {
        'ROBOTSTXT_OBEY': 0,
        'FEED_URI': 'gptk_staging_v1.xml',
        'FEED_FORMAT': 'xml',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    __connector_csv_filename = "connector_v1_final.csv"
    __connector_csv_log_file = "connector_csv_log_v1"

    def start_requests(self):

        # V1
        start_urls = {
            'http://www.greenpeace.org/turkey/tr/press/reports/coca-cola-dosyasi-1710/':('Raporlar','Biyoçeşitlilik ve Doğa','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/trakya-da-termik-santral-tehlikesi-rapor-180228/':('Raporlar','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/yukselis-ve-cokus-2018/':('Raporlar','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/eskisehir-termik-santral-tehlikesi-rapor-1802281/':('Raporlar','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/arilar-yasasin-diye-rapor/':('Raporlar','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/yagmur-ormanlari-icin-geri-sayim/':('Raporlar','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/Afinde-Komurlu-Termik-Santrallerin-Bedeli---Rapor/':('Raporlar','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/Akbayra-planlanan-termik-santralin-etkileri---Rapor/':('Raporlar','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/press/reports/Canakkalede-Termik-Santral-Projesinin-CED-Raporundaki-Eksiklikler---Rapor/':('Raporlar','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/ekolojik-tarimda-uretici-pazarlarinin-onemi/blog/62160/':('Blog','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/Plastiksiz-Denizler-Hareketi-Plastiksiz-Bir-Gelecek-Rehberi/blog/62154/':('Blog','Biyoçeşitlilik ve Doğa','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/plastik-poseti-birak-190114/blog/62093/':('Blog','Biyoçeşitlilik ve Doğa','','Plastik','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/basardik-arilara-zarar-veren-pestisitler-yasaklandi-181224/blog/62076/':('Blog','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/cop24ten-geriye-kalanlar-181218/blog/62063/':('Blog','İklim Krizi','','İklimDeğişikliği','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/kirli-palm-yana-kar-takibimiz-devam-ediyor/blog/62026/':('Blog','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/gunebakan-diyari-trakya-komur-istemiyor-181003/blog/61928/':('Blog','Enerji','','Kömür','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/cennetin-kanatlari-180919/blog/61887/':('Blog','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/orangutanlar-hakkinda-bilinmeyen-10-gercek/blog/61796/':('Blog','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/blog/mavi-gezegen/arilar-olmesin-gidamiz-tukenmesin/blog/61795/':('Blog','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','news-list','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/Plastik-atklarn-yeni-adresi-Turkiye/':('Haberler','Biyoçeşitlilik ve Doğa','','Plastik','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/arilar-hakkinda-10-ilginc-bilgi-181004/':('Haberler','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/ormansizlastirma-sorununu-cozmeyecek-181009/':('Haberler','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/cennet-kusu-istanbula-kondu-180916/':('Haberler','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/devletler-antarktika-okyanusu-nu-korumayi-basaramadi-181106/':('Haberler','Biyoçeşitlilik ve Doğa','','Okyanus','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/5-soruda-cop24-181205/':('Haberler','İklim Krizi','','İklimDeğişikliği','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/iklim-icin-ortak-cagri-181205/':('Haberler','İklim Krizi','','İklimDeğişikliği','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/hepimiz-ayni-kovandayiz-181213/':('Haberler','Biyoçeşitlilik ve Doğa','','GıdaTarım','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/mevsimler-alt-ust-ormanlar-alev-180725/':('Haberler','İklim Krizi','','İklimDeğişikliği','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/Krklarelililer-CED-toplantsn-yaptrmad/':('Haberler','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/Eskiehirde-termik-santrale-harcanacak-parayla-neler-yaplabilir/':('Haberler','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/penguenler-hakkinda-bilinmeyen-10-gercek-180425/':('Haberler','Biyoçeşitlilik ve Doğa','','Okyanus','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/turkiyede-havasi-tek-temiz-il-giresun-180503/':('Haberler','İklim Krizi','','HavaKirliliği','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/porsuk-cayindan-mesaj-komuru-es-gec-180505/':('Haberler','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/Trakyada-olas-komurlu-termik-santraller-11-bin-erken-olume-yol-acacak-180305/':('Haberler','Enerji','','Kömür','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/campaigns/nukleersiz-gelecek/chernobyl/cernobilde-ne-oldu/':('Blog','Enerji','','Nükleer','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/Kutup-aylar-hakknda-bilinmeyen-10-gercek-180227/':('Blog','İklim Krizi','','İklimDeğişikliği','','','article','Migrate'),
            'http://www.greenpeace.org/turkey/tr/news/cernobilin-sorumlusu-burada-260412/':('Haberler','Enerji','','Nükleer','','','article','Migrate'),
            # 'http://www.greenpeace.org/turkey/tr/get-involved/sehrinizdeki-greenpeace-yerel-grubuyla-iletisime-gecin/':('','','','','','','article','Migrate'),
            # 'http://www.greenpeace.org/turkey/tr/privacypolicy/':('','','','','','','article','Migrate'),
        }

        for url,data in start_urls.iteritems():
            p4_post_type, category1, category2, tags1, tags2, tags3, post_type, action = data

            if (post_type == 'article'):
                request = scrapy.Request(url, callback=self.parse_page_type2, dont_filter='true')
            elif (post_type == 'news-list'):
                request = scrapy.Request(url, callback=self.parse_page_type1, dont_filter='true')


            if ( action.lower()=='migrate' ):
                request.meta['status'] = 'publish'
            if ( action.lower()=='archive' ):
                request.meta['status'] = 'draft'
            request.meta['category1'] = category1
            request.meta['category2'] = category2
            request.meta['tags1'] = tags1
            request.meta['tags2'] = tags2
            request.meta['tags3'] = tags3
            request.meta['action'] = action
            request.meta['post_type'] = post_type
            request.meta['p4_post_type'] = p4_post_type
            yield request

        # Migrating authors/thumbnails
        '''
        author_usernames = {
            'greenpeace': 'Greenpeace P4',
            'Keith Stewart': 'p4_username_keith',
            'Miriam Wilson'
        }

        # Read in the file
        with open( 'gpaf_staging_v1.xml', 'r' ) as file :
            filedata = file.read()

        # Replace with correct usernames.
        for p3_author_username, p4_author_username in author_usernames.iteritems():
            filedata = filedata.replace('<author_username>' + p3_author_username, '<author_username>' + p4_author_username)

        # Remove dir="ltr" attributes from elements as requested.
        filedata = filedata.replace('dir="ltr"', '')

        # Write the file out again
        with open('gpaf_staging_v1.xml', 'w') as file:
            file.write(filedata)
        '''

    # Class = 'news-list'
    # pagetypes = blogs,news
    def parse_page_type1(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img/@src').extract()
        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesB_generated.append(image_file)

        imagesEnlarge=response.xpath('//div[@class="news-list"]//div[@class="post-content"]//a[@class="open-img EnlargeImage"]/@href').extract()
        imagesEnlarge_generated = list()
        for image_file in imagesEnlarge:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesEnlarge_generated.append(image_file)

        pdfFiles=response.css('div.news-list a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)

        date_field = response.css('div.news-list .caption::text').re_first(r' - \s*(.*)')
        if date_field:
            date_field = self.filter_month_name(date_field);
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  #english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ") #spanish
            date_field = date_field.replace(" på ", " ") #swedish
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = date_field.replace(" na ", " ") #slovenian
            date_field = date_field.replace(" o ", " ")  # polish

            date_field = dateutil.parser.parse(date_field)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        body_text = response.css('div.news-list div.post-content').extract_first()
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)

        body_text = self.filter_post_content(body_text)

        images=response.xpath('//*[@class="post-content"]/div/p/a//img[contains(@style, "float:")]').extract()   #img[@style="margin: 9px; float: left;"]
        imagesD_generated = list()
        for image in images:
            imagesD_generated.append(image)

        blockquotes = response.xpath('//*[@id="content"]//blockquote').extract()
        blockquotes_generated = list()
        for blockquote in blockquotes:
            blockquotes_generated.append(blockquote)

        author_username = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong/a/@href)').extract_first()

        if (author_username != 'None'):
            Segments  = author_username.strip().split('/')
            try:                                            #if ( ( len(Segments) == 4 ) and Segments[4] ):
                if ( Segments[5] ):
                    author_username = Segments[5]
            except IndexError:
                try:  # if ( ( len(Segments) == 4 ) and Segments[4] ):
                    if (Segments[3]):
                        author_username = Segments[3]
                except IndexError:
                    author_username = ''

        author_name = response.xpath('string(//div[@class="news-list"]/ul/li/*/*/span[@class="caption"]/span[@class="green1"]/strong)').extract()[0]
        if ( author_name ):
            author_name = author_name.strip()

        # Get the thumbnail of the post as requested.
        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        unique_map_id = int(time.time() + random.randint(0, 999))

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                # PHP webservice script url.
                api_url = "http://localhosttest/ocr_webservice/email_img_to_text.php"
                end_point_url = api_url + "?url=" + image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace('', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"' + image_file + '\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        """
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list.csv")
        """
        # List authors
        #data = [author_name,author_username]
        #self.csv_writer(data, "author_list.csv")

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.news-list h1::text'),
            #'subtitle': '',
            'author': author_name,
            'author_username': author_username,
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': response.xpath('string(//div[@class="news-list"]/ul/li/div[@class="post-content"]/div//*[self::p or self::h3 or self::h2][1])').extract()[0],
            'category1': response.meta['category1'],
            'category2': response.meta['category2'],
            'text':  body_text,
            'imagesA': imagesA_generated,
            'imagesEnlarge': imagesEnlarge_generated,
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'imagesD': imagesD_generated,
            'blockquote': blockquotes_generated,
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'tags3': response.meta['tags3'],
            'url': response.url,
            'status': response.meta['status'],
            'map_url': '',
            'unique_map_id': unique_map_id,
            'thumbnail': thumbnail,
        }

    # class = 'happen-box article'
    # pagetypes = parse_publication,parse_press,parse_feature
    def parse_page_type2(self, response):

        def extract_with_css(query):
            return response.css(query).extract_first()

        imagesA=response.xpath('//div[@class="post-content"]//a[img]/@href').extract()
        imagesA_generated = list()
        for image_file in imagesA:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            imagesA_generated.append(image_file)

        imagesB=response.xpath('//div[@class="post-content"]//img/@src').extract()
        if len(imagesB) == 0:
            imagesB = response.xpath('//div[@id="content"]//img/@src').extract()

        imagesB_generated = list()
        for image_file in imagesB:
            if (image_file.startswith('/')):
                image_file = image_file.replace('/','http://www.greenpeace.org/',1)
            # Custom fix for GPAF only.
            if 'http://assets.pinterest.com/images/PinExt.png' not in image_file:
                imagesB_generated.append(image_file)

        pdfFiles=response.css('div.article a[href$=".pdf"]::attr(href)').extract()
        pdf_files_generated = list()
        for pdf_file in pdfFiles:
            if (pdf_file.startswith('/')):
                pdf_file = pdf_file.replace('/','http://www.greenpeace.org/',1)
            pdf_files_generated.append(pdf_file)

        image_gallery=response.xpath("//*[contains(@class, 'embedded-image-gallery')]")
        p3_image_gallery = 'false'
        if image_gallery:
            p3_image_gallery = 'true'

        try:
            lead_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[1]/div/text()').extract()[0]
        except IndexError:
            lead_text = ''

        body_text = response.xpath('//*[@id="content"]/div[4]/div/div[2]/div[2]').extract()[0]
        if body_text:
            body_text = body_text.replace('src="//', 'src="https://').replace('src="/', 'src="http://www.greenpeace.org/').replace('href="/', 'href="http://www.greenpeace.org/')
            body_text = body_text.replace('<span class="btn-open">zoom</span>', '')
            body_text = re.sub('<p dir="ltr">(.*)<\/p>', "\g<1>", body_text)
            if lead_text:
                body_text = '<div class="leader" style="font-weight: bold;margin-bottom: 12px">' + lead_text + '</div>' + body_text + response.xpath(' //*[@id="content"]/div[4]/div/div[2]/p').extract_first()

        subtitle = extract_with_css('div.article h2 span::text')
        if subtitle:
            body_text = '<h2>' + subtitle + '</h2><br />' + body_text

        thumbnail = response.xpath('string(head//link[@rel="image_src"]/@href)').extract_first()

        date_field = response.css('div.article div.text span.author::text').re_first(r' - \s*(.*)')
        try:
            date_field = self.filter_month_name(date_field);
            # Filter extra string part from date.
            date_field = date_field.replace(" at", "")  #english
            date_field = date_field.replace(" à", "")
            date_field = date_field.replace(" kl.", "")
            date_field = date_field.replace(" v", "")
            date_field = date_field.replace(" en ", " ") #spanish
            date_field = date_field.replace(" på ", " ") #swedish
            date_field = date_field.replace(" di ", " ") #indonesian
            date_field = date_field.replace(" na ", " ") #slovenian
            date_field = date_field.replace(" o ", " ")  # polish
        except IndexError:
            date_field = ""

        if date_field:
            date_field = dateutil.parser.parse(date_field)

        # Filter email id image and replace it with email text.
        delete_images = list()
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                api_url = "http://localhosttest/ocr_webservice/email_img_to_text.php"
                end_point_url = api_url+"?url="+image_file
                emailid = urllib2.urlopen(end_point_url).read(1000)
                # Search replace the \n, <BR>, spaces from email id.
                emailid = emailid.replace('\n', '')
                emailid = emailid.replace('<br>', '')
                emailid = emailid.replace('<BR>', '')
                emailid = emailid.replace('', '')
                delete_images.append(image_file)
                # Remove the email images from Post body and replace it with email text.
                body_text = re.sub(
                    '<img[a-zA-Z0-9="\s\_]*src=\"'+image_file+'\"[a-zA-Z0-9="\s]*>',
                    '<a href="mailto:' + emailid.strip() + '" target="_blank">' + emailid.strip() + '</a>', body_text)

        # Remove the email images from list.
        for image_file in delete_images:
            imagesB_generated.remove(image_file)

        """
        #list images urls
        for image_file in imagesB_generated:
            if ("/emailimages/" in image_file):
                data = [image_file]
                self.csv_writer(data, "email_images_url_list.csv")
        
        """

        # Post data mapping logic start.
        unique_map_id = int(time.time() + random.randint(0, 999))
        map_url = ''
        """
        if "/en/" in response.url:
            # For English language POSTs

            # Check the POST transalation availability
            try:
                map_url = response.xpath('//*[@class="language"]//option[2]/@value').extract()[0]
            except IndexError:
                map_url = ''

            if "/fr/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                # The Post mapping data added into csv file.
                data = [unique_map_id, response.url, map_url]
                self.csv_writer(data, self.__connector_csv_filename)

                data = [response.url, response.meta['p4_post_type'], response.meta['category1'],response.meta['category2'], response.meta['tags1'], response.meta['tags2'], response.meta['tags3'], response.meta['post_type'], response.meta['action']]
                self.csv_writer(data, "Language_mapping_en_list.csv")
        else:
            # For French language POSTs

            # Check the POST transalation if available
            try:
                map_url = response.xpath('//*[@class="language"]//option[1]/@value').extract()[0]
            except IndexError:
                map_url = ''

            if "/en/" not in map_url:
                map_url = ''

            if map_url:
                map_url = 'http://www.greenpeace.org' + map_url

                with open(self.__connector_csv_filename, "rb") as file_obj:
                    reader = csv.reader(file_obj)
                    for row in reader:
                        if (row[1] == map_url or row[2] == response.url):
                            #print "=======Match found======="
                            unique_map_id = row[0]
                            # Log the details
                            data = ["FR==>", unique_map_id, response.url, map_url,"EN==>", row[0], row[1], row[2]]
                            #print data
                            self.csv_writer(data, self.__connector_csv_log_file)

                            data = [response.url, response.meta['p4_post_type'], response.meta['category1'], response.meta['category2'],
                                    response.meta['tags1'], response.meta['tags2'], response.meta['tags3'],
                                    response.meta['post_type'], response.meta['action']]
                            self.csv_writer(data, "Language_mapping_fr_list.csv")
        # Post data mapping logic ends.
        """

        yield {
            'type': response.meta['p4_post_type'],
            'p3_image_gallery': p3_image_gallery,
            'title': extract_with_css('div.article h1 span::text'),
            #'subtitle': '',
            'author': 'Greenpeace Turkey',
            'author_username': 'greenpeace',
            #'date': response.css('#content > div.happen-box.article > div > div.text > span').re_first(r' - \s*(.*)'),
            'date': date_field,
            #'lead': extract_with_css('div.news-list div.post-content *:first-child strong::text'),
            'lead': extract_with_css('#content > div.happen-box.article > div > div.text > div.leader > div'),
            'category1': response.meta['category1'],
            'category2': response.meta['category2'],
            #'text':  response.css('div.news-list div.post-content').extract_first(),
            'text':  body_text,
            'imagesA': imagesA_generated,
            #'imagesB': response.xpath('//div[@class="news-list"]//div[@class="post-content"]//img[not(ancestor::a)]/@src').extract(), #don't import image if there's an a tag around it
            'imagesB': imagesB_generated,
            'imagesC': response.xpath('//div[@class="gallery"]//div[@class="img-nav"]//a/@rel').extract(), # Galleries (horrible html)
            'pdfFiles': pdf_files_generated,
            'tags1': response.meta['tags1'],
            'tags2': response.meta['tags2'],
            'tags3': response.meta['tags3'],
            'map_url': map_url,
            'unique_map_id': unique_map_id,
            'url': response.url,
        }

    def filter_post_content(self, post_data):
        # Filter the youtube video and add embed shortcode instead.
        post_data = re.sub(
            '\<object[width\=\"height0-9\s]*data\=\"([https]*\:\/\/www.youtube.com[a-zA-Z0-9\/\=\-\?\_]*)\"[\=\"a-zA-Z\/\-\s0-9]*\>[\\n\s]*(.*)[\\n\s]*\<\/object\>',
            '[embed]\g<1>[/embed]', post_data)

        return post_data

# Filter month name function is not needed for english speaking sites

    def filter_month_name(self, month_name):

        month_ro_en = {
            'Ocak': 'January',
            'Şubat': 'February',
            'Mart': 'March',
            'Nisan': 'April',
            'Mayıs': 'May',
            'Hazīran': 'June',
            'Temmuz': 'July',
            'Ağustos': 'August',
            'Eylül': 'September',
            'Ekim': 'October',
            'Kasım': 'November',
            'Aralık': 'December',
        }

        # Replace the romanian month name with english month name.
        for ro_month, en_month in month_ro_en.iteritems():
            month_name = month_name.replace(ro_month, en_month)

        return month_name;

    def csv_writer(self, data, path):
        # Write data to a CSV file path
        with open(path, "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(data)
