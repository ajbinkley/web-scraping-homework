

# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data_dict = {}

    # # NASA Mars News


    # In[34]:


    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)


    # In[35]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[49]:


    news_title = soup.find_all('li', class_='slide')[0].select('div.content_title')[0].text
    news_p = soup.find_all('li', class_='slide')[0].text


    # # JPL Mars Space Images - Featured Image

    # In[8]:


    # URL of JPL Mars Space Images page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


    # In[9]:


    # Retrieve page with the requests module
    response = requests.get(jpl_url)


    # In[10]:


    # Create BeautifulSoup object; parse with 'html.parser'
    jpl_soup = BeautifulSoup(response.text, 'html.parser')


    # In[11]:


    #print(jpl_soup.prettify())


    # In[12]:


    domain = 'https://www.jpl.nasa.gov'
    image = jpl_soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')


    # In[13]:


    relative_img_url = image.article['style'][23:-3]


    # In[14]:


    featured_image_url = domain + relative_img_url


    # # Mars Weather


    # In[17]:


    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)


    # In[18]:


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[31]:


    mars_weather = soup.find('li', class_='js-stream-item stream-item stream-item ').p.text


    # # Mars Facts

    # In[ ]:


    url = 'https://space-facts.com/mars/'


    # In[ ]:


    tables = pd.read_html(url)

    # In[ ]:


    df = tables[0]
    df.columns = ['description','value']
    df.set_index('description', inplace=True)


    # In[ ]:


    html_table = df.to_html()


    # In[ ]:


    html_table = html_table.replace('\n', '')


    # # Mars Hemispheres


    # In[ ]:


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)


    # In[ ]:


    css_selector_begin = '#product-section > div.collapsible.results > div:nth-child('
    css_selector_end = ') > div > a > h3'
    hemisphere_image_urls = []

    for x in range(1, 5):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        css_selector_full = css_selector_begin + str(x) + css_selector_end

        browser.find_by_css(css_selector_full).click()

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')


        image_url = soup.find('img', class_='wide-image')['src']
        
        hemi_title = soup.find('h2', class_='title').text
        
        image_dict = {'title':hemi_title, 'img_url':'https://astrogeology.usgs.gov/' + image_url}
        
        hemisphere_image_urls.append(image_dict)

        browser.find_by_css('#splashy > div.wrapper > div.container > div.content > section > a').click()

    mars_data_dict = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': html_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }
    
    return mars_data_dict

