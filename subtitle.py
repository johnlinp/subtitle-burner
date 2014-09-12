# -*- coding: utf-8 -*-

import sys
import cv
import cv2
import Image, ImageFont, ImageDraw
import numpy
import pysrt
import datetime

class Subtitle(object):
    def __init__(self):
        self._left = 90
        self._right = 90
        self._top = 30
        self._bottom = 50
        self._margin = -20
        self._border = 1
        self._font = ImageFont.truetype('DroidSansFallback.ttf', 120)

    def render(self, input_video_fname, input_subt_fname, output_video_fname):
        capture, writer = self._get_video_components(input_video_fname, output_video_fname)
        subts = pysrt.open(input_subt_fname)

        print 'total %s frames' % self._frame_count
        for idx in range(self._frame_count):
            ret, frame = capture.read()
            if not ret:
                break
            print '\rframe %d' % idx,
            sys.stdout.flush()
            frame = self._put_subt(idx, frame, subts)
            writer.write(frame)

            #if idx == 300:
            #    cv2.imwrite('haha.jpg', frame)
            #    break

    def _get_video_components(self, input_video_fname, output_video_fname):
        capture = cv2.VideoCapture(input_video_fname)

        self._fps = capture.get(cv.CV_CAP_PROP_FPS)
        self._frame_width = int(capture.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        self._frame_height = int(capture.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        self._frame_count = int(capture.get(cv.CV_CAP_PROP_FRAME_COUNT))

        size = (self._frame_width, self._frame_height)
        print size
        writer = cv2.VideoWriter(output_video_fname, cv.CV_FOURCC('M','J','P','G'), self._fps, size)
        assert writer.isOpened()

        return capture, writer

    def _put_line(self, frame, level, line, mode):
        image = Image.fromarray(frame)
        draw = ImageDraw.Draw(image)
        text_width, text_height = draw.textsize(line, font=self._font)
        if mode == 'top-left':
            text_x = self._left
            text_y = self._top + (text_height + self._margin) * level
        elif mode == 'bottom-left':
            text_x = self._left
            text_y = self._frame_height - self._bottom - (text_height + self._margin) * (level + 1)
        elif mode == 'bottom-right':
            text_x = self._frame_width - self._right - text_width
            text_y = self._frame_height - self._bottom - (text_height + self._margin) * (level + 1)
        elif mode == 'bottom-center':
            text_x = (self._frame_width - text_width) / 2
            text_y = self._frame_height - self._bottom - (text_height + self._margin) * (level + 1)
        for delta_x in range(-self._border, self._border + 1):
            for delta_y in range(-self._border, self._border + 1):
                draw.text((text_x + delta_x, text_y + delta_y), line, font=self._font, fill=(255, 255, 255))
        draw.text((text_x, text_y), line, font=self._font, fill=(255, 255, 255))
        return numpy.array(image)

    def _put_subt(self, idx, frame, subts):
        chosens = []
        seconds = float(idx) / self._fps
        now = datetime.datetime.combine(datetime.date.today(), datetime.time()) + datetime.timedelta(seconds=seconds)
        for subt in subts:
            start = datetime.datetime.combine(datetime.date.today(), subt.start.to_time())
            end = datetime.datetime.combine(datetime.date.today(), subt.end.to_time())
            if now >= start and now < end:
                chosens.extend(subt.text.split('\n'))
                if subt.index in [5, 6, 7, 23, 25, 34, 29]:
                    mode = 'bottom-left'
                elif subt.index in [22, 24]:
                    mode = 'bottom-right'
                else:
                    mode = 'top-left'
        if chosens and 'bottom' in mode:
            chosens.reverse()
        for level, line in enumerate(chosens):
            frame = self._put_line(frame, level, line, mode)
        return frame

