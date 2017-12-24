from lxml import etree
import requests
import sendMail
import recMail
import time
import datetime
import getContent
import WorkInTime
import threading
import logging
import imMail
import threading
import seller
import re

from multiprocessing import Process, Value


ljxp = seller.Seller('邻居小铺', 'https://weidian.com/?userid=1173561383')
ljxp.findAllItem()


