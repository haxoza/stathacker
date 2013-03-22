from ghost import Ghost
from pprint import pprint
from time import sleep
from pyquery import PyQuery as pq
from lxml.html import HtmlElement
import re


class GAGetterException(Exception):
    pass


class GAGetter(object):

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.ghost = Ghost(wait_timeout=20)

    def test(self):
        self.sign_in()
        self.go_to_realtime_site()
        sleep(10)
        print 'COUNTER: {0}'.format(self.get_counter())

    def sign_in(self):
        page, resources = self.ghost.open(
                                'http://www.google.com/analytics/index.html')
        self.ghost.wait_for_text('Analytics')
        self.ghost.wait_for_selector('a.secondary-button')
        self.ghost.click('a.secondary-button')
        self.ghost.wait_for_text("Can't access your account?")
        self._fill_signin_form()
        self.ghost.wait_for_text('All Accounts')

    def _fill_signin_form(self):
        result, resources = self.ghost.fill(
                    "form", {
                        "Email": self.email,
                        "Passwd": self.password
                    }
                                            )

        page, resources = self.ghost.fire_on(
                                "form", "submit", expect_loading=True)
        self.ghost.wait_for_page_loaded()

    def go_to_realtime_site(self):
        m = re.search(
            r"#report/visitors-overview/([a-z0-9]+)/",
            self.ghost.content
        )
        self.ghost.evaluate(
            "window.location.href = '#realtime/rt-overview/{0}/'".format(
                m.group(1)
            )
        )
        self.ghost.wait_for_text('Right now')
        return self.ghost.content

    def get_counter(self):
        d = pq(self.ghost.content)
        return d('#ID-overviewCounterValue').html()


if __name__ == '__main__':
    getter = GAGetter('pitu1234a@gmail.com', '********')
    getter.test()
