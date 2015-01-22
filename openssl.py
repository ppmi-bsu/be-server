import itertools
import random
import subprocess
import locale
import os
from termcolor import colored



OPENSSL_DIR = '/home/mihas/openssl/openssl'

OPENSSL_EXE = OPENSSL_DIR + '/apps/openssl'
os.environ['LD_LIBRARY_PATH'] = OPENSSL_DIR

os.environ['OPENSSL_CONF'] = './openssl.cnf'

encoding = locale.getdefaultlocale()[1]


OPENSSL_OUTPUT_COLOR = 'magenta'


def openssl_call(cmd):

    if isinstance(cmd, str):
        cmd_list = cmd.split(' ')
    elif isinstance(cmd, list):
        cmd_list = list(itertools.chain(
                *(arg.split(' ') if isinstance(arg, str) else [str(arg)] for arg in cmd)
            ))
    else:
            raise AttributeError()

    print colored('openssl ' + ' '.join(cmd_list), 'green')
    out = subprocess.check_output([OPENSSL_EXE] + cmd_list).decode(encoding)
    print colored(out, OPENSSL_OUTPUT_COLOR)
    return out


CAPRIV_KEY_FILE = 'demoCA/private/cakey.pem'
CERT_FILE = "cert.pem"
CACERT_FILE = "demoCA/cacert.pem"

openssl_call('genpkey -algorithm bign-pubkey -out %s' % CAPRIV_KEY_FILE)
openssl_call([
    "req -x509",
    "-subj", u"/CN={CN}/O=My Dom, Inc./C=US/ST=Oregon/L=Portland".format(CN='www.mydom_%s.com' % random.randint(0, 10000)),
    ("-new -key %s -out %s" % (CAPRIV_KEY_FILE, CACERT_FILE))])


def issue_cert(req_file_path):
    out = openssl_call([
        "ca",
        "-in " + req_file_path,
        "-cert " + CACERT_FILE,
        "-batch",
        ("-keyfile %s -out %s" % (CAPRIV_KEY_FILE, CERT_FILE))])
