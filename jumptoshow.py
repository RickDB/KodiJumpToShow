# -*- coding: utf-8 -*-
# Module: default
# Author: RickDB
# Created on: 15.03.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmc
from xbmc import LOGNOTICE
import resources.lib.util as util

DBID = xbmc.getInfoLabel('ListItem.DBID')
DBTYPE = xbmc.getInfoLabel('ListItem.DBTYPE')
TVShowTitle = xbmc.getInfoLabel('ListItem.TVShowTitle')

# if parameters are supplied override any values
try:
    params = util.parseParameters()

    if params.has_key('DBID'):
        DBID = action = params['DBID']
    if params.has_key('DBTYPE'):
        DBTYPE = action = params['DBTYPE']
    if params.has_key('TVShowTitle'):
        TVShowTitle = action = params['TVShowTitle']
except:
    print 'JumpToShow: Error during parameters readout'


# xbmc.log('DBTYPE = ' + DBTYPE, level=LOGNOTICE)
# xbmc.log('TVShowTitle = ' + TVShowTitle, level=LOGNOTICE)
# xbmc.log('DBID = ' + DBID, level=LOGNOTICE)

def getshowid(dbid, dbtype):
    import json
    tvshowID = 0

    if dbtype == 'season':
        query = xbmc.executeJSONRPC(
            '{ "jsonrpc": "2.0", "method": "VideoLibrary.GetSeasonDetails", "params": {"seasonid": %s, "properties": ["tvshowid"]}, "id": 1 }' % dbid)
        query = unicode(query, 'utf-8', errors='ignore')
        j = json.loads(query)

        if 'result' not in j:  # usually caused by the 'All Seasons' item
            dbid = str(int(dbid) + 2)  # this seems to give Season 1 which will suffice
            query = xbmc.executeJSONRPC(
                '{ "jsonrpc": "2.0", "method": "VideoLibrary.GetSeasonDetails", "params": {"seasonid": %s, "properties": ["tvshowid"]}, "id": 1 }' % dbid)
            query = unicode(query, 'utf-8', errors='ignore')
            j = json.loads(query)

        tvshowID = j['result']['seasondetails']['tvshowid']
    elif dbtype == 'episode':
        query = xbmc.executeJSONRPC(
            '{ "jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %s, "properties": ["tvshowid"]}, "id": 1 }' % dbid)
        query = unicode(query, 'utf-8', errors='ignore')
        j = json.loads(query)

        tvshowID = j['result']['episodedetails']['tvshowid']

    return tvshowID


if DBID > 0:
    # If not tv show we look up id
    if DBTYPE == 'season' or DBTYPE == 'episode':
        # xbmc.log('Looking up DBID...', level=LOGNOTICE)
        DBID = getshowid(DBID, DBTYPE)
        # xbmc.log('Got DBID: '+str(DBID), level=LOGNOTICE)

    if DBID > 0:
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin('ActivateWindow(Videos, videodb://tvshows/titles/' + str(DBID) + '/)')
