#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import logging.handlers
import os
import os.path
import sys
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn


class MyHttpHandler(BaseHTTPRequestHandler):
    """
    basic http handler
    """
    def do_GET(self):
        try:
            if not self.__parse_get_req():
                logging.warning("parse get request failed")
            if self.static:
                self.__handle_static()
            else:
                self.__do_get(self.get)
        except Exception as e:
            logging.warning("handle get request error: %s" % str(e))
            self.__send_response("service error")

    def do_POST(self):
        try:
            if not self.__parse_post_req():
                logging.warning("parse post request failed")
            self.__do_post(self.post)
        except Exception as e:
            logging.warning("handle post request error: %s" % str(e))
            self.__send_response("service error")

    def __send_response(self, data):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def __parse_get_req(self):
        # deal get params
        self.get = {}
        self.static = False
        ul = self.path.split('?')
        if len(ul) < 2:
            logging.info("no get params")
            paths = ul[0].split('/')
            if paths[1] == 'static':
                self.static = True
                self.static_path = ul[0].strip('/')
        else:
            pl = ul[1].split('&')
            if len(pl) < 2:
                logging.info("no get params")
            else:
                for p in pl:
                    kv = p.strip().split('=')
                    self.get[kv[0]] = kv[1]
        return True

    def __parse_post_req(self):
        self.post = ""
        if "Content-Length" not in self.headers:
            logging.warning("post Request error: missing Content-Length")
            return False
        length = self.headers['Content-Length']
        # deal post parsms
        self.post = self.rfile.read(int(length))
        return True

    def __handle_static(self):
        if not os.path.exists(self.static_path):
            logging.warning("no such file: %s" % self.static_path)
            self.__send_response("not found")
        else:
            with open (self.static_path) as f:
                data = f.read()
            self.__send_response(data)

    def __do_get(self, get):
        # todo
        rep = json.dumps(get)
        self.__send_response(rep)

    def __do_post(self, post):
        # todo
        rep = post
        self.__send_response(rep)


class ThreadHttpServer(ThreadingMixIn, HTTPServer):
    pass


def init_log():
    logging.basicConfig(
        filename = "run.log",
        format = "[%(asctime)s][%(levelname)s][%(funcName)s][line:%(lineno)d]:%(message)s",
        level = logging.DEBUG,
        filemode = "a" 
    )


def run_server(port):
    s = ThreadHttpServer(('',port), MyHttpHandler)
    init_log()
    s.serve_forever()


