from core.settings import VALIDITY_ENDPOINT
import requests

class CDCJobs:

    @classmethod
    def check(cls):

        print('[CDC] checking')

        # processor
        url = VALIDITY_ENDPOINT + '/validity/cdc'       
        response = requests.get(url)

        print(response)