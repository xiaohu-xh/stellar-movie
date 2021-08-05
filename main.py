import threading
import StellarPlayer
import os
import shutil
import traceback
import sys 
import importlib
import json

class uiplugin(StellarPlayer.IStellarPlayerPlugin):
    def __init__(self,player:StellarPlayer.IStellarPlayer):
        super().__init__(player)
        print("init zhibo plugin")
        self.search_ret = []
        self.resources = []
        with open(__file__.replace('main.py',"data.csv"),'r', encoding='UTF-8') as f:
            for line in f:
                eles = line.split(",")
                if (len(eles) < 2):
                    continue
                eles[0] = eles[0].replace('[电影天堂www.dytt89.com]', '')
                eles[1] = eles[1].replace('\n', '')
                self.resources.append(eles)

    def start(self):
        print('ui start')
        grid_item_layout = [
            [
                {'type':'space'},
                {'type':'label','name':'关键词','width':60},
                {'type':'edit','name':'keyword','width':0.35},
                {'type':'button','name':'搜索','width':60},
                {'type':'space'}
            ]
        ]
        controls = [{'type':'space'},
        [{'type':'list','name':'list1','itemheight':0.9,'itemwidth':300, 'itemlayout':grid_item_layout,'value':[{}],'marginSize':5}],
        {'type':'space'},
        ]
        
        result, controls = self.player.doModal('main', 800, 600, '看各种电影', controls)
        print(f'{result=},{controls=}')


    def onClick(self,page,control):
        print('onClick,{control=}')
            

    def onListItemClick(self, page, control, item):
        print(f'onListItemClick')


    def onListItemControlClick(self, page, listControl, item, itemControl):
        
        if itemControl == '搜索':
            room = self.player.getListItemControlValue('main','list1',item,'keyword')
            print(f'{room=}')
            self.getLiveUrl(room)

        if itemControl == 'movieName':
            url = self.search_ret[item]['magnet']
            print(f'{url=}')
            self.player.play(url)
         
    def stop(self):
        super().stop()
        print("pugin stop")
        
    def getLiveUrl(self,room):
        # if  web == '斗鱼' :
        #     url = douyu.get_real_url(room)
#        
        # if url != False and url != '':
            # self.player.play(url)
        self.search_ret = []
        for eles in self.resources:
            if eles[0].find(room) >= 0:
                self.search_ret.append({'movieName': eles[0], 'magnet': eles[1]})

        grid_item_layout = [[{'type':'link','name':'movieName','value': 'magnet','width':0.5,'clickable':True}]]
        controls = [{'type':'space','height':5},
        [{'type':'list','name':'list1','itemheight':0.9,'itemwidth':300, 'itemlayout':grid_item_layout,'value':self.search_ret,'marginSize':5}],
        {'type':'space','height':5},
        ]
        
        result, controls = self.player.doModal('main1', 600, 400, '看各种电影', controls)
           

def newPlugin(player:StellarPlayer.IStellarPlayer,*arg):
    plugin = uiplugin(player)
    return plugin

def destroyPlugin(plugin:StellarPlayer.IStellarPlayerPlugin):
    plugin.stop()

