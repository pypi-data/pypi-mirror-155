# -*- coding: utf-8 -*-
import datetime

from thumbor.config import Config
from thumbor.handlers import ContextHandler
from thumbor.utils import logger
from os.path import exists

Config.define(
    "ICON_IMAGE_LOCAL_PATH",
    "",
    "specify your favicon.ico file path.",
    "icon handler",
)


class IconHandler(ContextHandler):
    async def get(self):
        res = await self.readIconBuffer()
        if res is not None:
            self.set_status(200)
            self.set_header("Content-Type", 'image/x-icon')

            max_age = self.context.config.MAX_AGE
            if max_age:
                self.set_header("Cache-Control", "max-age=" + str(max_age) + ",public")
                self.set_header("Expires", datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age))
            self.write(res)
            await self.finish()
        else:
            self._error(404, "[thumbor-icon-handler] do not found icon file in local filesystem or loader")

    async def readIconBuffer(self):
        """
        read favicon.ico file buffer from local at first, then fallback try loader
        if ICON_IMAGE_LOCAL_PATH is EMPTY, fallback using favicon.ico
        if ICON_IMAGE_LOCAL_PATH is NOT EMPTY, try it as local path at first, then fallback as loader path
        """
        path = self.context.config.ICON_IMAGE_LOCAL_PATH.strip()
        if path == '':
            logger.info(f'[thumbor-icon-handler] ICON_IMAGE_LOCAL_PATH missing or invalid, fallback using favicon.ico')
            path = 'favicon.ico'

        """ find local filesystem file at first """
        if exists(path):
            with open(path, "rb") as source_file:
                logger.debug(f"[thumbor-icon-handler] local filesystem found icon file:{path}")
                return source_file.read()

        """ try loader """
        loader_res = await self.context.modules.loader.load(self.context, path)
        if loader_res is None:
            logger.debug(f"[thumbor-icon-handler] loader do not found icon file:{path}")
            return None
        else:
            logger.debug(f"[thumbor-icon-handler] loader found icon file:{path}")
            return loader_res.buffer
