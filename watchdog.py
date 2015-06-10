#!/usr/bin/env python

import pyinotify
import active
import syslog

XML_TO_WATCH="/root/Dropbox/Updates/TBMFlashInfo.xml"

# for testing purposes
#XML_TO_WATCH="/root/active-watchdog/TBMFlashInfo.xml"

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CLOSE_WRITE(self, event):
        print "%s was changed" % event.pathname
        try:
            active.write(XML_TO_WATCH)
        except active.ActiveError, e:
            syslog.syslog("Error processing xml: %s" % e)

        
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(XML_TO_WATCH, mask, rec=False)

notifier.loop()
