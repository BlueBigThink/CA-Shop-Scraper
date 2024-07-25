import requests
import json
from scraper.models import Website, Category, Product
from lxml import html

API_TIMEOUT = 100000

class KmstoolsScraper:
    def __init__(self) -> None:
        self.settings = None
        self.session = requests.session()
        self.category_count = 0
        self.product_count = 0
        self.html_tree = None
        self.categories = []
        pass

    def set_settings(self, settings):
        for key in ["name", "domain", "url", "label"]:
            if key not in settings:
                print(f"{key} is absent in settings")
                return False
        self.settings = settings
        return True

    def create_site(self, name, domain, url):
        try:
            site = Website.objects.get(name=name)
            return site
        except Website.DoesNotExist:
            site = Website.objects.create(name=name, domain=domain, url=url)
            return site
        except Exception as e:
            raise e

    def create_category(self, site, category, level, parent = None, parent_paths = []):
        cat_paths = parent_paths.copy()
        cat_paths.append(cat_info["name"])
        try:
            category = Category.objects.get(site=site, orig_id=cat_info["id"])
            self.category_count += 1
            category.orig_path = " > ".join(cat_paths)
            category.save()
            print("-" * level, f"{self.category_count} : {category.name}: {cat_paths}")
        except Category.DoesNotExist:
            role = "leaf"
            if len(cat_info["subcategories"]) > 0:
                role ="node"
            category = Category.objects.create(
                site = site, 
                name = cat_info["name"],
                url = f"{site.url}{cat_info["url"]}",
                role = role,
                level = level,
                orig_id = cat_info["id"],
                parent = parent,
                orig_path = " > ".join(cat_paths)
            )
            self.category_count += 1
            print("+" * level, f"{self.category_count} : {category.name}: {cat_paths}")
        except Exception as e:
            raise e
        for subcat in cat_info["subcategories"]:
            self.create_category(site, subcat, level + 1, category, cat_paths)

    def create_categories_for_site(self, site):
        print("make categories ...")
        resp = self.session.get(
            self.settings["url"],
            timeout = API_TIMEOUT
        )
        self.html_tree = html.fromstring(resp.text)
        li_cateory_parents = self.html_tree.cssselect('ul#navpro-topnav')[0].cssselect('div.navpro-dropdown.navpro-dropdown-level1.size-small')[0].cssselect('ul.children')[0].cssselect('li.parent')
        for li_cateory_parent in li_cateory_parents:
            name = li_cateory_parent.cssselect('a')[0].cssselect('span')[0].text_content().strip()
            url = li_cateory_parent.cssselect('a')[0].get('href')
            sub_categories = []
            for li_item in li_cateory_parent.cssselect('li.li-item'):
                sub_name = li_item.cssselect('a')[0].cssselect('span')[0].text_content().strip()
                sub_url = li_item.cssselect('a')[0].get('href')
                sub_categories.append({
                    'name' : sub_name,
                    'url' : sub_url
                })
            self.categories.append({
                'name' : name,
                'url' : url,
                'sub_categories' : sub_categories
            })
        print(self.categories)
        for category in self.categories:
            self.create_category(site, category, 1)

    def start(self):
        print("start to scrape ...")
        if self.settings is None:
            print(f"settings should be setted, first.")
            return
        site = self.create_site(self.settings["name"], self.settings["domain"], self.settings["url"]) 
        self.create_categories_for_site(site)
        # self.create_products_for_site(site)
