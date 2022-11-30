import requests
import lxml.etree as etree
import re
import json


class FoodCom:
    # def __init__(self, postcode: int, lon: float, lat: float, retry: int = 3):
    def __init__(self, online_mode, retry: int = 3):
        """
        init a FoodCom obj
        :param postcode:
        :param lon:
        :param lat:
        :param retry: times of retry when bad network
        """
        # self.postcode = postcode
        # self.lon = lon
        # self.lat = lat
        self.rank_page_no = 0
        self.recipe_records = {}
        self.search_key_words = "grape salad"
        self.retry = retry
        
        self.online_mode=online_mode

    def rank_page(self, rank_page_no: int = None) -> dict:
        """
        get one page of top ranked recipes (ranked by trending)
        :param rank_page_no: page_number
        :return: info["available"] (bool) means network status, info["recipes"] is the ranked recipes result
        """
        if rank_page_no is None:
            # go to the next page
            self.rank_page_no += 1
        else:
            # go to the input page
            self.rank_page_no = rank_page_no

        # the website use 2 different urls when getting ranked recipes on the first page and on other pages
        # the first page
        if self.rank_page_no == 1:
            headers = {
                'authority': 'www.food.com',
                'method': 'GET',
                'path': '/recipe/all/trending',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cookie': '_pbjs_userid_consent_data=3524755945110770; usprivacy=1YNY; gig_bootstrap_3_-YpMMN5PDDnj1ri65ssss6K9Hq9y-y13U1TnjyjKSIxXJOuvE81IhyaP-BOkmb0v=_gigya_ver4; OneTrustWPCCPAGoogleOptOut=false; __gads=ID=5712bf5d1c1dfe1b:T=1668261613:S=ALNI_Maan8VDrSBOTvWFgZgxpdUOXThRfQ; _gcl_au=1.1.1430657068.1668261619; _lr_env_src_ats=false; _bs=cb83858f-1a45-65f2-aa4c-8d4b9105ef53; s_nr=1668262402323; krg_uid=%7B%22v%22%3A%7B%22clientId%22%3A%2241dfc787-4780-413a-850a-e101f150f94a%22%2C%22userId%22%3A%22523fbff4-e717-018a-111b-0dba48050e01%22%2C%22optOut%22%3Afalse%7D%7D; krg_crb=%7B%22v%22%3A%22eyJjbGllbnRJZCI6IjQxZGZjNzg3LTQ3ODAtNDEzYS04NTBhLWUxMDFmMTUwZjk0YSIsInRkSUQiOiIyODUxMzZkYi0xODA0LTQ2YjMtYmE2Yi0yYjhmYjFlMDUxZWQiLCJsZXhJZCI6IjUyM2ZiZmY0LWU3MTctMDE4YS0xMTFiLTBkYmE0ODA1MGUwMSIsInN5bmNJZHMiOnsiMjMiOiI4MTA2NjJkZi01ZTAzLTQ2MDAtYjI5YS02ZGY5ODJjM2IyYzciLCIyNSI6IjI4NTEzNmRiLTE4MDQtNDZiMy1iYTZiLTJiOGZiMWUwNTFlZCIsIjI5IjoiNjY0NjEwNzU4OTI4NTU1NzY4NyIsIjc0IjoiQ0FFU0VNcFFMMmtQeklBZnQxLWx0a2pscUt3IiwiOTciOiJ5LUZ0VXNFMmhFMnB1aE1aWmdjV0NNUzc0QTlGSG1NQkFGZnRZLX5BIiwiMl8xNiI6IkNBRVNFTXBRTDJrUHpJQWZ0MS1sdGtqbHFLdyIsIjJfODAiOiI4MTA2NjJkZi01ZTAzLTQ2MDAtYjI5YS02ZGY5ODJjM2IyYzciLCIyXzkzIjoiMjg1MTM2ZGItMTgwNC00NmIzLWJhNmItMmI4ZmIxZTA1MWVkIn0sImt0Y0lkIjoiYTM1OTMwMGUtZDk3Yi0wMmFhLTU1YmQtOGI4ZDNiNGQ5NmE0IiwiZXhwaXJlVGltZSI6MTY2ODQwMDI2Mzc2MSwibGFzdFN5bmNlZEF0IjoxNjY4MzEzODYzNzYxLCJwYWdlVmlld0lkIjoiIiwicGFnZVZpZXdUaW1lc3RhbXAiOjE2NjgzMTM4NTc1ODIsInBhZ2VWaWV3VXJsIjoiaHR0cHM6Ly93d3cuZm9vZC5jb20vc2VhcmNoLyIsInVzcCI6IjFZTlkifQ%3D%3D%22%7D; gig_canary=true; cto_bundle=quZAZF9KcXc2aUliRkNtUXZrUWVVWlp5a2Z3SnBySSUyQiUyQmtDTVV0a3pma3YwWU9vRXhMT3IwZ0tTYTFGQ3FlSnJBJTJCQXQlMkJTcW1JMkNsNjVDdE1oMkJFOHJMWE9ZJTJGVlo2VGs5UGVxJTJCSzg5TkV0aVU1NWRCJTJGV0dFRlhYeFE1TnJXTGNnJTJGNCUyRnVZZ2NRMzRKY2tXSzRhN0R4dmRPN1ElM0QlM0Q; _lr_geo_location=HK; RT="z=1&dm=food.com&si=42b3c2a2-6d55-4832-833d-f4e67e784fba&ss=lah07ibi&sl=0&tt=0&bcn=%2F%2F684d0d4a.akstat.io%2F"; AMCVS_BC501253513148ED0A490D45%40AdobeOrg=1; AMCV_BC501253513148ED0A490D45%40AdobeOrg=-2121179033%7CMCIDTS%7C19311%7CMCMID%7C25059505012901603493820485581044046737%7CMCAAMLH-1669126147%7C11%7CMCAAMB-1669126147%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1668528547s%7CNONE%7CvVersion%7C5.3.0; s_cc=true; gig_canary=false; gig_canary_ver=13455-3-27808650; __gpi=UID=000008f8203a002e:T=1668261613:RT=1668521358:S=ALNI_MY-Z7sbEsavTkVzAqfKD_lmXKfU9w; s_sq=%5B%5BB%5D%5D; OptanonConsent=isIABGlobal=false&datestamp=Tue+Nov+15+2022+22%3A09%3A53+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202209.2.0&hosts=&consentId=7dff4759-a3a6-4f33-97d0-c97f4392e309&interactionCount=1&landingPath=NotLandingPage&groups=BG1673%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=HK%3B; OptanonAlertBoxClosed=2022-11-15T14:09:53.037Z',
                'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
            }
            for i in range(self.retry):
                r = requests.get(url="https://www.food.com/recipe/all/trending", headers=headers)
                if r.status_code == requests.status_codes.codes.ok:
                    break
            if r.status_code == requests.status_codes.codes.ok:
                s = r.text
                pattern = r'"https://www\.food\.com/recipe/[a-z0-9\-]+-[0-9]+"'
                recipes_urls = set(re.findall(pattern=pattern, string=s))
                recipes_urls = {i[1:-1] for i in recipes_urls}
                info = {"available": True}
                info["recipes"] = {}
                for url in recipes_urls:
                    tmp = url.split("/")[-1].split("-")
                    recipe_name = tmp[:-1]
                    recipe_name = "".join([_ + " " for _ in recipe_name])[:-1]
                    recipe_id = tmp[-1]
                    info["recipes"][recipe_name] = recipe_id
                    self.recipe_records[recipe_id] = url
                r.close()
            else:
                info = {"available": False}

        # other pages
        else:
            headers = {
                "authority": r"api.food.com",
                "method": r"GET",
                "path": r"/services/mobile/fdc/search/sectionfront?pn={page_number}&recordType=Recipe&sortBy=trending&collectionId=17".format(
                    page_number=self.rank_page_no),
                "scheme": r"https",
                "accept": r"application/json, text/javascript, */*; q=0.01",
                "accept-encoding": r"gzip, deflate, br",
                "accept-language": r"zh-CN,zh;q=0.9",
                "content-type": r"application/json",
                "origin": r"https://www.food.com",
                "referer": r"https://www.food.com/",
                "sec-ch-ua": r'"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": r"?0",
                "sec-ch-ua-platform": r'"macOS"',
                "sec-fetch-dest": r"empty",
                "sec-fetch-mode": r"cors",
                "sec-fetch-site": r"same-site",
                "user-agent": r"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
            }
            url = "https://api.food.com/services/mobile/fdc/search/sectionfront?pn={page_number}&recordType=Recipe&sortBy=trending&collectionId=17".format(
                page_number=self.rank_page_no)
            for i in range(self.retry):
                r = requests.get(url, headers=headers)
                if r.status_code == requests.status_codes.codes.ok:
                    break
            if r.status_code == requests.status_codes.codes.ok:
                recipes_urls_new_page = []
                for _ in r.json()["response"]["results"]:
                    try:
                        if _["recordType"] == "Recipe":
                            recipes_urls_new_page.append(_["record_url"])
                    except:
                        continue
                info = {"available": True}
                info["recipes"] = {}
                for url in set(recipes_urls_new_page):
                    tmp = url.split("/")[-1].split("-")
                    recipe_name = tmp[:-1]
                    recipe_name = "".join([_ + " " for _ in recipe_name])[:-1]
                    recipe_id = tmp[-1]
                    info["recipes"][recipe_name] = recipe_id
                    self.recipe_records[recipe_id] = url
                r.close()
            else:
                info = {"available": False}

        return info

    def search(self, key_words: str = None) -> dict:
        """
        search for recipes according to any keywords input and get the one page of searching results
        :param key_words: keywords related the intended recipe
        :return: info["available"] (bool) means network status, info["recipes"] is the searching results
        """
        if key_words is None:
            self.search_page += 1
        else:
            self.search_page = 1
            self.search_key_words = key_words
        headers = {
            "authority": "api.food.com",
            "method": "POST",
            "path": "/external/v1/nlp/search",
            "scheme": "https",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.food.com",
            "referer": "https://www.food.com/",
            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"
        }
        payload = {"contexts": [], "searchTerm": self.search_key_words, "pn": self.search_page}
        data = json.dumps(payload)
        headers["content-length"] = str(len(data) - 5)
        for i in range(self.retry):
            r = requests.post(url="https://api.food.com/external/v1/nlp/search", headers=headers,
                              data=json.dumps(payload))
            if r.status_code == requests.status_codes.codes.ok:
                break
        info = {}
        if r.status_code == requests.status_codes.codes.ok:
            response_dict = r.json()
            r.close()
            info["available"] = True
            info["recipes"] = {}
            available_count = int(response_dict["response"]["totalResultsCount"]) - \
                              int(response_dict["response"]["parameters"]["offset"])
            if available_count > 0:
                for record in response_dict["response"]["results"]:
                    if record["recordType"] == "Recipe":
                        url = record["record_url"]
                        tmp = url.split("/")[-1].split("-")
                        recipe_name = tmp[:-1]
                        recipe_name = "".join([_ + " " for _ in recipe_name])[:-1]
                        recipe_id = tmp[-1]
                        self.recipe_records[recipe_id] = url
                        info["recipes"][recipe_name] = {
                            "title": record["main_title"],
                            "time_by_minutes": record["recipe_totaltime"],
                            "num_steps": record["num_steps"],
                            "num_ratings": record["main_num_ratings"],
                            "rating": record["main_rating"],
                            "recipe_id": recipe_id
                        }
        else:
            info["available"] = False
        return info

    def one_recipe_detail(self, recipe_id: str) -> dict:
        """
        get detailed information about one recipe
        :param recipe_id:
        :return: dict recipe info
        """
        info = {}
        if recipe_id in self.recipe_records:
            info["legal"] = True
            # get basic recipe information
            url = self.recipe_records[recipe_id]
            headers = {
                "authority": r'www.food.com',
                "method": r'GET',
                "path": r'/recipe/n-y-c-corned-beef-and-cabbage-15846?units=metric&scale=1',
                "scheme": r'https',
                "accept": r'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                "accept-encoding": r'gzip, deflate, br',
                "accept-language": r'zh-CN,zh;q=0.9',
                "cookie": r'_pbjs_userid_consent_data=3524755945110770; usprivacy=1YNY; gig_bootstrap_3_-YpMMN5PDDnj1ri65ssss6K9Hq9y-y13U1TnjyjKSIxXJOuvE81IhyaP-BOkmb0v=_gigya_ver4; OneTrustWPCCPAGoogleOptOut=false; __gads=ID=5712bf5d1c1dfe1b:T=1668261613:S=ALNI_Maan8VDrSBOTvWFgZgxpdUOXThRfQ; _gcl_au=1.1.1430657068.1668261619; _lr_env_src_ats=false; _bs=cb83858f-1a45-65f2-aa4c-8d4b9105ef53; s_nr=1668262402323; krg_uid=%7B%22v%22%3A%7B%22clientId%22%3A%2241dfc787-4780-413a-850a-e101f150f94a%22%2C%22userId%22%3A%22523fbff4-e717-018a-111b-0dba48050e01%22%2C%22optOut%22%3Afalse%7D%7D; krg_crb=%7B%22v%22%3A%22eyJjbGllbnRJZCI6IjQxZGZjNzg3LTQ3ODAtNDEzYS04NTBhLWUxMDFmMTUwZjk0YSIsInRkSUQiOiIyODUxMzZkYi0xODA0LTQ2YjMtYmE2Yi0yYjhmYjFlMDUxZWQiLCJsZXhJZCI6IjUyM2ZiZmY0LWU3MTctMDE4YS0xMTFiLTBkYmE0ODA1MGUwMSIsInN5bmNJZHMiOnsiMjMiOiI4MTA2NjJkZi01ZTAzLTQ2MDAtYjI5YS02ZGY5ODJjM2IyYzciLCIyNSI6IjI4NTEzNmRiLTE4MDQtNDZiMy1iYTZiLTJiOGZiMWUwNTFlZCIsIjI5IjoiNjY0NjEwNzU4OTI4NTU1NzY4NyIsIjc0IjoiQ0FFU0VNcFFMMmtQeklBZnQxLWx0a2pscUt3IiwiOTciOiJ5LUZ0VXNFMmhFMnB1aE1aWmdjV0NNUzc0QTlGSG1NQkFGZnRZLX5BIiwiMl8xNiI6IkNBRVNFTXBRTDJrUHpJQWZ0MS1sdGtqbHFLdyIsIjJfODAiOiI4MTA2NjJkZi01ZTAzLTQ2MDAtYjI5YS02ZGY5ODJjM2IyYzciLCIyXzkzIjoiMjg1MTM2ZGItMTgwNC00NmIzLWJhNmItMmI4ZmIxZTA1MWVkIn0sImt0Y0lkIjoiYTM1OTMwMGUtZDk3Yi0wMmFhLTU1YmQtOGI4ZDNiNGQ5NmE0IiwiZXhwaXJlVGltZSI6MTY2ODQwMDI2Mzc2MSwibGFzdFN5bmNlZEF0IjoxNjY4MzEzODYzNzYxLCJwYWdlVmlld0lkIjoiIiwicGFnZVZpZXdUaW1lc3RhbXAiOjE2NjgzMTM4NTc1ODIsInBhZ2VWaWV3VXJsIjoiaHR0cHM6Ly93d3cuZm9vZC5jb20vc2VhcmNoLyIsInVzcCI6IjFZTlkifQ%3D%3D%22%7D; gig_canary=true; cto_bundle=quZAZF9KcXc2aUliRkNtUXZrUWVVWlp5a2Z3SnBySSUyQiUyQmtDTVV0a3pma3YwWU9vRXhMT3IwZ0tTYTFGQ3FlSnJBJTJCQXQlMkJTcW1JMkNsNjVDdE1oMkJFOHJMWE9ZJTJGVlo2VGs5UGVxJTJCSzg5TkV0aVU1NWRCJTJGV0dFRlhYeFE1TnJXTGNnJTJGNCUyRnVZZ2NRMzRKY2tXSzRhN0R4dmRPN1ElM0QlM0Q; _lr_geo_location=HK; OptanonConsent=isIABGlobal=false&datestamp=Tue+Nov+15+2022+01%3A05%3A40+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202209.2.0&hosts=&consentId=7dff4759-a3a6-4f33-97d0-c97f4392e309&interactionCount=1&landingPath=NotLandingPage&groups=BG1673%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=HK%3B; OptanonAlertBoxClosed=2022-11-14T17:05:40.327Z; RT="z=1&dm=food.com&si=42b3c2a2-6d55-4832-833d-f4e67e784fba&ss=lah07ibi&sl=0&tt=0&bcn=%2F%2F684d0d4a.akstat.io%2F"; AMCVS_BC501253513148ED0A490D45%40AdobeOrg=1; AMCV_BC501253513148ED0A490D45%40AdobeOrg=-2121179033%7CMCIDTS%7C19311%7CMCMID%7C25059505012901603493820485581044046737%7CMCAAMLH-1669126147%7C11%7CMCAAMB-1669126147%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1668528547s%7CNONE%7CvVersion%7C5.3.0; s_cc=true; gig_canary=false; gig_canary_ver=13455-3-27808650; __gpi=UID=000008f8203a002e:T=1668261613:RT=1668521358:S=ALNI_MY-Z7sbEsavTkVzAqfKD_lmXKfU9w; s_sq=%5B%5BB%5D%5D',
                "sec-ch-ua": r'"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": r'?1',
                "sec-ch-ua-platform": r'"Android"',
                "sec-fetch-dest": r'document',
                "sec-fetch-mode": r'navigate',
                "sec-fetch-site": r'none',
                "sec-fetch-user": r'?1',
                "upgrade-insecure-requests": r'1',
                "user-agent": r'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
            }
            for i in range(self.retry):
                r = requests.get(url + r'?units=metric&scale=1', headers=headers)
                if r.status_code == requests.status_codes.codes.ok:
                    break
            if r.status_code == requests.status_codes.codes.ok:
                info["recipe_available"] = True
                info["data"] = {}
                data = info["data"]

                # recipe id
                data["id"] = recipe_id
                html = etree.HTML(r.text)
                r.close()

                # title
                data["title"] = \
                    html.xpath('//*[@id="recipe"]/div[@class="layout__item title svelte-d43h84"]/h1/text()')[0]

                # author & description
                try:
                    author_description_xpath = '//*[@id="recipe"]/div[@class="layout__item author-description svelte-d43h84"]/div[@class="author-description svelte-5nsvrc"]'
                    author_description = html.xpath(author_description_xpath)[0]
                    # author
                    try:
                        author = author_description.xpath(
                            './div[@class="author svelte-7q12ny"]/div[@class="byline svelte-7q12ny"]')[0]
                        assert author.text.replace(" ", "").replace("\n", "") == 'Submittedby'
                        data["author"] = author.xpath('./a/text()')[0]
                    except:
                        data["author"] = "unknown"
                    # description
                    try:
                        description_xpath = './div[@class="recipe-description paragraph"]'
                        description_xpath += '/div[@class="text-truncate svelte-hbkwz9"]'
                        description_xpath += '/div[@class="text svelte-hbkwz9 truncated"]'
                        description_xpath += '/text()'
                        data["description"] = "".join([x + " " for x in
                                                       "".join([_ + " " for _ in author_description.xpath(
                                                           description_xpath)]).replace(
                                                           "\n",
                                                           " ").split(
                                                           " ") if len(x) > 0])[:-1]
                    except:
                        data["description"] = "..."
                except:
                    data["author"] = "unknown"
                    data["description"] = "..."

                # cooking time & kinds of ingredients
                has_time = False
                has_kinds = False
                data["ingredients"] = {}
                ingredients = data["ingredients"]
                try:
                    facts_xpath = '//*[@id="recipe"]/div[@class="layout__item details svelte-d43h84"]'
                    facts_xpath += '/div[@class="facts svelte-d43h84"]'
                    facts_xpath += '/dl[@class="svelte-d43h84"]'
                    facts_xpath += '/div[@class="facts__item svelte-d43h84"]'
                    for div in html.xpath(facts_xpath):
                        prefix = div.xpath("./dt/text()")[0]
                        if prefix == 'Ready In:':  # cooking time
                            data["time"] = div.xpath("./dd/text()")[0]
                            has_time = True
                        elif prefix == 'Ingredients:':  # kinds
                            ingredients["kinds"] = div.xpath("./dd/text()")[0].replace(" ", "").replace("\n", "")
                            has_kinds = True
                    if not has_time:
                        data["time"] = "unknown"
                    if not has_kinds:
                        ingredients["kinds"] = "unknown"
                except:
                    data["time"] = "unknown"
                    ingredients["kinds"] = "unknown"

                # ingredient list dedtail
                igd_all_xpath = '//*[@id="recipe"]'
                igd_all_xpath += '/section[@class="layout__item ingredients svelte-d43h84"]'
                igd_all_xpath += '/ul[@class="ingredient-list svelte-d43h84"]/li'
                igd_all = html.xpath(igd_all_xpath)
                igd_all_detail = []
                for li in igd_all:
                    try:
                        amt = "".join(li.xpath('./span[@class="ingredient-quantity svelte-d43h84"]/text()'))
                        if float(amt) == 0:
                            amt = ""
                        igd_detail = "".join(
                            [x + " " for x in li.xpath('./span[@class="ingredient-text svelte-d43h84"]')[
                                0].itertext()]).replace("\n", "")
                        igd_detail = "".join([x + " " for x in igd_detail.split(" ") if len(x) > 0])[:-1]
                        igd_all_detail.append({"amt": amt, "detail": igd_detail})
                    except:
                        continue
                ingredients["detail"] = igd_all_detail

                # cooking directions
                directions_xpath = '//*[@id="recipe"]'
                directions_xpath += '/section[@class="layout__item directions svelte-d43h84"]'
                directions_xpath += '/ul[@class="direction-list svelte-d43h84"]'
                directions_xpath += '/li[@class="direction svelte-d43h84"]'
                data["directions"] = [x.text.replace("\n", " ").replace("\t", " ") for x in
                                      html.xpath(directions_xpath)]

                # get nutrition table
                script_info = html.xpath(
                    '//*[@id="top"]/div[@class="body svelte-1sprt3h"]/script[@type="application/ld+json"]/text()')[
                    0]
                script_info = json.loads(script_info)
                yields_text = script_info["recipeYield"]
                # number start
                for si, s in enumerate(yields_text):
                    if s in '1234567890':
                        break
                yields_text = yields_text[si:]
                # number end
                for si, s in enumerate(yields_text):
                    if s not in '1234567890':
                        break
                yields = int(yields_text[:si])
                yields = max(1, yields)
                nutrition_raw = script_info["nutrition"]
                nutrition = {}
                for key in ['calories', 'fatContent', 'saturatedFatContent', 'cholesterolContent',
                            'sodiumContent',
                            'carbohydrateContent', 'fiberContent', 'sugarContent', 'proteinContent']:
                    nutrition[key] = float(nutrition_raw[key]) / yields
                data["nutrition"] = nutrition
            else:
                info["recipe_available"] = False

            # get approximate price and product list
            if info["recipe_available"]:
                recipe_tag = url.split("/")[-1]
                headers = {
                    'authority': r'widget.whisk.com',
                    'method': r'GET',
                    'path': r'/api/v2/recipes/_widget?url=https%3A%2F%2Fwww.food.com%2Frecipe%2F{recipe_tag}&user_country=US&user_zip={code}'.format(
                        code=self.postcode, recipe_tag=recipe_tag),
                    'scheme': r'https',
                    'accept': r'*/*',
                    'accept-encoding': r'gzip, deflate, br',
                    'accept-language': r'zh-CN,zh;q=0.9',
                    'origin': r'https://cdn.whisk.com',
                    'referer': r'https://cdn.whisk.com/',
                    'sec-ch-ua': r'"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                    'sec-ch-ua-mobile': r'?1',
                    'sec-ch-ua-platform': r'"Android"',
                    'sec-fetch-dest': r'empty',
                    'sec-fetch-mode': r'cors',
                    'sec-fetch-site': r'same-site',
                    'user-agent': r'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                    'whisk-timezone': r'Asia/Shanghai'
                }
                price_url = "https://widget.whisk.com/api/v2/recipes/_widget?url=https%3A%2F%2Fwww.food.com%2Frecipe%2F{recipe_tag}&user_country=US&user_zip={code}".format(
                    recipe_tag=recipe_tag, code=self.postcode)
                for i in range(self.retry):
                    r = requests.get(price_url, headers=headers)
                    if r.status_code == requests.status_codes.codes.ok:
                        break
                if r.status_code == requests.status_codes.codes.ok:
                    info["price available"] = True
                    response_json = r.json()
                    r.close()

                    # price
                    if response_json["checkoutOptions"]["displayCost"]:
                        totoal_price = response_json["checkoutOptions"]["availableInventories"][0]["priceDetails"][
                            'totalPrice']
                        try:
                            resipe_serves = response_json["checkoutOptions"]["recipe"]["recipeYield"]
                        except:
                            resipe_serves = yields
                        if resipe_serves == 0:
                            resipe_serves = yields
                        data["price"] = totoal_price / resipe_serves
                    else:
                        data["price"] = None

                    # product list
                    try:
                        data["product_list"] = response_json["metadata"]["productsInRecipe"]
                    except:
                        data["product_list"] = None
                else:
                    info["price available"] = False
        else:
            info["legal"] = False
        return info


if __name__ == "__main__":
    # init a FoodCom obj
    postcode = 15213
    lon = -79.9457835174865
    lat = 40.44587605455525
    myFoodCom = FoodCom(postcode, lon, lat)

    # how to use rank_page method ?
    print("get top ranked recipes")

    print("page 1")
    page1 = myFoodCom.rank_page()
    if page1["available"]:
        for recipe_name in page1["recipes"]:
            print(recipe_name, page1["recipes"][recipe_name])
    else:
        print("bad network")

    print("page 2")
    page2 = myFoodCom.rank_page()
    if page2["available"]:
        for recipe_name in page2["recipes"]:
            print(recipe_name, page2["recipes"][recipe_name])
    else:
        print("bad network")

    print("page 99")
    page99 = myFoodCom.rank_page(rank_page_no=99)
    if page99["available"]:
        for recipe_name in page99["recipes"]:
            print(recipe_name, page99["recipes"][recipe_name])
    else:
        print("bad network")

    # if you then call it again, it will continue based on the last call
    print("page 100")
    page100 = myFoodCom.rank_page()
    if page100["available"]:
        for recipe_name in page100["recipes"]:
            print(recipe_name, page100["recipes"][recipe_name])
    else:
        print("bad network")

    # how to use search method ?
    print('search for keywords "shrimp salad"')
    key_words = "shrimp salad"
    print("page 1")
    page1 = myFoodCom.search(key_words=key_words)
    if page1["available"]:
        print(len(page1["recipes"]), "recipe records at page 1")
        for record in page1["recipes"].values():
            print(
                f"{record['title']}({record['recipe_id']}), {record['time_by_minutes']} mins, {record['num_steps']} steps, rated {record['rating']} stars by {record['num_ratings']} people")
    else:
        print("bad network")

    print("the results may be more than 1 page")
    page_count = 1
    next_page = True
    while next_page:
        page_count += 1
        # if no input at param key_words, myFoodCom will go on the last search keywords and move to the next page
        page_n = myFoodCom.search()
        if page_n["available"]:
            count = len(page_n["recipes"])
            print("new {count} recipes at page {page_count}".format(count=count, page_count=page_count))
            if count == 0:
                next_page = False
        else:
            print("bad network at page {page_count}".format(page_count=page_count))
            next_page = False

    print('what if we input meaningless words "asd fgh jkl;"')
    key_words = "asd fgh jkl;"
    meaningless_search = myFoodCom.search(key_words=key_words)
    print(
        f"the network status is {meaningless_search['available']}, but response has {len(meaningless_search['recipes'])} recipe record")
    print(meaningless_search)

    # how to use one_recipe_detail method
    print("if we want detailed information of shrimp salad with pineapple and pecans(100852)")
    recipe_id = "100852"
    info = myFoodCom.one_recipe_detail(recipe_id)


    def display_recipe_detail(info):
        if info["legal"]:
            if info["recipe_available"]:
                data = info["data"]
                output_s = ""
                output_s += "-------------------------"
                output_s += info["data"]["title"]
                output_s += "-------------------------"
                output_s += "\n"
                output_s += "recipe id : "
                output_s += data["id"]
                output_s += "\n"
                output_s += "author : "
                output_s += data["author"]
                output_s += "\n"
                output_s += "description : "
                output_s += data["description"]
                output_s += "\n"
                output_s += "cooking time : "
                output_s += data["time"]
                output_s += "\n"
                output_s += "ingredients : "
                output_s += data["ingredients"]["kinds"]
                output_s += "\n"
                output_s += "----------"
                output_s += "directions"
                output_s += "----------"
                output_s += "\n"
                for di, d in enumerate(data["directions"]):
                    output_s += "%-2d %s\n" % (di + 1, d)
                output_s += "----------"
                output_s += "ingredients"
                output_s += "----------"
                output_s += "\n"
                for igd in data["ingredients"]["detail"]:
                    output_s += "%-8s %s\n" % (igd["amt"], igd["detail"])
                output_s += "----------"
                output_s += "nutrition table"
                output_s += "----------"
                output_s += "\n"
                output_s += "calories %.2f kcal\n" % data["nutrition"]["calories"]
                output_s += "fat %.2f g\n" % data["nutrition"]["fatContent"]
                output_s += "\t saturated fat %.2f g\n" % data["nutrition"]["saturatedFatContent"]
                output_s += "cholesterol %.2f mg\n" % data["nutrition"]["cholesterolContent"]
                output_s += "sodium %.2f mg\n" % data["nutrition"]["sodiumContent"]
                output_s += "carbohydrate %.2f g\n" % data["nutrition"]["carbohydrateContent"]
                output_s += "\t fiber %.2f g\n" % data["nutrition"]["fiberContent"]
                output_s += "\t sugar %.2f g\n" % data["nutrition"]["sugarContent"]
                output_s += "protein %.2f g\n" % data["nutrition"]["proteinContent"]
                if info["price available"]:
                    output_s += "----------"
                    output_s += "purchase recommendation"
                    output_s += "----------"
                    output_s += "\n"
                    if data["price"] is None:
                        output_s += "estimated cost per serve unavailable\n"
                    else:
                        output_s += 'estimated cost per serve %.2f $\n' % (data["price"] / 100)
                    if data["product_list"] is None or len(data["product_list"]) == 0:
                        output_s += "recommended product list unavailable\n"
                    else:
                        output_s += "recommended product list :\n"
                        for s in data["product_list"]:
                            output_s += "\t"
                            output_s += s.lower()
                            output_s += "\n"
                else:
                    output_s += "purchase data unavailable\n"
            else:
                output_s = "bad network"
        else:
            output_s = "unknown recipe id"
        print(output_s)
        return output_s


    display_recipe_detail(info)

    print("but if we try to get a recipe which is not shown before, it's illegal")
    recipe_id = "999999"
    info = myFoodCom.one_recipe_detail(recipe_id)
    display_recipe_detail(info)

    print("next step in dataflow")

    # googlemap
    print("googlemap input")
    print("lon",myFoodCom.lon)
    print("lat",myFoodCom.lat)
    print("postcode",myFoodCom.postcode)

    # foodkeeper
    print("foodkeeper input")
    print("if users want ingredients' preservation information of shrimp salad with pineapple and pecans(100852)")
    recipe_id = "100852"
    info = myFoodCom.one_recipe_detail(recipe_id)
    info["data"]["product_list"]