from django.test import TestCase

# Create your tests here.
def get_client_ip(request) -> object:
    x = request.META.get('HTTP_X_FORWARDED_FOR')
    print(x)
    if x:
        ip = x.split(',')[0]
        print(ip, '+++++++++++++++++++++++++++')
    else:
        ip = request.META.get('REMOTE_ADDR')
        print(ip)

    return ip
