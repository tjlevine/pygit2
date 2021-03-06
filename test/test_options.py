# -*- coding: UTF-8 -*-
#
# Copyright 2010-2017 The pygit2 contributors
#
# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2,
# as published by the Free Software Foundation.
#
# In addition to the permissions in the GNU General Public License,
# the authors give you unlimited permission to link the compiled
# version of this file into combinations with other programs,
# and to distribute those combinations without any restriction
# coming from the use of this file.  (The General Public License
# restrictions do apply in other respects; for example, they cover
# modification of the file, and distribution when not linked into
# a combined executable.)
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.

"""Tests for Blame objects."""

from __future__ import absolute_import
from __future__ import unicode_literals
import unittest
import pygit2
from pygit2 import (
    GIT_OBJ_BLOB,
    GIT_OPT_GET_MWINDOW_SIZE, GIT_OPT_SET_MWINDOW_SIZE,
    GIT_OPT_GET_SEARCH_PATH, GIT_OPT_SET_SEARCH_PATH,
    GIT_OPT_GET_MWINDOW_MAPPED_LIMIT, GIT_OPT_SET_MWINDOW_MAPPED_LIMIT,
    GIT_CONFIG_LEVEL_SYSTEM, GIT_CONFIG_LEVEL_XDG, GIT_CONFIG_LEVEL_GLOBAL,
    GIT_OPT_SET_CACHE_OBJECT_LIMIT,
    GIT_OPT_GET_CACHED_MEMORY,
    GIT_OPT_ENABLE_CACHING,
)
from pygit2 import option
from . import utils

class OptionsTest(utils.NoRepoTestCase):

    def __option(self, getter, setter, value):
        old_value = option(getter)
        option(setter, value)
        self.assertEqual(value, option(getter))
        # Reset to avoid side effects in later tests
        option(setter, old_value)

    def __proxy(self, name, value):
        old_value = getattr(pygit2.settings, name)
        setattr(pygit2.settings, name, value)
        self.assertEqual(value, getattr(pygit2.settings, name))
        # Reset to avoid side effects in later tests
        setattr(pygit2.settings, name, old_value)

    def test_mwindow_size(self):
        self.__option(
            GIT_OPT_GET_MWINDOW_SIZE,
            GIT_OPT_SET_MWINDOW_SIZE,
            200 * 1024)

    def test_mwindow_size_proxy(self):
        self.__proxy('mwindow_size', 300 * 1024)

    def test_mwindow_mapped_limit_200(self):
        self.__option(
            GIT_OPT_GET_MWINDOW_MAPPED_LIMIT,
            GIT_OPT_SET_MWINDOW_MAPPED_LIMIT,
            200 * 1024)

    def test_mwindow_mapped_limit_300(self):
        self.__proxy('mwindow_mapped_limit', 300 * 1024)

    def test_cache_object_limit(self):
        new_limit = 2 * 1024
        option(GIT_OPT_SET_CACHE_OBJECT_LIMIT, GIT_OBJ_BLOB, new_limit)

    def test_cache_object_limit_proxy(self):
        new_limit = 4 * 1024
        pygit2.settings.cache_object_limit(GIT_OBJ_BLOB, new_limit)

    def test_cached_memory(self):
        value = option(GIT_OPT_GET_CACHED_MEMORY)
        self.assertEqual(value[1], 256 * 1024**2)

    def test_cached_memory_proxy(self):
        self.assertEqual(pygit2.settings.cached_memory[1], 256 * 1024**2)

    def test_enable_cache(self):
        option(GIT_OPT_ENABLE_CACHING, False)
        option(GIT_OPT_ENABLE_CACHING, True)

    def test_enable_cache_proxy(self):
        pygit2.settings.enable_caching(False)
        pygit2.settings.enable_caching(True)

    def test_cache_max_size_proxy(self):
        pygit2.settings.cache_max_size(128 * 1024**2)
        self.assertEqual(pygit2.settings.cached_memory[1], 128 * 1024**2)
        pygit2.settings.cache_max_size(256 * 1024**2)
        self.assertEqual(pygit2.settings.cached_memory[1], 256 * 1024**2)

    def test_search_path(self):
        paths = [(GIT_CONFIG_LEVEL_GLOBAL, '/tmp/global'),
                 (GIT_CONFIG_LEVEL_XDG,    '/tmp/xdg'),
                 (GIT_CONFIG_LEVEL_SYSTEM, '/tmp/etc')]

        for level, path in paths:
            option(GIT_OPT_SET_SEARCH_PATH, level, path)
            self.assertEqual(path, option(GIT_OPT_GET_SEARCH_PATH, level))

    def test_search_path_proxy(self):
        paths = [(GIT_CONFIG_LEVEL_GLOBAL, '/tmp2/global'),
                 (GIT_CONFIG_LEVEL_XDG,    '/tmp2/xdg'),
                 (GIT_CONFIG_LEVEL_SYSTEM, '/tmp2/etc')]

        for level, path in paths:
            pygit2.settings.search_path[level] = path
            self.assertEqual(path, pygit2.settings.search_path[level])

if __name__ == '__main__':
    unittest.main()
