#-*- coding:utf-8 -*-
from splinter.browser import Browser
import time
import argparse


def login(b,username,pwd):
	'''京东登陆'''
	b.click_link_by_text(u"你好，请登录")
	time.sleep(10)
	b.click_link_by_text(u"账户登录")
	time.sleep(4)
	b.fill("loginname",username)
	b.fill("nloginpwd",pwd)
	b.find_by_id("loginsubmit").click()
	time.sleep(3)
	return b


def loop(b,url):
	try:
		if b.title==u"订单结算页 -京东商城":
			b.find_by_text(u"保存收货人信息").click()
			b.find_by_text(u"保存支付及配送方式").click()
			b.find_by_id("order-submit").click()
			return b
		else:
			b.visit(url)
			b.find_by_id("btn-reservation").click()
			time.sleep(3)
			loop(b,url)
	except Exception as e:
		b.reload()
		time.sleep(2)
		loop(b,url)



def start(url,username,pwd):
	b = Browser(driver_name="firefox")
	b.visit(url)
	login(b,username,pwd)
	try:
		b.find_by_id("btn-reservation").click()
	except AttributeError as e:
		print('Error:', e)
	time.sleep(10)
	while True:
		loop(b,url)
		if b.is_element_present_by_id("tryBtn"):
			b.find_by_id("tryBtn").click()
			time.sleep(4)
		elif b.title==u"订单结算页 -京东商城":
			b.find_by_id("order-submit").click() 
		else:
			print(u'恭喜你，抢购成功')
			break



if __name__=="__main__":

	parser = argparse.ArgumentParser(description=u'京东抢购')
	parser.add_argument('-u', '--username', help=u'登录用户名', default='')
	parser.add_argument('-p', '--password', help=u'登录密码', default='')
	parser.add_argument('-l', '--url', help=u'抢购链接地址', default='')

	options = parser.parse_args()
	print options

	if options.username=="":
		print u'请输入登录用户名'
		exit(1)

	if options.password=="":
		print u'请输入登录密码'
		exit(1)

	if options.url == '':
		print u'请输入商品链接地址'
		exit(1)

	start(options.url,options.username,options.password)
