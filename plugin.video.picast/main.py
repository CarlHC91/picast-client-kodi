# -*- coding: utf-8 -*-

import sys
import requests
import xbmcaddon

from lib import kodi


kod = kodi.Kodi()

addon = xbmcaddon.Addon()
server_host = addon.getSetting('server_host')


def run():
  params = kod.getParams()

  if params.get('action') is None:
    params['action'] = 'list_directory'
    params['id_directory'] = '0'

  if params.get('action') == 'play_archive':
    play_archive(params)

  if params.get('action') == 'list_directory':
    list_directory(params)

  kod.endFolder()


def list_directory(params):
  url = server_host + '/directoryDetails/findAllByParent'

  request_details = {
    'parent_directory': {
      'id_directory':  params.get('id_directory')
    }
  }

  try:
    response_details = requests.post(url, json = request_details).json()

    for directory_details in response_details['directory_details_list']:
      id_directory = directory_details['id_directory']
      label = directory_details['file_name']
      url = '%s?action=list_directory&id_directory=%s&label=%s' % (sys.argv[0], str(id_directory), str(label))

      kod.addFolder(label = label, url = url)

  except Exception as e:
    kod.log(str(e))

  url = server_host + '/archiveDetails/findAllByParent'

  request_details = {
    'parent_directory': {
      'id_directory':  params.get('id_directory')
    }
  }

  try:
    response_details = requests.post(url, json = request_details).json()

    for archive_details in response_details['archive_details_list']:
      id_archive = archive_details['id_archive']
      label = archive_details['file_name']
      url = '%s?action=play_archive&id_archive=%s&label=%s' % (sys.argv[0], str(id_archive), str(label))

      kod.addVideo(label = label, url = url)
  except Exception as e:
    kod.log(str(e))


def play_archive(params):
  label = params.get('label')
  path = server_host + '/archiveDetails/downloadOneById?id_archive=' + params.get('id_archive')

  kod.playVideo(label = label, path = path)


run()

