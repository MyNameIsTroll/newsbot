# NewsBot
A robot that publishes the content of RSS feeds on a Mastodon account.


## Installation
1. Go to your Mastodon account in ``settings/development``.
   ![image](https://github.com/MyNameIsTroll/newsbot/assets/31790025/34e0ef45-4166-49af-ac29-5a2e8d3cd34e)


2. Create a new application, name it after your robot.
  ![image](https://github.com/MyNameIsTroll/newsbot/assets/31790025/2122ede5-6fb2-436c-8f14-fb6c9794d3a7)


3. Copy your credentials into the ``newsbot.py`` script
5. Replace the path ``/HOME/USER/PATH/`` into ``newsbot.py`` with the path to your location on the server.

7. Paste your RSS feed(s) (one per line) into the ``rss_feeds.txt`` file.
8. In scipt ``newsbot.py``, modify the number of publications it should send per execution (default = 3).
9. Create a CRON task (``crontab -e``) with a call to the python script every X minutes. <br>
   EXAMPLE:<br>
   ``*/10 * * * * python /HOME/USER/PATH/newsbot.py``

10. Please remember to set your robot's toots to **Unlisted** to avoid flooding public instance.
   ![image](https://github.com/MyNameIsTroll/newsbot/assets/31790025/883b393b-4b20-42f8-aeac-a9842161b238)
11. Enjoy


   
