import requests
import check_ad
from BeautifulSoup import BeautifulSoup 
import sys

class MyPrint():

    LOGIN_URL = "https://PRINTCASCL.intranet.epfl.ch:2941/webtools/"
    JOB_URL = "https://PRINTCASCL.intranet.epfl.ch:2941/webtools/jobsview.html"

    def __init__(self, username, password):
        """docstring for __init__"""
        ad_info = check_ad.get_info(username)
        self.username = ad_info.get('Logon name (NTLanman)')
        self.password = password
        self.session = requests.Session()
        self.__login()

    def post(self, *args, **kwargs):
        return self.session.post(*args, verify='printcascl.intranet.epfl.ch', **kwargs)

    def get(self, *args, **kwargs):
        return self.session.get(*args, verify='printcascl.intranet.epfl.ch', **kwargs)

    @property
    def balance(self):
        req = self.get(MyPrint.LOGIN_URL)
        soup = BeautifulSoup(req.content)
        return float(soup.findAll('tr')[-1].findAll('td')[-1].text.strip('fr. '))
        #Total balance:

    def get_jobs(self):
        req = self.get(MyPrint.JOB_URL)
        soup = BeautifulSoup(req.content)
        return [el.text for el in soup.find('select').children]

    def delete_job(self, job_id):
        req = self.get(MyPrint.JOB_URL)
        soup = BeautifulSoup(req.content)
        return [el.text for el in soup.find('select').children]

    def __login(self):
        page = self.get(MyPrint.LOGIN_URL)
        if page.status_code != 200:
            raise Error()
        soup = BeautifulSoup(page.content)
        username_field = soup.find('input', attrs={'type': 'text'})['name']
        password_field = soup.find('input', attrs={'type': 'password'})['name']
        print(username_field)
        print(password_field)
        res = self.post(MyPrint.LOGIN_URL, data={username_field: self.username, password_field: self.password, 'B1': 'login'}).content
        #return res





if __name__ == '__main__':
    print(MyPrint(sys.argv[1], sys.argv[2]).balance)
