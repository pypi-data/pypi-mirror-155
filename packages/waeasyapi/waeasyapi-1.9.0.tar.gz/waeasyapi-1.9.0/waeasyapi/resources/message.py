from .base import Resource
from ..constants.url import URL
import warnings


class Message(Resource):
    def __init__(self, client=None):
        super(Message, self).__init__(client)
        self.base_url = URL.MESSAGE_URL

    def sendMessage(self, data={}):
        """"
        Send message to the number

        Args:
            number : mobile number of the receiver
            message : message you want to send

        Returns:
            Status 
        """
        url = "{}/message".format(self.base_url)
        return self.post_url(url, data)

    def sendTemplate(self, data={}):
        """"
        Send template to the number

        Args:
            number : mobile number of the receiver
            message : message you want to send
            params : object including all required parameters

        Returns:
            Status 
        """
        url = "{}/template".format(self.base_url)
        return self.post_url(url, data)

    def sendMedia(self, data={}):
        """"
        Send media to the number

        Args:
            number : mobile number of the receiver
            message : message you want to send
            params : object including all required parameters

        Returns:
            Status 
        """
        url = "{}/media".format(self.base_url)
        return self.post_url(url, data)
