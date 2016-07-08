import exception


class ValueMissing(Exception):

    def __init__(self, value):
        Exception.__init__(self,"Error reading file it is missing parameter", value)



class ErrorLoadingTest(Exception):

    def __init__(self):
        Exception.__init__(self,"Error Loading Test\n")#, value)

    def __init__(self, value):
        Exception.__init__(self,"Error Loading Test\n" + str(value))


class ErrorCreds(Exception):

    def __init__(self):
        Exception.__init__(self,"Error in Credentials. Please check\n")
