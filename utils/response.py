


class BaseResponse(object):

    def __init__(self):

        self.status=False
        self.message=None
        self.data= None

    def get_dic(self):
        return  self.__dict__

