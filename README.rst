::
              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|


    ======================================
    wishbone_contrib.module.output.twitter
    ======================================

    Version: 1.0.0

    Submit events to the Twitter API.
    ---------------------------------

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


