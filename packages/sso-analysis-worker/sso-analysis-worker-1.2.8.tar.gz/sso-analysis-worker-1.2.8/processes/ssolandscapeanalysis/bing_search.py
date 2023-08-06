import os
import tempfile
import time

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

import exceptions
from logmgmt import logger
from services import DriverManager

bing_url = 'https://bing.com'
xpath = '//*[@id="b_results"]/li[@class="b_algo"]/*[1]/*[1]'


def test_search(driver: WebDriver) -> bool:
    driver.get(bing_url)
    try:
        search_field = driver.find_element(By.ID, 'sb_form_q')
        search_field.send_keys("test")
        search_field.submit()
        time.sleep(2)
        return len(driver.find_elements(By.XPATH, xpath)) > 0
    except NoSuchElementException:
        return False


def save_error_screenshot(driver: WebDriver):
    extensions_folder = tempfile.tempdir + "/ssoworker-errors/"
    if not os.path.exists(extensions_folder):
        os.makedirs(extensions_folder)
    if driver.save_screenshot(extensions_folder + "bing-error.png"):
        logger.info("Saved screenshot to " + extensions_folder)
    else:
        logger.info("Could not save error screenshot")


def get_bing_login_pages(driver: WebDriver, base_page, count_of_results=1, login_search_term="login", max_tries=3,
                         include_just_sub_domains=True) -> list:
    logger.info("Starting Bing search")
    search_term = base_page + " " + login_search_term
    if include_just_sub_domains:
        search_term += " site:" + base_page
    logger.info("Searching Bing with term \"" + search_term + "\"")
    counter = 1
    while counter <= max_tries:
        counter += 1
        try:
            driver.get(bing_url)
            search_field = driver.find_element(By.ID, 'sb_form_q')
            search_field.send_keys(search_term)
            search_field.submit()
            time.sleep(2)
            logger.info("Taking first " + str(count_of_results) + " result(s)")
            links = []
            while len(links) < count_of_results:
                selected = driver.find_elements(By.XPATH, xpath)
                logger.info("Found " + str(len(selected)) + " result items")
                if len(selected) == 0:
                    if len(links) == 0:
                        logger.info("We could not find first link of Bing search results! "
                                    "Checking if test search is working!")
                        save_error_screenshot(driver)
                        if not test_search(driver):
                            raise exceptions.BingHasChangedException()
                        logger.info("Looks like no links are found by Bing for the original request.")
                        if counter <= max_tries:
                            logger.info("Retrying getting results")
                            raise exceptions.RetryException()
                        logger.info("Returning empty list")
                        return links
                    return links
                link_counter = 0
                while len(links) < count_of_results and link_counter < len(selected):
                    raw_link = selected[link_counter]
                    while raw_link.tag_name != "a":
                        logger.info("Intermediate element found. Going one step deeper")
                        raw_link = raw_link.find_element(By.CSS_SELECTOR, "*:first-child")
                    link = raw_link.get_attribute("href")
                    logger.info("Got " + link)
                    links.append(link)
                    link_counter += 1

                if len(links) < count_of_results:
                    logger.info("Finished results for current site but more links were requested. Loading next site")
                    time.sleep(5)
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.sb_bp')
                    if next_buttons:
                        driver.execute_script("arguments[0].click();", next_buttons[-1])
                        time.sleep(2)
                    else:
                        break
                else:
                    break
            return links
        except NoSuchElementException:
            raise exceptions.BingHasChangedException()
        except WebDriverException as e:
            logger.error(e)
            logger.error("We got an unknown Webdriverexception. Please manage this!")
        except exceptions.BingHasChangedException as e:
            raise e
        except exceptions.RetryException:
            logger.info("Retrying (attempt: " + str(counter) + ")")
            continue
        except Exception as e:
            logger.error(e)
            logger.error("We got an unknown Exception. Please manage this!")

        if counter <= max_tries:
            logger.info("Retrying (attempt: " + str(counter) + ")")
            continue
    raise exceptions.BingHasChangedException()


if __name__ == "__main__":
    names = [  # "google.com", "youtube.com", "facebook.com", "netflix.com", "microsoft.com", "twitter.com",
        # "instagram.com", "tmall.com", "linkedin.com", "apple.com", "qq.com", "wikipedia.org",
        # "baidu.com",
        # "googletagmanager.com",
        #"sohu.com", "live.com", "wordpress.org", "yahoo.com", "netflix.net", "amazon.com",
        #"youtu.be", "pinterest.com", "taobao.com", "adobe.com", "windowsupdate.com", "360.cn", "office.com",
        #"vimeo.com", "jd.com", "microsoftonline.com", "amazonaws.com", "bing.com", "wordpress.com", "goo.gl",
        #"reddit.com", "zoom.us",
        #"github.com", "weibo.com", "doubleclick.net", "bit.ly", "sina.com.cn",
        #"googleusercontent.com", "macromedia.com", "xinhuanet.com", "blogspot.com", "whatsapp.com", "mozilla.org",
        #"msn.com", "tumblr.com", "google-analytics.com",
        "vk.com", "nytimes.com", "flickr.com", "europa.eu",
        "nih.gov",
        #"skype.com", "gravatar.com", "office365.com", "dropbox.com", "spotify.com", "soundcloud.com",
        "akamaiedge.net", "medium.com", "google.com.hk", "t.co", "panda.tv", "zhanqi.tv", "akadns.net",
        "alipay.com", "myshopify.com", "apache.org", "icloud.com", "forbes.com", "paypal.com", "csdn.net",
        "cnn.com", "ebay.com", "w3.org", "cloudflare.com", "theguardian.com", "yahoo.co.jp", "archive.org",
        "lencr.org", "twitch.tv", "github.io", "sourceforge.net", "imdb.com", "bbc.co.uk", "bbc.com", "naver.com",
        "canva.com", "bongacams.com", "stackoverflow.com", "creativecommons.org", "office.net", "aliexpress.com",
        "tiktok.com", "force.com", "forms.gle", "miit.gov.cn", "issuu.com", "who.int", "aaplimg.com", "yandex.ru",
        "weebly.com", "amazon.in", "etsy.com", "googlesyndication.com", "windows.net", "wixsite.com",
        "washingtonpost.com", "cdc.gov", "outlook.com", "tianya.cn", "t.me", "huanqiu.com", "amazon.co.jp",
        "reuters.com", "googleadservices.com", "chaturbate.com", "ytimg.com", "tinyurl.com", "yy.com",
        "sciencedirect.com", "wikimedia.org", "wsj.com", "digicert.com", "okezone.com", "wix.com", "bloomberg.com",
        "opera.com", "youtube-nocookie.com", "oracle.com", "apple-dns.net", "mail.ru", "businessinsider.com",
        "slideshare.net", "google.de", "indeed.com", "coinmarketcap.com", "blogger.com", "wp.com", "php.net",
        "harvard.edu", "sharepoint.com", "aparat.com", "imgur.com", "researchgate.net", "17ok.com", "godaddy.com",
        "amazon.co.uk", "mit.edu", "fbcdn.net", "so.com", "google.co.in", "list-manage.com", "salesforce.com",
        "cnet.com", "cnbc.com", "wiley.com", "windows.com", "gnu.org", "1688.com", "booking.com", "go.com",
        "wa.me", "dailymail.co.uk", "google.com.br", "ibm.com", "stanford.edu", "tradingview.com", "nature.com",
        "googlevideo.com", "ok.ru", "walmart.com", "app-measurement.com", "usatoday.com", "163.com", "hp.com",
        "un.org", "espn.com", "eventbrite.com", "doi.org", "gvt2.com", "surveymonkey.com", "google.co.jp",
        "gvt1.com", "chase.com", "www.gov.uk", "fandom.com", "springer.com", "unsplash.com", "freepik.com",
        "alibaba.com", "nginx.org", "cloudfront.net", "nasa.gov", "mailchimp.com", "telegraph.co.uk",
        "instructure.com", "time.com", "nflxso.net", "haosou.com", "npr.org", "cpanel.net", "google.co.uk",
        "yelp.com", "themeforest.net", "ted.com", "scorecardresearch.com", "facebook.net", "msedge.net",
        "samsung.com", "behance.net", "google.cn", "tribunnews.com", "bitly.com", "telegram.org", "addtoany.com",
        "opendns.com", "pornhub.com", "nginx.com", "amazon-adsystem.com", "myspace.com", "rakuten.co.jp",
        "scribd.com", "wired.com", "amazon.de", "akamai.net", "dailymotion.com", "babytree.com", "line.me",
        "indiatimes.com", "techcrunch.com", "ggpht.com", "cpanel.com", "pikiran-rakyat.com", "flipkart.com",
        "huffingtonpost.com", "addthis.com", "zendesk.com", "grammarly.com", "shopify.com", "goodreads.com",
        "mysql.com", "gome.com.cn", "cnblogs.com", "google.es", "google.fr", "ca.gov", "squarespace.com",
        "independent.co.uk", "googletagservices.com", "amzn.to", "berkeley.edu", "w3schools.com", "foxnews.com",
        "hugedomains.com", "tripadvisor.com", "livejasmin.com", "latimes.com", "aliyun.com", "pixabay.com",
        "google.ru", "6.cn", "google.it", "akamaized.net", "adnxs.com", "xvideos.com", "aol.com", "zillow.com",
        "demdex.net", "stackexchange.com", "fb.com", "wetransfer.com", "healthline.com", "sitemaps.org",
        "taboola.com", "shutterstock.com", "ft.com", "free.fr", "youku.com", "binance.com", "debian.org",
        "quora.com", "state.gov", "udemy.com", "livejournal.com", "fiverr.com", "webmd.com", "intuit.com",
        "arnebrachhold.de", "loc.gov", "statista.com", "theverge.com", "wikihow.com", "kickstarter.com",
        "cornell.edu", "beian.gov.cn", "intel.com", "bilibili.com", "hubspot.com", "theatlantic.com", "slack.com",
        "nationalgeographic.com", "g.page", "prnewswire.com", "ietf.org", "cbsnews.com", "xhamster.com",
        "statcounter.com", "savefrom.net", "fda.gov", "investopedia.com", "tandfonline.com", "deviantart.com",
        "washington.edu", "mediafire.com", "ilovepdf.com", "rubiconproject.com", "roblox.com", "marriott.com",
        "android.com", "snapchat.com", "cisco.com", "mailchi.mp", "ikea.com", "rednet.cn", "google.ca",
        "giphy.com", "pubmatic.com", "ettoday.net", "nbcnews.com", "linktr.ee", "twimg.com", "usnews.com",
        "marketwatch.com", "adsrvr.org", "aboutads.info", "gmail.com", "huffpost.com", "dell.com", "hao123.com",
        "ntp.org", "bestbuy.com", "daum.net", "digg.com", "upwork.com", "trello.com", "buzzfeed.com", "deepl.com",
        "kompas.com", "oup.com", "duckduckgo.com", "jimdo.com", "msftconnecttest.com", "box.com", "nr-data.net",
        "amazon.ca", "criteo.com", "edgekey.net", "business.site", "akismet.com", "safebrowsing.apple",
        "webex.com", "americanexpress.com", "cambridge.org", "pki.goog", "2mdn.net", "zoho.com", "rlcdn.com",
        "evernote.com", "sagepub.com", "about.com", "azure.com", "gosuslugi.ru", "speedtest.net", "detik.com",
        "hbr.org", "academia.edu", "weather.com", "akamaihd.net", "princeton.edu", "google.com.tw",
        "casalemedia.com", "zhihu.com", "bandcamp.com", "change.org", "typepad.com", "ups.com", "padlet.com",
        "sciencemag.org", "pinimg.com", "pixnet.net", "economist.com", "msftncsi.com", "allaboutcookies.org",
        "launchpad.net", "networkadvertising.org", "ampproject.org", "fedex.com", "unesco.org",
        "constantcontact.com", "digikala.com", "disqus.com", "coursera.org", "britannica.com", "pbs.org",
        "openx.net", "whitehouse.gov", "craigslist.org", "e2ro.com", "globo.com", "wellsfargo.com", "tistory.com",
        "usda.gov", "nypost.com", "mayoclinic.org", "trustpilot.com", "primevideo.com", "kumparan.com",
        "target.com", "mashable.com", "fastly.net", "uol.com.br", "businesswire.com", "moatads.com", "51.la",
        "google.com.sg", "patreon.com", "cnzz.com", "epa.gov", "stumbleupon.com", "vice.com", "discord.com",
        "umich.edu", "momoshop.com.tw", "newrelic.com", "outbrain.com", "bidswitch.net", "columbia.edu",
        "eepurl.com", "fb.me", "homedepot.com", "irs.gov", "jquery.com", "noaa.gov", "engadget.com", "redhat.com",
        "hotstar.com", "typeform.com", "arcgis.com", "vox.com", "jiameng.com", "psu.edu", "feedburner.com",
        "getpocket.com", "pexels.com", "usps.com", "investing.com", "people.com.cn", "worldbank.org", "iso.org",
        "advertising.com", "dribbble.com", "hulu.com", "airbnb.com", "cbc.ca", "trafficmanager.net", "rt.com",
        "fc2.com", "yale.edu", "sciencedaily.com", "zdnet.com", "trendyol.com", "telegram.me", "wpengine.com",
        "smallpdf.com", "onlinesbi.com", "gofundme.com", "calendly.com", "webs.com", "example.com", "abc.net.au",
        "istockphoto.com", "varzesh3.com", "whatsapp.net", "steampowered.com", "stripe.com", "azureedge.net",
        "cdninstagram.com", "google.com.tr", "upenn.edu", "qualtrics.com", "quizlet.com", "fastcompany.com",
        "elsevier.com", "teamviewer.com", "meetup.com", "google.com.mx", "mozilla.com", "getadblock.com",
        "bluekai.com", "agkn.com", "psychologytoday.com", "newyorker.com", "everesttech.net", "bet9ja.com",
        "3lift.com", "inc.com", "merriam-webster.com", "dw.com", "tripod.com", "hdfcbank.com", "apnews.com",
        "deloitte.com", "ebay.de", "wisc.edu", "zerodha.com", "secureserver.net", "adsafeprotected.com",
        "mathtag.com", "entrepreneur.com", "gizmodo.com", "ox.ac.uk", "nike.com", "fortune.com", "geocities.com",
        "theconversation.com", "plesk.com", "plos.org", "capitalone.com", "gotowebinar.com", "quantserve.com",
        "tapad.com", "ieee.org", "hootsuite.com", "doubleverify.com", "tudou.com", "bmj.com", "sun.com",
        "amazon.fr", "medicalnewstoday.com", "yimg.com", "bbb.org", "avito.ru", "hotjar.com", "canada.ca",
        "verisign.com", "discord.gg", "guardian.co.uk", "umn.edu", "oreilly.com", "sogou.com", "bankofamerica.com",
        "photobucket.com", "envato.com", "bet365.com", "jotform.com", "weforum.org", "ubuntu.com", "huawei.com",
        "krxd.net", "appsflyer.com", "grid.id", "att.com", "sfgate.com", "scientificamerican.com", "xnxx.com",
        "youronlinechoices.com", "kakao.com", "crashlytics.com", "fidelity.com", "biomedcentral.com",
        "google.co.th", "jhu.edu", "vkontakte.ru", "ndtv.com", "ameblo.jp", "arxiv.org", "suara.com",
        "haiwainet.cn", "mckinsey.com", "sindonews.com", "newsweek.com", "uci.edu", "apa.org", "nvidia.com",
        "glassdoor.com", "pcmag.com", "elegantthemes.com", "fontawesome.com", "indiegogo.com", "chess.com",
        "ucla.edu", "oecd.org", "mzstatic.com", "spotxchange.com", "slate.com", "chicagotribune.com", "ask.com",
        "redd.it", "ebay.co.uk", "miitbeian.gov.cn", "crwdcntrl.net", "aboutcookies.org", "cmu.edu",
        "disneyplus.com", "360.com", "elpais.com", "notion.so", "bluehost.com", "steamcommunity.com", "cam.ac.uk",
        "amazon.es", "python.org", "amazon.it", "hilton.com", "edgesuite.net", "lenovo.com", "google.com.ar",
        "realtor.com", "asos.com", "openstreetmap.org", "sfx.ms", "adform.net", "aliexpress.ru", "ftc.gov",
        "utexas.edu", "wayfair.com", "google.com.au", "ed.gov", "soso.com", "pewresearch.org", "accuweather.com",
        "wikia.com", "wiktionary.org", "nps.gov", "arstechnica.com", "xing.com", "google.pl", "icicibank.com",
        "jstor.org", "cnnic.cn", "bizjournals.com", "myworkday.com", "smartadserver.com", "nikkei.com",
        "spiegel.de", "timeanddate.com", "pinterest.ca", "cbslocal.com", "fool.com", "dotomi.com",
        "visualstudio.com", "blackboard.com", "azurewebsites.net", "adp.com", "redfin.com", "uchicago.edu",
        "chegg.com", "media.net", "symantec.com", "chron.com", "fao.org", "nba.com", "uk.com", "nist.gov",
        "tencent.com", "www.gov.cn", "thelancet.com", "gitlab.com", "ltn.com.tw", "si.edu", "zol.com.cn",
        "jsdelivr.net", "qz.com", "thawte.com", "mirror.co.uk", "howstuffworks.com", "house.gov", "metropoles.com",
        "bscscan.com", "pnas.org", "turn.com", "docker.com", "adobe.io", "google.com.sa", "thesun.co.uk",
        "licdn.com", "apple.news", "patch.com", "media-amazon.com", "gartner.com", "lijit.com", "cricbuzz.com",
        "barnesandnoble.com", "etoro.com", "youm7.com", "appspot.com", "google.com.eg", "politico.com", "ny.gov",
        "coingecko.com", "uber.com", "japanpost.jp", "jamanetwork.com", "wildberries.ru", "mercadolibre.com.ar",
        "google.co.id", "bitnami.com", "atlassian.com", "about.me", "uiuc.edu", "chinadaily.com.cn",
        "livescience.com", "criteo.net", "shareasale.com", "vmware.com", "1rx.io", "purdue.edu", "usc.edu",
        "altervista.org", "variety.com", "anchor.fm", "orange.fr", "china.com", "verizon.com", "omtrdc.net",
        "mercadolibre.com.mx", "census.gov", "nyu.edu", "seekingalpha.com", "bidr.io", "smh.com.au",
        "googleblog.com", "bootstrapcdn.com", "tiktokv.com", "liadm.com", "typekit.net", "shopee.tw",
        "manoramaonline.com", "feedly.com", "remove.bg", "nydailynews.com", "geeksforgeeks.org",
        "icloud-content.com", "ozon.ru", "hbomax.com", "sahibinden.com", "googleapis.com", "mdpi.com", "ign.com",
        "moneycontrol.com", "acs.org", "com.com", "rollingstone.com", "teads.tv", "proofpoint.com", "senate.gov",
        "autodesk.com", "sharethrough.com", "usgs.gov", "telewebion.com", "venturebeat.com", "go-mpulse.net",
        "ea.com", "news.com.au", "globenewswire.com", "frontiersin.org", "yahoodns.net", "spankbang.com",
        "sec.gov", "bls.gov", "espncricinfo.com", "avast.com", "playstation.com", "ria.ru", "withgoogle.com",
        "discordapp.com", "hhs.gov", "rakuten.com", "live.net", "techradar.com", "tiktokcdn.com", "netscape.com",
        "aljazeera.com", "sitescout.com", "us.com", "miibeian.gov.cn", "khanacademy.org", "braze.com",
        "lifehacker.com", "breitbart.com", "adobedtm.com", "ning.com", "y2mate.com", "norton.com", "slashdot.org",
        "xfinity.com", "worldometers.info", "dhl.com", "nejm.org", "matterport.com", "asus.com", "costco.com",
        "premierbet.co.ao", "enable-javascript.com", "tremorhub.com", "appcenter.ms", "imrworldwide.com", "m.me",
        "blogspot.co.uk", "msu.edu", "earthlink.net", "freshdesk.com", "sectigo.com", "coinbase.com",
        "postgresql.org", "truste.com", "www.nhs.uk", "reverso.net", "over-blog.com", "sonhoo.com", "docusign.com",
        "farfetch.com", "hatena.ne.jp", "zemanta.com", "macys.com", "sentry.io", "rokna.net", "sky.com",
        "allegro.pl", "prezi.com", "thetimes.co.uk", "nfl.com", "douban.com", "xbox.com", "google.co.kr",
        "ucsd.edu", "comodoca.com", "cdn-apple.com", "trustarc.com", "eff.org", "branch.io", "people.com",
        "lazada.sg", "thehill.com", "ufl.edu", "thedailybeast.com", "iqiyi.com", "instructables.com", "moodle.org",
        "inquirer.net", "duke.edu", "unicef.org", "cookielaw.org", "expedia.com", "sakura.ne.jp",
        "thefreedictionary.com", "substack.com", "web.de", "mixcloud.com", "thesaurus.com", "umd.edu", "mlb.com",
        "getbootstrap.com", "thepiratebay.org", "scmp.com", "softonic.com", "joomla.org", "parallels.com",
        "shaparak.ir", "automattic.com", "ssl-images-amazon.com", "setn.com", "today.com", "optimizely.com",
        "ow.ly", "readthedocs.io", "rambler.ru", "foursquare.com", "history.com", "hatenablog.com", "itu.int",
        "privacyshield.gov", "contextweb.com", "express.co.uk", "citi.com", "themeisle.com", "donya-e-eqtesad.com",
        "indiamart.com", "northwestern.edu", "techtarget.com", "squareup.com", "shein.com", "merdeka.com", "in.gr",
        "linksynergy.com", "alexa.com", "cloudflare.net", "theglobeandmail.com", "etherscan.io", "namu.wiki",
        "emxdgt.com", "utoronto.ca", "dot.gov", "rottentomatoes.com", "digitaltrends.com", "google.com.ua",
        "hicloud.com", "chinaz.com", "hollywoodreporter.com", "drupal.org", "mystrikingly.com",
        "proiezionidiborsa.it", "urbandictionary.com", "dictionary.com", "filesusr.com", "libsyn.com",
        "imageshack.us", "unc.edu", "51yes.com", "moz.com", "tableau.com", "cbssports.com", "siemens.com",
        "amazon.com.mx", "newscientist.com", "exelator.com", "tokopedia.com", "ticketmaster.com",
        "adsymptotic.com", "sberbank.ru", "360yield.com", "genius.com", "nhk.or.jp", "google.nl",
        "hindustantimes.com", "goo.ne.jp", "mitre.org", "coupang.com", "lemonde.fr", "id5-sync.com", "icann.org",
        "cutt.ly", "boston.com", "indianexpress.com", "ssrn.com", "houzz.com", "nymag.com", "flashtalking.com",
        "woocommerce.com", "justice.gov", "wufoo.com", "albawabhnews.com", "alicdn.com", "neobux.com", "lowes.com",
        "admin.ch", "heavy.com", "illinois.edu", "fb.watch", "angelfire.com", "gallup.com", "apachefriends.org",
        "kernel.org", "w55c.net", "adjust.com", "sap.com", "mercadolivre.com.br", "openssl.org", "gamespot.com",
        "line.biz", "nicovideo.jp", "xe.com", "focus.cn", "mixpanel.com", "google.ro", "mapquest.com",
        "crunchbase.com", "gstatic.com", "myworkdayjobs.com", "audible.com", "pwc.com", "hostgator.com", "dan.com",
        "documentforce.com", "sba.gov", "google.com.vn", "is.gd", "bugsnag.com", "asu.edu", "biblegateway.com",
        "iana.org", "mercari.com", "metro.co.uk", "icio.us", "science.org", "unity3d.com"]
    driver = DriverManager.generate_driver()
    for name in names:
        print(get_bing_login_pages(driver, name, count_of_results=3))
    driver.quit()
