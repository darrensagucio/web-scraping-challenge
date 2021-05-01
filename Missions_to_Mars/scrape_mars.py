from splinter import Browser
from bs4 import BeautifulSoup as bs
import time 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 

def scrape():
    url_list = [
        'https://redplanetscience.com/',
        'https://spaceimages-mars.com',
        'https://galaxyfacts-mars.com',
        'https://marshemispheres.com/cerberus.html',
        'https://marshemispheres.com/schiaparelli.html',
        'https://marshemispheres.com/syrtis.html',
        'https://marshemispheres.com/valles.html'
    ]

    loop_count = 0
    count_hemispheres = 0 
    hemisphere_list = []

    for i in range(len(url_list)):
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        browser.visit(url_list[i])

        time.sleep(1)
        
        html = browser.html
        soup = bs(html, "html.parser")

        if loop_count == 0:
            news_block = soup.find('div', class_='list_text')
    
            recent_title = news_block.find_all('div', class_='content_title')[0].text
            recent_p = news_block.find_all('div', class_='article_teaser_body')[0].text

            mars_scrapedata = {
                'recent_title': recent_title,
                'recent_parag': recent_p
            }

            browser.quit()
        
        if loop_count == 1:
            featured_img_block = soup.find('div', class_='floating_text_area')
    
            featured_image_path = featured_img_block.find('a')["href"]
            featured_image_url = f'{url_list[i]}/{featured_image_path}'

            mars_scrapedata['featured_img_url'] = featured_image_url

            browser.quit()
        
        if loop_count == 2:
            tables = pd.read_html(url_list[i])
            df = tables[0]
            rename_column_df = df.rename(columns={0:'Mars - Earth Comparison', 1:'Mars', 2:'Earth'}, inplace=False)
            drop_row_df = rename_column_df.drop([0])
            clean_df = drop_row_df.set_index('Mars - Earth Comparison')
            html_table = clean_df.to_html()
            clean_html = html_table.replace('\n', '')
            mars_scrapedata['mars_table'] = clean_html
            browser.quit()
        
        if loop_count > 2:
            image_url = 'https://marshemispheres.com/'
            hemisphere_block = soup.find('div', class_ = 'downloads')
            hemisphere_ulsection = hemisphere_block.find('ul')
            hemisphere_lisection = hemisphere_ulsection.find_all('li')[0]
            hemisphere_path = hemisphere_lisection.find('a')["href"]
            hemisphere_url = image_url + hemisphere_path
    
            hemispheretitle = soup.find('h2', class_ = 'title').text
    
            hemisphere_image_title_urls = {
                'title':hemispheretitle,'img_url':hemisphere_url
            }
        
            hemisphere_list.append(hemisphere_image_title_urls)

            browser.quit()
            
            count_hemispheres += 1
            
            if count_hemispheres == 4:
                mars_scrapedata['hemisphere_urls'] = hemisphere_list

        loop_count += 1    

    return mars_scrapedata