#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# takes TBM xml data and produces content.lua

import os
import sys
import xml.etree.cElementTree as cET
import xml.etree.ElementTree as ET

AC_FILE = "/root/Dropbox/Updates/content.lua"

# for testing
#AC_FILE = "/root/active-watchdog/content.lua"

class ActiveError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(value)
    

def write(xml_file):
    
    xml_parser = cET.XMLParser(encoding="utf-8")
    try:
        tree = ET.parse(xml_file, xml_parser)
    except Exception, e:
        raise ActiveError("Error reading xml file: %s" % e)
    

    root = tree.getroot()

    # sections are:
    # weather
    #    city
    #       day1
    #          day
    #          min
    #          max
    #          date
    #          gfx
    #          ldesc
    #       ...
      #       ...
      #       day6
      #     city
      #       .....
      # news
      #     business
      #        newsitem1
      #            headline
      #            abstract
      #            date
      #            source
      #            cid
      #        newsitem2
      #        ....

      #     world
      #        ....
      #     sport
      #        ....
      #     sportsresults
      #        ....
      #     local
      #        ....
      #     lotto

      # commodities
      #     gold
      #        value
      #        change



    try: 
        f = open(AC_FILE, "wb")
    except Exception, e:
        raise ActiveError("Unable to open content output file: %s" % e)
    
    f.write("\n\ncontent = {\n")


    weather = root.find("weather")
    f.write("  weather = {\n")

    for city in weather:
        name = city.find('fullname').text
        f.write ("    %s = {\n" % name.replace(" ", "_").lower())
        f.write ("      name = '%s',\n" % name)
        for info in city:
            if 'day' in info.tag:
                try:
                    day = info[0].text.lower()
                except AttributeError:
                    day = None
                f.write("      %s = {\n" % day)
                for el in info:
                    f.write("          %s = '%s',\n" % (el.tag, el.text))
                f.write("      },\n")
        f.write ("    },\n")

    f.write("  },\n")

    forex = root.find("forex")
    f.write("  forex = {\n")

    for cur in forex:
        f.write("    %s = {\n" % cur.tag)
        f.write("        name = '%s',\n" % cur.tag.upper())
        f.write("        val = '%s',\n" % cur.text)
        f.write("    },\n")

    f.write("  },\n")

    news = root.find("news")
    f.write("  news = {\n")

    newscat_names = {

        'business' : "Business News",
        'world' : "World News",
        'sport' : "Sports News",
        'sportsresults' : "Sports Results",
        'local' : "Local News",
        'lotto' : "Lotto Draw",
    }


    for cat in news:
        category = cat.tag
        # local is a lua keyword
        if category == "local":
            category = "localnews"

        f.write("    %s = {\n" % category)
        f.write("      name = '%s',\n" % newscat_names[cat.tag])
        for ni in cat:
            f.write("      %s = {\n" % ni.tag)
            for el in ni:
                try:
                    f.write('        %s = [[%s]],\n' % (el.tag, el.text.strip()))
                except AttributeError:
                    pass
            f.write("      },\n")
        f.write("    },\n")

    f.write("  },\n")

    commodities = root.find("commodities")
    f.write("  commodities = {\n")

    for c in commodities:
        f.write("    %s = {\n" % c.tag)
        f.write("        name = '%s',\n" % c.attrib['name'])
        for el in c:
            f.write("        %s = '%s',\n" % (el.tag, el.text))
        f.write("    },\n")


    f.write("  },\n")


    f.write("}\n\n")
    f.write("return content\n")
    f.close()

if __name__=='__main__':
    write(sys.argv[1])
