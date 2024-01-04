#!/bin/python3

# from lib import epd7in3g
from PIL import Image, ImageDraw, ImageFont
import time

class callendar():
    def __init__(self, width:int, height:int, font_url:str):
        self.setResolution(width, height)
        self.setFont(font_url)
        
    def setResolution(self, width, height):
        self.width  = width
        self.height = height

    def setFont(self, font_url):
        self.font10 = ImageFont.truetype(font=self.download_font(font_url), size=10)
        self.font18 = ImageFont.truetype(font=self.download_font(font_url), size=18)
        self.font50 = ImageFont.truetype(font=self.download_font(font_url), size=50)

    def download_font(url):
        from zipfile import ZipFile
        import requests
        import io
        header = {
            "Accept": "zip-file" 
        }
        response = requests.get(url=url, headers=header, stream=True)
        if response.ok:
            zip_file = ZipFile(io.BytesIO(response.content))
            for file in zip_file.infolist():
                if file.filename.lower().endswith('.ttf'):
                    font = zip_file.open(file.filename)
        
        return font

    def draw_callendar_skelet(self, headline:str, day_segment:int):
        image = Image.new("RGB", (self.width, self.height), "white")
        draw  = ImageDraw.Draw(image)

        x1_skelet = (self.width / 100)  * 1
        y1_skelet = (self.height / 100) * 10
        x2_sekelt = self.width  - x1_skelet
        y2_skelet = self.height - x1_skelet

        # OUTER BOX and HEADLINE TEXT
        draw.rounded_rectangle([(x1_skelet, y1_skelet), (x2_sekelt, y2_skelet)], radius=5 , outline="black", width=5, corners=(True, True, True, True))
        draw.text((self.width / 2,  y1_skelet / 2), headline, fill="black", font=self.font50, anchor="mm")

        # GET last Monday
        now            = time.time()
        monday         = time.localtime(now)
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
            draw.rounded_rectangle([(x1_header, y1_header), (x2_header, y2_header)], radius=3, outline="black", width=3, corners=(True, True, False, False))

            # DATE TEXT
            date = time.localtime(now + (day * 60 * 60 * 24))
            switch = {
                0: ["Po", "black"],
                1: ["Út", "black"],
                2: ["St", "black"],
                3: ["Čt", "black"],
                4: ["Pá", "black"],
                5: ["So", "red"],
                6: ["Ne", "red"]
            }
            date_print = f"{switch.get(date.tm_wday)[0]} {date.tm_mday}.{date.tm_mon}.{date.tm_year}"
            draw.text((x1_header + 4, y2_header), date_print, font=self.font18, fill=switch.get(date.tm_wday)[1], anchor="ld")

            # DAY
            x1_body = x1_header
            y1_body = y2_header + (GAP / 2)
            x2_body = x1_body + COLLUM_WIDTH - (GAP * 2)
            y2_body = y2_skelet - GAP
            draw.rounded_rectangle([(x1_body, y1_body), (x2_body, y2_body)], radius=2, outline="black", width=3, corners=(False, False, True, True))

            # HOURS
            HOUR_GAP = (y2_body - y1_body) / day_segment
            for hour in range(day_segment):
                x1_hour = x1_body
                y1_hour = y1_body + (hour * HOUR_GAP)
                x2_hour = x2_body
                y2_hour = y1_hour
                draw.line([(x1_hour, y1_hour), (x2_hour, y2_hour)], fill="black", width=1)
                hour_print = f"{time.localtime(((hour * 60 * 60) * (24 / day_segment)) - (60 * 60)).tm_hour}:00"
                draw.text((x1_hour + (GAP / 2), y1_hour + (GAP / 2)), hour_print, font=self.font10, fill="black", anchor="lt")

            # WEEKEND
            x1_weekend = x1_skelet + (5 * COLLUM_WIDTH)
            y1_weekend = y1_skelet
            x2_weekend = x2_sekelt
            y2_weekend = y2_skelet
            draw.rounded_rectangle([(x1_weekend, y1_weekend), (x2_weekend, y2_weekend)], radius=7, outline="black", width=4, corners=(True, True, True, True))

        return image

cal = callendar(width=800, height=480, font_url="https://www.ceskefonty.cz/ceske-fonty-zdarma-ke-stazeni/43/scrgunny.zip")
background = cal.draw_callendar_skelet("test", 12)
background.show()

# epd.init()
# epd.Clear()
# epd.display(epd.getbuffer(image))
# epd.sleep()
