## FAZ-paperboy

FAZ-paperboy is a command line tool to deliver your FAZ or F.A.S.
newspaper freshly every day. Its CLI signature is as follows:

    usage: paperboy.py [-h] --user-agent USER_AGENT --output-directory
                       OUTPUT_DIRECTORY --username USERNAME --password PASSWORD
                       [--cookie-file COOKIE_FILE] [--debug]
    
    FAZ-paperboy delivers your FAZ or F.A.S. newspaper freshly every day.
    
    optional arguments:
      -h, --help            show this help message and exit
      --user-agent USER_AGENT, -ua USER_AGENT
                            User agent you want paperboy to use.
      --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                            Directory to store the PDFs of the downloaded
                            newspaper issues.
      --username USERNAME, -u USERNAME
                            User name to login at http://faz.net for the e-paper
                            download.
      --password PASSWORD, -p PASSWORD
                            Password for user given by --username.
      --cookie-file COOKIE_FILE, -c COOKIE_FILE
                            File to store the cookies in.
      --debug, -d           Increase verbosity.

It is written for Python 3.x and requires the modules
[requests](https://pypi.python.org/pypi/requests/) and
[beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4/).

### Similar Software

* *faz2kindle*:
  * Blog post [FAZ to Kindle in Python](http://www.peterhofmann.me/2013/11/faz-to-kindle-in-python/)
  * [faz2kindle on Github](https://github.com/peteh/faz2kindle)

