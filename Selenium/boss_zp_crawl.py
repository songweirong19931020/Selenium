"""
@File : boss_zp_crawl.py
@copyright : Administrator
@Coder: Leslie_s
@Date: 2020/3/20 13:54
@Idea: PyCharm 
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

class Boss_Crawl(object):
    driver_path = r'C:\Program Files (x86)\Google\chromedriver.exe'
    def __init__(self):
        # options是为了防爬虫做的设置
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.url = 'https://www.zhipin.com/'

    def run(self, search):
        self.driver.get(self.url)
        inputTag = self.driver.find_element_by_class_name('ipt-search')
        inputTag.send_keys(search)
        inputTag.send_keys(Keys.RETURN)  # 用按钮用不了,用回车替代
        time.sleep(0.5)
        self.driver.find_element_by_link_text('武汉').click()  # 切换城市
        while True:
            self.parser_list_page()
            self.driver.find_element_by_class_name('next').click()
            source = BeautifulSoup(self.driver.page_source, 'html.parser')
            urls = source.find_all('div', class_='job-primary')


    def parser_list_page(self):
        source = BeautifulSoup(self.driver.page_source, 'html.parser')
        urls = source.find_all('div', class_='job-primary')
        for url in urls:
            pager_url = 'https://www.zhipin.com' + str(url.find('div', class_='primary-wrapper').a['href'])
            time.sleep(0.5)
            self.request_detail_page(pager_url)

    def request_detail_page(self, pager_url):
        self.driver.execute_script("window.open('%s')" % pager_url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        source = BeautifulSoup(self.driver.page_source, 'html.parser')
        position_info = source.find('div', class_='info-primary')
        pos = {}
        position_name = position_info.find('div', class_='name').find('h1').string  # 职位名称
        position_salary = position_info.find('span', class_='salary').string  # 职位薪水
        position_city = position_info.find('p').get_text()  # 工作城市
        position_work_years = position_info.find_all('em', class_='dolt')[0].get_text()  # 工作经验
        position_education = position_info.find_all('em', class_='dolt')[1].get_text()  # 学历
        position_status = position_info.find('div', class_='job-status').find('span').string
        print(position_name, position_salary, position_city, position_work_years, position_education)
        try:
            welfare = position_info.find('div', class_='job-tags').find_all('span')
        except:
            print('无福利，跳过此次循环！')
        # 职位要求
        position_inint = source.find('div', class_='job-detail')
        job_sec = position_inint.find('div', class_='text').get_text()  # 职位要求
        job_company = position_inint.find('div', class_='name').get_text()  # 公司信息
        ##公司信息
        position_sider_info = source.find('div', class_='sider-company')
        position_refsh = position_sider_info.find('p', class_='gray').string  # 刷新时间
        print('\n', '*' * 50)
        pos['position_name'] = position_name
        pos['position_salary'] = position_salary
        pos['position_city'] = position_city
        pos['position_work_years'] = position_work_years
        pos['position_education'] = position_education
        pos['job_sec'] = job_sec
        pos['position_status'] = position_status
        pos['job_company'] = job_company
        pos['position_refsh'] = position_refsh
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)

if __name__ == '__main__':
    Spider = Boss_Crawl()
    Spider.run('数据分析')
