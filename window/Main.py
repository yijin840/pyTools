#!/usr/bin/python
# -*- coding: UTF-8 -*-

from service.load.loadResource import get_value
from view.pyside6.windows import show

if __name__ == "__main__":
    title = get_value("yijin#view#title", "resources/application.yml")
    show(None)
