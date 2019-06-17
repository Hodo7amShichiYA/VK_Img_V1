from selenium import webdriver
from lxml import etree
import time
from time import sleep
def vkimg(userid):
    email = 'x'
    pwd = 'x'
    with open('./%s lasturl.txt'%userid, 'r+') as l:
        url = l.read()
    print('地址获取成功')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(30)
    browser.get("https://vk.com/feed")
    print('LOGIN...')
    elem = browser.find_element_by_id('email')
    elem.send_keys(email)
    elem = browser.find_element_by_id('pass')
    elem.send_keys(pwd)
    elem = browser.find_element_by_id('login_button')
    elem.click()
    print('登录完成')

    browser.get(url)
    starttime = time.time()
    for i in range(1,40000):
        pst = time.time()
        sleep(3)
        response = browser.page_source
        html = etree.HTML(response)
        html_data = html.xpath('//*[@id="pv_photo"]/img/@src')[0]
        print('获取完成')
        pageurl = browser.current_url
        print('正在抓取第%s页的页面代码:%s' % (i,pageurl))
        with open('./%s lasturl.txt'%userid, 'w') as tf:
            tf.write(pageurl)
        print('获取完成')
        with open('./%s url.txt'%userid, 'a') as f:
            f.write('%s\n'%html_data)
        print('第%s页图片地址抓取完成' % i)
        elem = browser.find_element_by_id('pv_photo')
        elem.click()
        pet = time.time()
        print('第%s张图片抓取用时%d秒'%(i,(pet-pst)))
    browser.quit()
    endtime = time.time()
    print('程序执行时长：%d 秒'%(endtime-starttime))
if __name__ == "__main__":
    userid = input('输入本次抓取的文件名：')
    print('尝试获取上次保存的地址')
    try:
        with open('./'+userid+' lasturl.txt', 'r+') as f:
            aa = f.read()
            print(aa)
    except:
        intro = input('初次抓取请填入第一张图片的地址：')
        with open('./%s lasturl.txt' % userid, 'w') as lu:
            lu.write(intro)
    vkimg(userid)
