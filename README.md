# dl-exam-submissions

A side project to help my Mother download exam submissions sent to an email.

## What it does

This project downloads attachments from emails on a specified date from a specified gmail account. Then it will sort the submissions into different folders for different professors. It also tracks which Roll Number's submissions it received.

**Robusteness**: It deals with submissions that whose roll numbers cannot be identified by saving them as [<Email-Source>].ext. For emails that did not have any attachments, it saves the message along with an identified Roll Numbers and the name of the Professor.

## How to Use

It requires certain things to facillitate OAuth2 and has helper functions for getting those in `oath2.py` provided by Google.

This will give you a **refresh token** that you need to paste in a file called `refreshToken`.

You also need to register with Google for a `client id` and `secret`. Please put these along with the `domain` of the imap server and the `email address` in config.json.

### Helpful Links

* [OAuth2.py Guide](https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough)
* [Google's Oath2 guide](https://developers.google.com/identity/protocols/oauth2)

## Acknowledgements

Special Thanks to **Vladimir Kaukin** and the others for their contributions to [imap-tools](https://github.com/ikvk/imap_tools) !
