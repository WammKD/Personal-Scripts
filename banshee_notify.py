#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Original Author: Kaivalagi
# Created: 26/07/2009
#
# Modified by: Jesse Matties
# Modified on: 20/04/2011
# Modified version is severely cut down so as to increase speed.
# Sends info to notify-send to create a popup, showing currently playing
# song info and album art.
# depends on Banshee 2.* and lib-notify

from optparse import OptionParser
import os
import subprocess

try:
    import dbus
    DBUS_AVAIL = True
except ImportError:
    # Dummy D-Bus library
    class _Connection:
        get_object = lambda *a: object()
    class _Interface:
        __init__ = lambda *a: None
        ListNames = lambda *a: []
    class Dummy: pass
    dbus = Dummy()
    dbus.Interface = _Interface
    dbus.service = Dummy()
    dbus.service.method = lambda *a: lambda f: f
    dbus.service.Object = object
    dbus.SessionBus = _Connection
    DBUS_AVAIL = False


class CommandLineParser:

    parser = None

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-d", "--datatype", dest="datatype", default="TI", type="string", metavar="DATATYPE", help=u"[default: %default] The data type options are: ST (status), CA (coverart), TI (title), AL (album), AR (artist), GE (genre), YR (year), TN (track number), FN (file name), BR (bitrate k/s), LE (length), PP (current position in percent), PT (current position in time), VO (volume), RT (rating). Not applicable at command line when using templates.")
        self.parser.add_option("-c", "--coverartpath", dest="coverartpath", default="/tmp/cover", type="string", metavar="PATH", help=u"[default: %default] The file where coverart gets copied to if found when using the --datatype=CA option. Note that if set to an empty string i.e. \"\" the original file path is provided for the coverart path.")

    def parse_args(self):
        (options, args) = self.parser.parse_args()
        return (options, args)

class MusicData:
    def __init__(self,coverart,title,album,artist):
        self.coverart = coverart
        self.title = title
        self.album = album
        self.artist = artist
        
class BansheeInfo:
    
    error = u""
    musicData = None
    
    def __init__(self, options):
        self.options = options
        
    def testDBus(self, bus, interface):
        obj = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        dbus_iface = dbus.Interface(obj, 'org.freedesktop.DBus')
        avail = dbus_iface.ListNames()
        return interface in avail
        
    def getOutputData(self, datatype):
        output = u""
        
        try:
                
            bus = dbus.SessionBus()
            if self.musicData == None:
                
                if self.testDBus(bus, 'org.bansheeproject.Banshee'):
                    
                    try:
                        
                        # setup dbus hooks
                        remote_player = bus.get_object('org.bansheeproject.Banshee', '/org/bansheeproject/Banshee/PlayerEngine')
                        iface_player = dbus.Interface(remote_player, 'org.bansheeproject.Banshee.PlayerEngine')
                            
                        # grab the data into variables
                        location = iface_player.GetCurrentUri()

                        # try to get all the normal stuff...the props return an empty string if nothing is available

                        props = iface_player.GetCurrentTrack()

                        if "name" in props:
                            title = props["name"]
                        else:
                            title = None
                            
                        if "album" in props:
                            album = props["album"]
                        else:
                            album = None
                            
                        if "artist" in props:
                            artist = props["artist"]
                        else:
                            artist = None
                            
                        # TODO: get album art working for internet based (if feasible)...
                        # get coverart url or file link
                        if "artwork-id" in props:
                            if os.path.exists(os.path.expanduser("~/.cache/media-art/")):
                                path_prefix = os.path.expanduser("~/.cache/media-art/")
                            else:
                                path_prefix = os.path.expanduser("~/.cache/album-art/")
                            
                            coverart = os.path.join(path_prefix,str(props["artwork-id"]) +".jpg")
                            if coverart.find("http://") != -1:
                                coverart = None
                        else:
                            coverart = None
                            
                        self.musicData = MusicData(coverart,title,album,artist)
                        
                    except SystemExit:
                        return u""

            if self.musicData != None:
                
                if datatype == "CA": #coverart
                    if self.musicData.coverart == None or len(self.musicData.coverart) == 0:
                        output = None
                    else:
                        output = self.musicData.coverart
                            
                elif datatype == "TI": #title
                    if self.musicData.title == None or len(self.musicData.title) == 0:
                        output = None
                    else:
                        output = self.musicData.title
                        
                elif datatype == "AL": #album
                    if self.musicData.album == None or len(self.musicData.album) == 0:
                        output = None
                    else:
                        output = self.musicData.album
                        
                elif datatype == "AR": #artist
                    if self.musicData.artist == None or len(self.musicData.artist) == 0:
                        output = None
                    else:
                        output = self.musicData.artist
                        
                else:
                    return u""

            if output == None or self.musicData == None:
                if datatype == "CA":
                    output = ""                  
                else:
                    output = unknown_string
            
            return output
        
        except SystemExit:
            return ""

    def writeOutput(self):

        output = self.getOutputData(self.options.datatype)
    
    def makeNotification(self):
        artist = self.musicData.artist
        album = self.musicData.album
        title = self.musicData.title
        coverart = self.musicData.coverart
        subprocess.call(["notify-send", "--icon=%s" %coverart, "%s" %title, "<i>by</i> \'%s\'\n<i>from</i> \'%s\'" %(artist, album)])
        
def main():
    
    parser = CommandLineParser()
    (options, args) = parser.parse_args()

    bansheeinfo = BansheeInfo(options)
    bansheeinfo.writeOutput()
    bansheeinfo.makeNotification()
    
if __name__ == '__main__':
    main()
    
