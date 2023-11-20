from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

class RateGain:
    def __init__(self):
        self.bot = webdriver.Chrome(executable_path='D:/chromedriver-win64/chromedriver')

    def get_blog_data(self, base_url):

        bot = self.bot
        all_data = []
        page_no = 1

        while True:
            url = f'{base_url}/page/{page_no}'
            bot.get(url)
            time.sleep(3)
            blog_titles = [title.text if title.text else None for title in bot.find_elements(By.XPATH, '/html/body/div[1]/main/div/article/div/div[2]/div[3]/div/div/div/div[1]/article/div/div/h6')]            
            if not blog_titles:
                break 
            blog_dates = [date.text if date.text else None for date in bot.find_elements(By.XPATH, '/html/body/div[1]/main/div/article/div/div[2]/div[3]/div/div/div/div[1]/article/div/div/div[1]/div[1]/span')]
            
            blog_image_urls = [img.get_attribute("data-bg") if img.get_attribute("data-bg") else None for img in bot.find_elements(By.XPATH, '/html/body/div[1]/main/div/article/div/div[2]/div[3]/div/div/div/div[1]/article/div/div[1]/a[1]')]
            
            blog_likes_count = [likes.text if likes.text else None for likes in bot.find_elements(By.XPATH, '/html/body/div[1]/main/div/article/div/div[2]/div[3]/div/div/div/div[1]/article/div/div/a[2]/span')]
            
            if not all(len(lst) == len(blog_titles) for lst in [blog_titles, blog_dates, blog_image_urls, blog_likes_count]):
                max_len = max(len(blog_titles), len(blog_dates), len(blog_image_urls), len(blog_likes_count))
                blog_titles += [None] * (max_len - len(blog_titles))
                blog_dates += [None] * (max_len - len(blog_dates))
                blog_image_urls += [None] * (max_len - len(blog_image_urls))
                blog_likes_count += [None] * (max_len - len(blog_likes_count))

            page_data = pd.DataFrame({
                'Title': blog_titles,
                'Date': blog_dates,
                'Image URL': blog_image_urls,
                'Likes Count': blog_likes_count
            })

            all_data.append(page_data)
            page_no += 1

        if all_data:
            all_data = pd.concat(all_data, ignore_index=True)

            all_data.to_csv('blog_data.csv', index=False)

        bot.quit()

base_url = 'https://rategain.com/blog' 
scraper = RateGain()
scraper.get_blog_data(base_url)
