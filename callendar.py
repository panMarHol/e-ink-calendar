#!/bin/python3

from PIL import Image, ImageDraw, ImageFont
from lib import epd7in3g
import requests
import zipfile
import time
import io

font_url = "https://dl.dafont.com/dl/?f=gunny_rewritten"

def callendar_skelet(draw_skelet, headline, headline_font, date_font, hour_font, day_segment):
    x1_skelet = (epd.width / 100)  * 1
    y1_skelet = (epd.height / 100) * 10
    x2_sekelt = epd.width  - x1_skelet
    y2_skelet = epd.height - x1_skelet

    # OUTER BOX and HEADLINE TEXT
    draw_skelet.rounded_rectangle([(x1_skelet, y1_skelet), (x2_sekelt, y2_skelet)], radius=5 , outline=epd.BLACK, width=5, corners=(True, True, True, True))
    draw_skelet.text((epd.width / 2,  y1_skelet / 2), headline, fill=epd.BLACK, font=headline_font, anchor="mm")

    # Get last Monday
    now = time.time()
    monday = time.localtime(now)
    days_to_monday = monday.tm_wday
    while (days_to_monday > 0):
        now = now - (60 * 60 * 24)
        days_to_monday -= 1

    # BODY
    for day in range(7):

        HEADER_SIZE = 28
        COLLUM_WIDTH = ((x2_sekelt - x1_skelet) / 7 )
        GAP = (COLLUM_WIDTH / 100) * 8

        # HEAD
        x1_header = x1_skelet + (day * COLLUM_WIDTH) + GAP
        y1_header = y1_skelet + GAP
        x2_header = x1_header + COLLUM_WIDTH - (GAP * 2)
        y2_header = y1_header + HEADER_SIZE
        draw_skelet.rounded_rectangle([(x1_header, y1_header), (x2_header, y2_header)], radius=3, outline=epd.BLACK, width=3, corners=(True, True, False, False))

        # DATE TEXT
        date = time.localtime(now + (day * 60 * 60 * 24))
        switch = {
            0: ["Po", epd.BLACK],
            1: ["Út", epd.BLACK],
            2: ["St", epd.BLACK],
            3: ["Čt", epd.BLACK],
            4: ["Pá", epd.BLACK],
            5: ["So", epd.RED],
            6: ["Ne", epd.RED]
        }
        date_print = f"{switch.get(date.tm_wday)[0]} {date.tm_mday}.{date.tm_mon}.{date.tm_year}"
        draw_skelet.text((x1_header + 4, y2_header), date_print, font=date_font, fill=switch.get(date.tm_wday)[1], anchor="ld")

        # DAY
        x1_body = x1_header
        y1_body = y2_header + (GAP / 2)
        x2_body = x1_body + COLLUM_WIDTH - (GAP * 2)
        y2_body = y2_skelet - GAP
        draw_skelet.rounded_rectangle([(x1_body, y1_body), (x2_body, y2_body)], radius=2, outline=epd.BLACK, width=3, corners=(False, False, True, True))

        # HOURS
        HOUR_GAP = (y2_body - y1_body) / day_segment
        for hour in range(day_segment):
            x1_hour = x1_body
            y1_hour = y1_body + (hour * HOUR_GAP)
            x2_hour = x2_body
            y2_hour = y1_hour
            draw.line([(x1_hour, y1_hour), (x2_hour, y2_hour)], fill=epd.BLACK, width=1)
            hour_print = f"{time.localtime(((hour * 60 * 60) * (24 / day_segment)) - (60 * 60)).tm_hour}:00"
            draw.text((x1_hour + (GAP / 2), y1_hour + (GAP / 2)), hour_print, font=hour_font, fill=epd.BLACK, anchor="lt")

        # WEEKEND
        x1_weekend = x1_skelet + (5 * COLLUM_WIDTH)
        y1_weekend = y1_skelet
        x2_weekend = x2_sekelt
        y2_weekend = y2_skelet
        draw_skelet.rounded_rectangle([(x1_weekend, y1_weekend), (x2_weekend, y2_weekend)], radius=7, outline=epd.BLACK, width=4, corners=(True, True, True, True))

    return draw_skelet

def get_font(url):
    header = {
        "Accept": "zip-file"
    }
    response = requests.get(url=url, headers=header, stream=True)
    if response.ok:
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        font = zip_file.open('gnyrwn971.ttf')

    return font

epd = epd7in3g.EPD()
ImageFont.load_default()
font10 = ImageFont.truetype(font=get_font(font_url), size=10)
font18 = ImageFont.truetype(font=get_font(font_url), size=18)
font30 = ImageFont.truetype(font=get_font(font_url), size=30)
font50 = ImageFont.truetype(font=get_font(font_url), size=50)

full_frame = (epd.width, epd.height)

image = Image.new("RGB", full_frame, epd.WHITE)
draw = ImageDraw.Draw(image)
callendar_skelet(draw, "Miluji tě", font50, font18, font10, 12)

epd.init()
epd.Clear()
epd.display(epd.getbuffer(image))
epd.sleep()
