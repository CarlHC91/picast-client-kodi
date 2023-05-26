# -*- coding: utf-8 -*-

import sys
import xbmc
import xbmcgui
import xbmcplugin


class Kodi(object):

  def log(self, value):
    xbmc.log(value, xbmc.LOGINFO)


  def getParams(self):
    params = sys.argv[2]

    result = {}

    commands = params[params.find('?') + 1:]

    for command in commands.split('&'):
      if '=' in command:
        split = command.split('=')
        result[split[0]] = split[1]
      else:
        result[command] = ''

    return result


  def addFolder(self, label = '', url = '', art_labels = {}):
    listitem = xbmcgui.ListItem(label = label)
    listitem.setArt(art_labels)

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = listitem, isFolder = True)


  def addVideo(self, label = '', url = '', info_labels = {}, art_labels = {}, cast_labels = []):
    listitem = xbmcgui.ListItem(label = label)
    listitem.setInfo('video', info_labels)
    listitem.setArt(art_labels)
    listitem.setCast(cast_labels)

    listitem.setProperty('Video', 'true')
    listitem.setProperty('IsPlayable', 'true')

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = listitem, isFolder = False)


  def endFolder(self):
    xbmcplugin.endOfDirectory(handle = int(sys.argv[1]), succeeded = True)


  def playVideo(self, label = '', path = ''):
    listitem = xbmcgui.ListItem(label = label, path = path)

    listitem.setProperty('IsPlayable', 'true')

    xbmcplugin.setResolvedUrl(handle = int(sys.argv[1]), succeeded = True, listitem = listitem)

