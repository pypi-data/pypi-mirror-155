#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  m3u8dl.py
@Date    :  2022/06/20
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
from tkinter import E
import aigpy
import requests

from urllib.request import urlopen


class M3u8Downloader(object):
    def __init__(self, url, path, threadNum: int = 1) -> None:
        self._url = url
        self._path = path
        self._threadNum = threadNum

    def __getTsUrls__(self):
        content = requests.get(self._url).content
        if content is None:
            raise Exception("get m3u8 content failed.")

        urls = aigpy.m3u8.parseTsUrls(content)
        if len(urls) <= 0:
            raise Exception("get ts urls failed.")

        return urls

    def __getTmpDir__(self):
        dir = aigpy.path.getDirName(self._path)
        name = aigpy.path.getFileNameWithoutExtension(self._path)
        return f"{dir}/{name}"

    def __getTmpPartPath__(self, index):
        dir = self.__getTmpDir__()
        return f"{dir}/{str(index)}"
    
    def __combineFile__(self, urls):
        with open(self._path, 'wb') as f:
            for index, urls in enumerate(urls):
                itemPath = self.__getTmpPartPath__(index)
                itemText = aigpy.file.getContent(itemPath, True)
                f.write(itemText)

    @staticmethod
    def __download_thread__(url, path, progress):
        error = None
        for index in range(0, 3):
            try:
                response = urlopen(url)
                totalSize = response.length

                curcount = 0
                chunksize = 16 * 1024
                with open(path, 'wb') as f:
                    while True:
                        chunk = response.read(chunksize)
                        f.write(chunk)

                        curcount += len(chunk)
                        if curcount >= totalSize:
                            break
            except Exception as e:
                error = e 
                continue

            if progress:
                progress.step()

            return True, ""
        return False, error

    def start(self, showProgress: bool = True):
        tmpDir = self.__getTmpDir__()
        if aigpy.path.mkdirs(tmpDir) is False:
            raise Exception("create tmp dir failed.")
            
        try:
            tsUrls = self.__getTsUrls__()
            progress = None
            if showProgress:
                progress = aigpy.progress.ProgressTool(len(tsUrls), 15)
            
            threads = aigpy.thread.ThreadTool(self._threadNum)
            for index, itemUrl in enumerate(tsUrls):
                itemPath = self.__getTmpPartPath__(index)
                threads.start(self.__download_thread__, itemUrl, itemPath, progress)

            results = threads.waitAll()
            threads.close()

            for item in results:
                if item[0] is False:
                    raise Exception("Some parts download failed.")
            
            self.__combineFile__(tsUrls)
            aigpy.path.remove(tmpDir)
        except Exception as e:
            aigpy.path.remove(tmpDir)
            raise e
