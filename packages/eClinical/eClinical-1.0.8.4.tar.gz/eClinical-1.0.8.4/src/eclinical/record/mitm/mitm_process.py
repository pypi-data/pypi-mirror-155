import os.path
import sys
from multiprocessing import Process
from mitmproxy.tools.main import mitmdump


class MitmProcess(Process):
    def __init__(self):
        Process.__init__(self)

    def set_host(self, host): self.host = host

    def run(self) -> None:
        # sys.argv = ['mitmdump', '-s', os.path.join(os.path.dirname(__file__), "mitm_addons.py"), '-p',
        #             '9999', '--ignore-hosts', '.*443$', '--set', 'upstream_cert=false', 'block_global=false']
        # sys.argv = ['mitmdump', '-s', os.path.join(os.path.dirname(__file__), "mitm_addons.py"), '-p',
        #             '9999', '--ignore-hosts', f'^(?![0-9\.]+:)(?!([^\.:]+\.)*{self.host}:80$', '--set',
        #             'upstream_cert=false']
        # sys.argv = ['mitmdump','-q', '-s', os.path.join(os.path.dirname(__file__), "mitm_addons.py"), '-p',
        #             '9999', '--allow-hosts', f'.*{self.host}:80$', 'block_global=false']
        sys.argv = ['mitmdump','-q', '-s', os.path.join(os.path.dirname(__file__), "mitm_addons.py"), '-p',
                    '9999', '--allow-hosts', f'.*dev-03-app-01.chengdudev.edetekapps.cn:81$', 'block_global=false']
        # argvs = [ '-s', os.path.join(os.path.dirname(__file__), "mitm_addons.py"), '-p',
        #             '9999', '--allow-hosts', '.*52.82.79.202:81$', '--set','block_global=false']
        mitmdump()

    def stop(self) -> None:
        if self.is_alive():
            self.kill()
