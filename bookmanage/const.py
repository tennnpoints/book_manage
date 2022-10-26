UNREAD = 0
READING = 1
END = 2
DELETE = 3
ERROR = 1
CLEAR = 0
def book_manage_ctxprocessor(req):
    return {
        'UNREAD': UNREAD,
        'READING': READING,
        'END': END,
        'DELETE': DELETE,
        'ERROR': ERROR,
        'CLEAR': CLEAR
    }