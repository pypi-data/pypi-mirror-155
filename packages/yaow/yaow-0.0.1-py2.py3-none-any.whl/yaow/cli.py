import time
from threading import Thread
from queue import Queue, Empty
import sys
import pyotp
import datetime
from urllib.parse import parse_qs, urlparse
import validators
import keyring
import keyring.backend
import json
import re
from rich.traceback import install
from rich.console import Console
import subprocess
from O365 import Account, FileSystemTokenBackend
import getpass
import os
import yamlarg
#readline is required for >1024 response url for o365 authentication
import readline


class LocalKeyring(keyring.backend.KeyringBackend):
    priority = 1

    def __init__(self, filename):
        self.filename = filename

    def set_password(self, servicename, username, password):
        try:
            with open(self.filename, "r") as f:
                keyring = json.loads(f.read())
        except:
            keyring = dict()
        if servicename not in keyring:
            keyring[servicename] = dict()
        keyring[servicename][username] = password
        with open(self.filename, "w") as f:
            f.write(json.dumps(keyring))

    def get_password(self, servicename, username):
        with open(self.filename, "r") as f:
            keyring = json.loads(f.read())
        return keyring[servicename][username]

    def delete_password(self, servicename, username):
        with open(self.filename, "r") as f:
            keyring = json.loads(f.read())
        if servicename in keyring:
            keyring[servicename].pop(username, None)
        with open(self.filename, "w") as f:
            f.write(json.dumps(keyring))


def o365_authentication():
    id = get_or_set_password("openconnect", "o365id")
    pw = get_or_set_password("openconnect", "o365pw")
    credentials = (id, pw)
    try:
        token_backend = FileSystemTokenBackend(token_filename="o365_token.txt")
        account = Account(credentials, token_backend=token_backend)
        authenticated = account.is_authenticated
    except:
        with open("o365_token.txt", "w") as f:
            pass
        token_backend = FileSystemTokenBackend(token_filename="o365_token.txt")
        account = Account(credentials, token_backend=token_backend)
        authenticated = False
    # Check to make sure the o365_token.txt worked to authenticate the app.
    result = False
    if not authenticated:
        print("Please generate an o365_token.txt file to be used for authentication.")
        while not authenticated:
            try:
                result = account.authenticate(
                    scopes=["basic", "message_all", "offline_access"]
                )
                authenticated = account.is_authenticated
            except:
                pass
    # Refresh and save the O365 token.
    account.connection.refresh_token()
    account.connection.token_backend.save_token()
    return account


def get_totp(server):
    otp_secret = get_or_set_password("otp", server)
    if validators.url(otp_secret):
        secret = parse_qs(urlparse(otp_secret).query)["secret"][0]
    else:
        secret = otp_secret
    totp = pyotp.TOTP(secret)
    totp.interval - datetime.datetime.now().timestamp() % totp.interval
    return str(totp.now())


def enqueue_output(out, queue):
    while True:
        queue.put(out.read(1))


def get_or_set_password(service, username):
    creds = keyring.get_password(service, username)
    if creds is None:
        keyring.set_password(
            service,
            username,
            getpass.getpass(
                "Enter the password for " + service + ", username:" + username + ":"
            ),
        )
        creds = keyring.get_password(service, username)
    return creds


def get_output(q, start=""):
    output = [start.encode("utf-8")]
    while True:
        try:
            output.append(q.get_nowait())
        except Empty:
            return "".join([a.decode("utf-8") for a in output])


def print_and_return(orj, new):
    print(new, end="", flush=True)
    orj = orj + new
    return orj


def main():
    console = Console()
    # change cwd to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    args = yamlarg.parse("arguments.yaml")
    install(show_locals=args["debug"])

    # Set the keyring backend to a local file if a credential store is not installed.
    try:
        keyring.set_password("test", "test", "test")
        keyring.delete_password("test", "test")
    except:
        # set the keyring for keyring lib
        keyring.set_keyring(LocalKeyring(), filename=args["backupKeyringFile"])

    ON_POSIX = "posix" in sys.builtin_module_names

    script = ["sudo", "openconnect", args["server"], "--user=" + args["username"]]
    if args["servercert"] is not None:
        script.append("--servercert=" + args["servercert"])
    if args["group"] is not None:
        script.append("--authgroup=" + args["group"])
    if args["script"] is not None:
        script.append("--script=" + args["script"])
        print(args["script"])
    print(" ".join(script))

    p = subprocess.Popen(
        script, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE
    )

    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True  # thread dies with the program
    t.start()

    output = ""
    output = print_and_return(output, get_output(q))
    try:
        pw_sent = False
        un_sent = False
        rs_sent = False
        while True:
            time.sleep(0.1)
            if output[-9:] == "Password:" and not pw_sent:
                print("\nSending password.\n", end="", flush=True)
                p.stdin.write(
                    (
                        get_or_set_password(args["server"], args["username"]) + "\n\n"
                    ).encode("utf-8")
                )
                p.stdin.flush()
                pw_sent = True
                output = print_and_return(output, get_output(q))
            elif output[-9:] == "Username:" and not un_sent:
                p.stdin.write((args["username"]).encode("utf-8"))
                p.stdin.flush()
                un_sent = True
                output = print_and_return(output, get_output(q))
            elif output[-9:] == "Response:" and not rs_sent:
                if args["totp"]:
                    p.stdin.write((get_totp(args["server"]) + "\n").encode("utf-8"))
                    p.stdin.flush()
                    rs_sent = True
                elif args["email"] != "":
                    waiting_for_message = True
                    account = o365_authentication()
                    mailbox = account.mailbox(args["email"])
                    submit_time = time.time() - 60
                    while waiting_for_message:
                        twofa_folder = mailbox.inbox_folder().get_folder(
                            folder_name=args["folder"]
                        )
                        if (
                            time.mktime(
                                twofa_folder.get_messages().__next__().sent.timetuple()
                            )
                            < submit_time
                        ):
                            time.sleep(0.1)
                        else:
                            waiting_for_message = False
                            break
                    twofa_folder = twofa_folder = mailbox.inbox_folder().get_folder(
                        folder_name=args["folder"]
                    )
                    twofa_code = re.search(
                        args["regex"], twofa_folder.get_messages().__next__().body
                    ).group(1)
                    p.stdin.write((twofa_code + "\n").encode("utf-8"))
                    p.stdin.flush()
                    rs_sent = True
            else:
                output = print_and_return(output, get_output(q))

    except KeyboardInterrupt:
        if args["debug"]:
            console.print_exception(show_locals=True)
        try:
            subprocess.check_output("sudo pkill openconnect", shell=True)
        except:
            pass
        sys.exit()
