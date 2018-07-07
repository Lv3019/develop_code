#! /usr/bin/env python
#coding=utf-8

'''
    定义108社区帖子对象
'''
class post():
    #发布时间
    create_time = ''
    #帖子id
    infoid = ''
    #用户id
    userid = ''
    #用户name
    username = ''
    #点赞数
    up = 0
    #评论数
    comment= 0
    #初始化
    def __init__(self,create_time,infoid,userid,username,up,comment):
        self.create_time = create_time
        self.infoid = infoid
        self.userid = userid
        self.username = username
        self.up = up
        self.comment = comment
    
    def getallinfo(self):
        return "用户名:%s 用户id:%s 帖子id:%s 发布时间:%s 点赞数:%s 评论数:%s".decode('utf-8') % (self.username,self.userid,self.infoid,self.create_time,self.up,self.comment)    
    
    def getuserid(self):
        return self.userid
    def getusername(self):
        return self.username
    def getinfoid(self):
        return self.infoid
    def getcreatetime(self):
        return self.create_time
    def getup(self):
        return self.up
    def getcomment(self):
        return self.comment
    