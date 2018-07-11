## FAZ-paperboy

FAZ-paperboy is a command line tool to deliver your FAZ or F.A.S.
newspaper freshly every day. Its CLI signature is as follows:

    $ ./paperboy.py --help
    usage: paperboy.py [-h] --user-agent USER_AGENT --output-directory
                       OUTPUT_DIRECTORY --fullname FULLNAME --username USERNAME
                       --password PASSWORD [--cookie-file COOKIE_FILE]
                       [--filename-template FILENAME_TEMPLATE] [--debug]
    
    FAZ-paperboy delivers your FAZ or F.A.S. newspaper freshly every day.
    
    optional arguments:
      -h, --help            show this help message and exit
      --user-agent USER_AGENT, -ua USER_AGENT
                            User agent you want paperboy to use.
      --output-directory OUTPUT_DIRECTORY, -o OUTPUT_DIRECTORY
                            Directory to store the PDFs of the downloaded
                            newspaper issues.
      --fullname FULLNAME, -f FULLNAME
                            Full name of the user as shown when logged in to the
                            profile on https://www.faz.net/mein-faz-net/profil/ -
                            used to check if logged in successfully.
      --username USERNAME, -u USERNAME
                            User name to login at https://faz.net for the e-paper
                            download.
      --password PASSWORD, -p PASSWORD
                            Password for user given by --username.
      --cookie-file COOKIE_FILE, -c COOKIE_FILE
                            File to store the cookies in.
      --filename-template FILENAME_TEMPLATE, -t FILENAME_TEMPLATE
                            Template for the output filenames. By default this is
                            "{isodate}_{orig_newspaper}.pdf". {isodate} is the
                            date in the format YYYY-MM-DD. For the date in the
                            format YYYYMMDD, just use {date}. If you want to use
                            the original filename of the PDFs, you could use
                            "{original}.pdf". For a short version of the newspaper
                            name, there is also {newspaper}.
      --debug, -d           Increase verbosity.

It is written for Python 3.x and requires the modules
[requests](https://pypi.python.org/pypi/requests/) and
[beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4/).

### Similar Software

* *faz2kindle*:
  * Blog post [FAZ to Kindle in Python](http://www.peterhofmann.me/2013/11/faz-to-kindle-in-python/)
  * [faz2kindle on Github](https://github.com/peteh/faz2kindle)

