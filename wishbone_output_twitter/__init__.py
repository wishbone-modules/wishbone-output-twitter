#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2018 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from gevent import monkey; monkey.patch_all()
from wishbone.module import OutputModule
import twitter


class TwitterOut(OutputModule):
    '''
    Submit events to the Twitter API.


    Parameters::

        - consumer_key(str)("wishbone")
            |  Your Twitter user's consumer_key.

        - consumer_secret(str)("wishbone")
            |  Your Twitter user's consumer_secret.

        - access_token_key(str)("wishbone")
            |  The oAuth access token key value

          access_token_secret(str)("wishbone")
            |  The oAuth access token's secret

        - native_events(bool)(False)
           |  Submit Wishbone native events.

        - parallel_streams(int)(1)
           |  The number of outgoing parallel data streams.

        - payload(str)(None)
           |  The string to submit.
           |  If defined takes precedence over `selection`.

        - selection(str)("data")*
           |  The part of the event to submit externally.
           |  Use an empty string to refer to the complete event.

    Queues::

        - inbox
           |  Incoming messages

    '''

    def __init__(self, config,
                 selection="data", payload=None, native_events=False, parallel_streams=1,
                 consumer_key="wishbone", consumer_secret="wishbone", access_token_key="wishbone", access_token_secret="wishbone"):

        OutputModule.__init__(self, config)
        self.pool.createQueue("inbox")
        self.registerConsumer(self.consume, "inbox")

    def preHook(self):

        self.api = twitter.Api(
            consumer_key=self.kwargs.consumer_key,
            consumer_secret=self.kwargs.consumer_secret,
            access_token_key=self.kwargs.access_token_key,
            access_token_secret=self.kwargs.access_token_secret,
            tweet_mode="extended"
        )

    def consume(self, event):

        data = self.getDataToSubmit(event)
        data = self.encode(data)
        try:
            result = self.api.PostUpdate(data)
        except twitter.error.TwitterError as err:
            raise Exception("Failed to send tweet. Reason: Error %s. %s" % (err.message[0]["code"], err.message[0]["message"]))
        else:
            self.logging.debug("Event %s submitted successfully to Twitter. Returned ID is %s." % (event.get('uuid'), result.id))
