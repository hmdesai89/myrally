
filename='rally_timestamp.log'

def datacrunch():
    action_list = []
    action_detail = []
    f = open(filename,'r')
    exc = 0
    for line in f :
        resp_time = line.rsplit(' ',6)
        if resp_time[1] not in action_list : 
            action_list.append(resp_time[1])
            ok_resp = 0
            if resp_time[5] == '200':
                ok_resp = 1
            action_detail.append({'action_name': resp_time[1],  'count': 1, 'total': float(resp_time[3]), 'min_time': float(resp_time[3]),
                                  'max_time' : float(resp_time[3]), 'average': 0 , 'ok_resp' : ok_resp})
        
        elif resp_time[5] != 'Exception' :
            for action in action_detail :
                if action['action_name'] == resp_time[1] :
                    action['count'] = action['count'] + 1
                    action['total'] = action['total'] + float(resp_time[3])
                    if resp_time[5] == '200':
                        action['ok_resp'] +=1

                    if action['min_time'] > float(resp_time[3]) :
                        action['min_time'] = float(resp_time[3])
                    elif action['max_time'] < float(resp_time[3]) :
                        action ['max_time'] = float(resp_time[3])

        else :
            exc +=1 

    print '{:30s}|   {:}  |  {:}  |  {:}  |   {:} |  {:}  |'.format('action_name','count','average','min_time', 'max_time', 'ok resp')
    print '--------------------------------------------------------------------------------------------'
    for action in action_detail :
         action['average'] = action['total'] / action['count']
         print '{:30s}|   {:4}   |  {:.4f}   |   {:.4f}   |   {:.4f}   |   {:4}    |'.format(action['action_name'],action['count'],action['average'],action['min_time'], action['max_time'], action['ok_resp'])
         #print (action['action_name']+'\t|'+str(action['count'])+'\t|'+str(action['average'])+'\t|'+str(action['min_time'])+
         #        '\t|'+str(action['max_time']))   
    f.close()
    print 'total number of exception in client = {}'.format(exc)
    return action_detail

class Action() :
    def __init__(action_name) :
        self.action_name = action_name
        self.count = 0
        self.total = 0
        self.min_time = None
        self.max_time = None

if __name__ == '__main__' :
    datacrunch()
