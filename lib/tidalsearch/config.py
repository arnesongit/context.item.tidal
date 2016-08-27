# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Arne Svenson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import os, platform
import xbmc, xbmcaddon

#------------------------------------------------------------------------------
# Global Definitions
#------------------------------------------------------------------------------

USER_AGENTS = {
    "Windows IE": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Windows Firefox": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "MacOS Firefox": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0",
    "MacOS Chrome": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "MacOS Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
    "iPad": "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
    "iPhone": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
    "Mobile": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
               }

# Constants from appTidal.js
class CONST(object):
    addon_name = "TIDAL Search"
    addon_id = "context.item.tidal.search"

    youtube_addon_id = 'plugin.video.youtube'
    
    artistImageURL = "http://images.tidalhifi.com/im/im?w={width}&h={height}&artistid={artistid}"
    userPlaylistFanartUrl =  "http://images.tidalhifi.com/im/im?w={width}&h={height}&uuid={uuid}&cols={cols}&rows={rows}&artimg&dummy={dummy}"
    videoImageURL = "http://images.tidalhifi.com/im/im?w={width}&h={height}&img={imagepath}"
    profilePictureUrl = "http://resources.tidal.com/images/{picture}/{size}.jpg"
    artistFallbackImageId = "1e01cdb6-f15d-4d8b-8440-a047976c1cac"
    albumFallbackImageId = "0dfd3368-3aa1-49a3-935f-10ffb39803c0"
    playlistFallbackImageId = "443331e2-0421-490c-8918-5a4867949589"
    videoFallbackImageId = "fa6f0650-76ac-41d1-a4a3-7fe4c89fca90"
    editorialCategories = ("topalbums", "newtracks", "newalbums",
                            "recommendedalbums", "recommendedtracks", "recommendedplaylists",
                            "newplaylists", "toptracks")
    artistIdVariousArtists = "2935"

    videoQuality = {'DEFAULT': (1920, 1080),
                    'MP4_1080P': (1920, 1080),
                    'MP4_720P': (1280, 720),
                    'MP4_540P': (960, 540),
                    'MP4_480P': (854, 480),
                    'MP4_360P': (640, 360),
                    'MP4_240P': (426, 240) }

    searchTypes = ['ARTISTS', 'ALBUMS', 'PLAYLISTS', 'TRACKS', 'VIDEOS']

    apiLocation = "https://api.tidal.com/v1/"

    apiToken = [ "wdgaB1CilGA-S_s2",  # Browser
                 "P5Xbeo5LFvESeDy6" ]  # Android

    metaCacheFile = 'metaCache.db'  # SQlite DB for cach data

# Image Sizes for Thumbnails/Covers/Fanart
class ImgSize(object):
    album = ("80x80", "160x160", "320x320", "640x640", "1280x1280")
    artist = ("160x160", "320x320", "160x107", "320x214", "640x428", "1024x256", "1080x720")
    playlist = ("160x107", "320x214", "1080x720")
    genre = ("460x306", "2048x512")
    mood = ("342x342", "2048x330")
    promo = ("550x400", "1280x720")
    featuredPromo = ("1280x400", "1650x400", "2200x400", "2750x400")
    video = ("160x107", "320x214")

class MusicQuality(object):
    lossless_hd = 'LOSSLESS_HD'
    lossless = 'LOSSLESS'
    high = 'HIGH'
    low = 'LOW'

class VideoQuality(object):
    _max = 9999     # Select highest Quality
    _1080p = 1080
    _720p = 720
    _540p = 540
    _480p = 480
    _360p = 360
    _240p = 240
    _novid = 721  # Select 720p stream to play audio only 

#------------------------------------------------------------------------------
# Configuration Class
#------------------------------------------------------------------------------

class Config(object):

    def __init__(self, addon):
        self.reload(addon)
        
    def reload(self, addon):
        # Addon Info
        self.addon_id = addon.getAddonInfo('id')
        self.addon_name = addon.getAddonInfo('name')
        self.addon_path = addon.getAddonInfo('path').decode('utf-8')
        self.addon_base_url = 'plugin://' + self.addon_id
        self.addon_fanart = os.path.join(self.addon_path, 'fanart.jpg').decode('utf-8')
        self.addon_icon = os.path.join(self.addon_path, 'icon.png').decode('utf-8')

        # Hidden Settings
        '''
        self._user_id = addon.getSetting('user_id')
        self._session_id = addon.getSetting('session_id')
        self._playlist_session_id = addon.getSetting('playlist_session_id')
        self._session_country = addon.getSetting('country_code')
        self._session_token = addon.getSetting('session_token')
        # Session Settings
        self.homeDir = addon.getAddonInfo('path').decode('utf-8')
        self.username = addon.getSetting('username')
        self.password = addon.getSetting('password')
        self.subscription_type = [MusicQuality.lossless, MusicQuality.high, MusicQuality.low][int('0%s' % addon.getSetting('subscription_type'))]
        self.login_token = int('0%s' % addon.getSetting('login_token'))
        self.country = addon.getSetting('country')
        '''
        self.debug = True if addon.getSetting('debug') == 'true' else False
        self.debug_server = addon.getSetting('debug_server')
        self.log_details = int('0%s' % addon.getSetting('log_details'))
        # Global
        '''
        self.showFanart = True if addon.getSetting('show_fanart') == 'true' else False
        self.folderColor = addon.getSetting('folder_color')
        self.favoriteColor = addon.getSetting('favorite_color')
        self.userPlaylistColor = addon.getSetting('user_playlist_color')
        self.notPlayableColor = addon.getSetting('not_playable_color')
        self.cacheFavorites = True if addon.getSetting('cache_favorites') == 'true' else False
        self.cachePlaylists = True if addon.getSetting('cache_playlists') == 'true' else False
        self.cacheAlbums = True if addon.getSetting('cache_albums') == 'true' else False
        self.max_http_requests = int('0%s' % addon.getSetting('max_http_requests'))
        self.cacheDir = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
        self.showNotifications = False if addon.getSetting('no_notifications') == 'true' else True
        self.confirmFavoriteActions = False if addon.getSetting('no_favorite_confirm') == 'true' else True
        self.default_trackplaylist = addon.getSetting('default_trackplaylist').decode('utf-8')
        self.default_trackplaylist_id = addon.getSetting('default_trackplaylist_id').decode('utf-8')
        self.default_videoplaylist = addon.getSetting('default_videoplaylist').decode('utf-8')
        self.default_videoplaylist_id = addon.getSetting('default_videoplaylist_id').decode('utf-8')
        # Music Settings
        self.musicQuality = [MusicQuality.lossless, MusicQuality.high, MusicQuality.low, MusicQuality.lossless_hd][int('0%s' % addon.getSetting('music_quality'))]
        self.showAlbumType = True if addon.getSetting('show_album_type') == 'true' else False
        self.explicitMask = addon.getSetting('explicit_mask').decode('utf-8')
        # Video Settings
        self.maxVideoHeight = [VideoQuality._max, VideoQuality._1080p, VideoQuality._720p, VideoQuality._540p, VideoQuality._480p, VideoQuality._360p, VideoQuality._240p][int('0%s' % addon.getSetting('video_quality'))]
        self.maxVideoHeightSlowServers = [VideoQuality._max, VideoQuality._1080p, VideoQuality._720p, VideoQuality._540p, VideoQuality._480p, VideoQuality._360p, VideoQuality._240p][int('0%s' % addon.getSetting('slow_video_quality'))]
        self.slowServers = addon.getSetting('slow_servers').split(' ')
        '''
        # Search Tuning Settings
        self.fuzzy_artist_level = float('0%s' % addon.getSetting('fuzzy_artist_level'))
        self.fuzzy_title_level = float('0%s' % addon.getSetting('fuzzy_title_level'))
        self.fuzzy_album_level = float('0%s' % addon.getSetting('fuzzy_album_level'))
        self.fuzzy_album_artist_level = float('0%s' % addon.getSetting('fuzzy_album_artist_level'))
        self.fuzzy_album_year_level = float('0%s' % addon.getSetting('fuzzy_album_year_level'))
        self.search_blacklist1 = addon.getSetting('search_blacklist1').split()
        self.search_blacklist2 = addon.getSetting('search_blacklist2').split()
        self.search_blacklist3 = addon.getSetting('search_blacklist3').split()
        self.search_blacklist1_percent = float('0%s' % addon.getSetting('search_blacklist1_percent'))
        self.search_blacklist2_percent = float('0%s' % addon.getSetting('search_blacklist2_percent'))
        self.search_blacklist3_percent = float('0%s' % addon.getSetting('search_blacklist3_percent'))
        self.search_artist_diff_level = float('0%s' % addon.getSetting('search_artist_diff_level'))
        # other Settings
        # Other Settings
        try:
            self.kodiVersion = '16'
            self.kodiVersion = xbmc.getInfoLabel('System.BuildVersion').split()[0]
            self.kodiVersion = self.kodiVersion.split('.')[0]
        except:
            pass
        self.skinTheme = xbmc.getSkinDir()
        self.platform = platform.platform().lower()
        self.os = 'MacOS' if 'darwin' in self.platform \
            else 'Windows' if 'windows' in self.platform \
            else 'Android' if 'android' in self.platform \
            else 'OpenELEC' if 'openelec' in self.platform \
            else 'LibreELEC' if 'libreelec' in self.platform \
            else 'Linux' if 'linux' in self.platform \
            else 'Unknown'
        #self.showExtrasContext = True if xbmcaddon.Addon('context.item.my_extras').getAddonInfo('id') else False
        
#------------------------------------------------------------------------------
# Configuration
#------------------------------------------------------------------------------

addon = xbmcaddon.Addon(CONST.addon_id)
settings = Config(addon) 

def reloadConfig():
    settings.reload(addon)
    return settings

def getSetting(setting):
    return addon.getSetting(setting)

def setSetting(setting, value):
    addon.setSetting(setting, value)
            
# End of File