#! /usr/bin/env python
#coding=utf-8
'''
Created on 2018年7月2日
爬108社区
@author: Administrator
'''
import re
import time
from post import post
import urllib2
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from twisted.python.runtime import seconds



url = "http://shangyu.108sq.com"
links = {}

#声明浏览器
def driver_open():
   dcap = dict(DesiredCapabilities.PHANTOMJS)
   #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
   dcap["phantomjs.page.settings.userAgent"] = (r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36") 
   #打开带配置信息的phantomJS浏览器
   driver = webdriver.PhantomJS(executable_path="D:\System sofeware\python27\Scripts\phantomjs.exe",desired_capabilities=dcap)
   # 隐式等待10秒，可以自己调节
   driver.implicitly_wait(10)
   # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
   # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
   driver.set_page_load_timeout(10)
   # 设置10秒脚本超时时间
   driver.set_script_timeout(20)
   return driver
#获取js加载后的页面
def get_content(driver,url):
    driver.get(url)
    time.sleep(10)
    content = driver.page_source.encode('utf-8')
    #关闭浏览器对象
    driver.close()
    soup = BeautifulSoup(content, 'lxml')
    return soup
    
    
#获取首页页面内容
def index(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {"User-Agent":user_agent}
    request = urllib2.Request(url=url,headers=headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response,'lxml')
    return soup

#获取108社区板块链接
def fornumlist():
    soup = index(url)
    fornumlist = soup.find_all('div',class_='Sq_leftNav_forum')
    list = fornumlist[0].find_all('li')
    for i in range(len(list)):
        link = ''
        link = url + list[i].find('a').get('href') 
        nm  = list[i].text
        links[nm] = link 

#每个板块内容        
def fornum(driver):  
    #link = links['找对象'.decode('utf-8')]
    #return link
    soup = get_content(driver, 'http://fuyang.108sq.com/shuo/forum/001002')
    return soup

#得到下一天的链接地址 
def nextpage(soup):
    page_content = soup.find('div',class_='pagination').find('a',class_='TCPage__next')
    next_link = url + page_content.get('href')
    return next_link
    
#获取每个帖子相关信息
def posts(soup):
   
    posts = soup.find_all('div',class_='TCSayList_li')
    #获取帖子id
    infoid = posts[0].get('info-id')
    #获取发布时间
    sec = posts[0].find('a',class_='TCSayList_li_time').get('data-time')
    #对发布时间格式化
    sec = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(sec)))
    #获取发布帖子用户id
    userid = posts[0].find('a',class_='TCSayList_li_author').get('data-tcuserpanel-uid') 
    #获取发布帖子用户名
    username = posts[0].find('a',class_='TCSayList_li_author').text
    #获取帖子点赞数
    up = posts[0].find('div',class_='TCSayList_li_handlers').find_all('span')[2].text
    #判断是否点赞
    if not up.isdigit():
        up = 0  
    #获取帖子评论数
    comment = posts[0].find('div',class_='TCSayList_li_handlers').find_all('span')[4].get_text()
    #判断是否评论
    if not comment.isdigit():
        comment = 0
    #填充对象post
    p = post(sec,infoid,userid,username,up,comment)
    return p
    
if __name__ == '__main__':
    driver = driver_open()
    soup = fornum(driver)
    print posts(soup).getallinfo()
    #退出webdriver
    driver.quit()
    #遍历字典，类似map
    #for key in links:
    #    print key + "\t\t\t" + links[key]
    