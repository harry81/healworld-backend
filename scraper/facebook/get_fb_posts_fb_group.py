# -*- coding: utf-8 -*-
# ref : https://github.com/minimaxir/facebook-page-post-scraper
import requests
import json
import urllib2
import re
import datetime
import time
from django.conf import settings
from urlparse import urlparse
from dateutil.parser import parse
from scraper.models import ScraperItem
from django.core.files import File

access_token = "%s|%s" % (
    settings.SOCIAL_AUTH_FACEBOOK_KEY,
    settings.SOCIAL_AUTH_FACEBOOK_SECRET)


def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try:
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)

            print "Error for URL %s: %s" % (url, datetime.datetime.now())
            print "Retrying."

    return response.read()


# Needed to write tricky unicode correctly to csv
def unicode_normalize(text):
    return text.translate({
        0x2018: 0x27, 0x2019: 0x27, 0x201C: 0x22, 0x201D: 0x22,
        0xa0: 0x20}).encode('utf-8')


def getFacebookPageFeedData(group_id, access_token, num_statuses):

    # Construct the URL string; see
    # http://stackoverflow.com/a/37239851 for Reactions parameters
    base = "https://graph.facebook.com/v2.8"
    node = "/%s/feed" % group_id

    fields = "/?fields=message,link,created_time,type,name,id," + \
             "comments.limit(0).summary(true),shares,reactions." + \
             "limit(0).summary(true),from"
    parameters = "&limit=%s&since=yesterday&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data


def getReactionsForStatus(status_id):
    access_token = "%s|%s" % (
        settings.SOCIAL_AUTH_FACEBOOK_KEY,
        settings.SOCIAL_AUTH_FACEBOOK_SECRET)

    # See http://stackoverflow.com/a/37239851 for Reactions parameters
        # Reactions are only accessable at a single-post endpoint

    base = "https://graph.facebook.com/v2.6"
    node = "/%s" % status_id
    reactions = "/?fields=" \
                "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
                ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
                ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
                ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
                ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
                ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data


def saveFacebookPageFeedStatus(status):
    if status['type'] in ['link', 'status']:
        return

    try:
        link = status['link']
        fb_id = re.findall('fbid=([0-9]+)', link)[0]

        item = {
            'item_id': status['id'],
            'from_id': status['from']['id'],
            'from_name': status['from']['name'],
            'name': status['name'],
            'item_type': status['type'],
            'link': status['link'],
            'fb_id': fb_id,
            'message': status['message'],
            'created_at': parse(status['created_time'])
        }
    except Exception as e:
        print e
        print "[%s] doesn't saved [%s]" % (status['type'], e)
        return

    try:
        ScraperItem.objects.create(**item)
        print "%s[%s] saved" % (item['name'], item['item_type'])
    except Exception as e:
        print "%s - [%s] doesn't saved" % (e, status['type'])


def copyStatusToCore():
    from core.models import Image, User, Item

    access_token = "%s|%s" % (
        settings.SOCIAL_AUTH_FACEBOOK_KEY,
        settings.SOCIAL_AUTH_FACEBOOK_SECRET)

    for sc_item in ScraperItem.objects.all():
        if Item.objects.filter(link=sc_item.link).exists():
            continue

        # save image
        image_list_url = "https://graph.facebook.com/v2.8/%s?fields=images&access_token=%s" %\
                         (sc_item.fb_id, access_token)
        image_list = requests.get(image_list_url)
        if not image_list.ok:
            continue

        image_list_dict = json.loads(image_list.content)
        image_url = sorted(image_list_dict['images'])[3]

        img = requests.get(image_url['source'])
        filename = urlparse(image_url['source']).path.rsplit('/')[-1]

        print "%s - %s" % (image_url['source'], filename)

        with open('/tmp/%s' % filename, 'wb') as fp:
            for chunk in img.iter_content(1024):
                fp.write(chunk)

        image = Image()
        image.itemshot.save(filename,
                            File(open('/tmp/%s' % filename)))

        # save item with #image and #item
        facebookuser = User.objects.get(username='Facebook')
        item_dict = {
            "title": sc_item.from_name,
            "user": facebookuser,
            "memo": sc_item.message,
            "link": sc_item.link,
        }

        core_item = Item.objects.create(**item_dict)
        image.item = core_item
        image.save()


def processFacebookPageFeedStatus(status, access_token):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else \
            unicode_normalize(status['message'])
    link_name = '' if 'name' not in status.keys() else \
            unicode_normalize(status['name'])
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else \
            unicode_normalize(status['link'])
    status_author = unicode_normalize(status['from']['name'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(\
            status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    # best time format for spreadsheet programs:
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else \
            status['shares']['count']

    # Counts of each reaction separately; good for sentiment
    # Only check for reactions if past date of implementation:
    # http://newsroom.fb.com/news/2016/02/reactions-now-available-globally/

    reactions = getReactionsForStatus(status_id, access_token) \
            if status_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else \
            reactions['like']['summary']['total_count']

    # Special case: Set number of Likes to Number of reactions for pre-reaction
    # statuses

    num_likes = num_reactions if status_published < '2016-02-24 00:00:00' else \
            num_likes

    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)

    # return a tuple of all processed data

    return (status_id, status_message, status_author, link_name, status_type,
            status_link, status_published, num_reactions, num_comments,
            num_shares,  num_likes, num_loves, num_wows, num_hahas, num_sads,
            num_angrys)


def scrapeFacebookPageFeedStatus(group_id):
    has_next_page = True
    num_processed = 0   # keep a count on how many we've processed
    scrape_starttime = datetime.datetime.now()

    print "Scraping %s Facebook Page: %s\n" % \
        (group_id, scrape_starttime)

    statuses = getFacebookPageFeedData(group_id, access_token, 100)

    while has_next_page:
        for status in statuses['data']:
            # Ensure it is a status with the expected metadata
            if 'reactions' in status:
                saveFacebookPageFeedStatus(status)

            # output progress occasionally to make sure code is not
            # stalling
            num_processed += 1
            if num_processed % 100 == 0:
                print "%s Statuses Processed: %s" % (
                    num_processed, datetime.datetime.now())

        # if there is no next page, we're done.
        if 'paging' in statuses.keys():
            statuses = json.loads(request_until_succeed(
                statuses['paging']['next']))
        else:
            has_next_page = False

    print "\nDone!\n%s Statuses Processed in %s" % \
        (num_processed, datetime.datetime.now() - scrape_starttime)


# The CSV can be opened in all major statistical programs. Have fun! :)
