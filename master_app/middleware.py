import datetime
import traceback
from master_app.models import UserLogs, AdminLogs

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
    else:
       ip = request.META.get('REMOTE_ADDR')
    return ip, user_agent

class UserLocation:  
    def __init__(self, get_response):  
        self.get_response = get_response  
      
    def __call__(self, request):  
        # print(get_client_ip(request))
        # file1 = open('../log.txt', 'a+')
        # file1.writelines(get_client_ip(request))
        # file1.close()
        # print(request.get_full_path())
        ip, user_agent = get_client_ip(request)
        try:
            if request.get_full_path().startswith("/chpoen"):
                if not request.get_full_path().startswith("/chpoen/jsi18n"):
                    AdminLogs.objects.create(
                        public_ip_address = ip, 
                        user_agent = user_agent
                    )
            else:
                UserLogs.objects.create(
                    public_ip_address = ip, 
                    user_agent = user_agent
                )
        except :
            traceback.print_exc()
        response = self.get_response(request)  
        return response  