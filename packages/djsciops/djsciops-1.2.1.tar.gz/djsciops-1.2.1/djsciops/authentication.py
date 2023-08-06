import base64
from datetime import datetime, timezone
import json
import logging
import flask
import webbrowser
import multiprocessing
import urllib
import http.client
import botocore
from .log import log
from time import time

import boto3
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

LOOKUP_SERVICE_ALLOWED_ORIGIN = "https://ops.datajoint.io"
LOOKUP_SERVICE_DOMAIN = "ops.datajoint.io"
LOOKUP_SERVICE_ROUTE = "/social-login/api/user"
LOOKUP_SERVICE_AUTH_PROVIDER = "accounts.datajoint.io"


def _oidc_login(
    auth_client_id: str,
    auth_url: str = "https://accounts.datajoint.io/auth/auth",
    lookup_service_allowed_origin: str = LOOKUP_SERVICE_ALLOWED_ORIGIN,
    lookup_service_domain: str = LOOKUP_SERVICE_DOMAIN,
    lookup_service_route: str = LOOKUP_SERVICE_ROUTE,
    lookup_service_auth_provider: str = LOOKUP_SERVICE_AUTH_PROVIDER,
    code_challenge: str = "ubNp9Y0Y_FOENQ_Pz3zppyv2yyt0XtJsaPqUgGW9heA",
    code_challenge_method: str = "S256",
    code_verifier: str = "kFn5ZwL6ggOwU1OzKx0E1oZibIMC1ZbMC1WEUXcCV5mFoi015I9nB9CrgUJRkc3oiQT8uBbrvRvVzahM8OS0xJ51XdYaTdAlFeHsb6OZuBPmLD400ozVPrwCE192rtqI",
    callback_port: int = 28282,
    delay_seconds: int = 60,
):
    """
    Primary OIDC login flow.
    """
    # Prepare user
    log.warning(
        "User authentication required to use DataJoint SciOps CLI tools. We'll be "
        "launching a web browser to authenticate your DataJoint account."
    )
    # allocate variables for access and context
    code = None
    cancelled = True
    # Prepare HTTP server to communicate with browser
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app = flask.Flask("browser-interface")

    def shutdown_server():
        """
        Shuts down Flask HTTP server.
        """
        func = flask.request.environ.get("werkzeug.server.shutdown")
        if func is not None:
            # Ensure running with the Werkzeug Server
            func()

    @app.route("/login-cancelled")
    def login_cancelled():
        """
        Accepts requests which will cancel the user login.
        """
        shutdown_server()
        return """
        <!doctype html>
        <html>
          <head>
            <script>
              window.onload = function load() {
              window.open('', '_self', '');
              window.close();
              };
            </script>
          </head>
          <body>
          </body>
        </html>
        """

    @app.route("/login-completed")
    def login_completed():
        """
        Redirect after user has successfully logged in.
        """
        nonlocal code
        nonlocal cancelled
        cancelled = False
        code = flask.request.args.get("code")
        shutdown_server()
        return """
        <!doctype html>
        <html>
          <head>
            <script>
              window.onload = function load() {
              window.open('', '_self', '');
              window.close();
              };
            </script>
          </head>
          <body>DataJoint login completed! Feel free to close this tab if it did not close automatically.</body>
        </html>
        """

    # build url
    query_params = dict(
        scope="openid",
        response_type="code",
        client_id=auth_client_id,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        redirect_uri=f"http://localhost:{callback_port}/login-completed",
    )
    link = f"{auth_url}?{urllib.parse.urlencode(query_params)}"
    # attempt to launch browser or provide instructions
    browser_available = True
    try:
        webbrowser.get()
    except webbrowser.Error:
        browser_available = False
    if browser_available:
        log.info("Browser available. Launching...")
        webbrowser.open(link, new=2)
    else:
        log.warning(
            "Brower unavailable. On a browser client, please navigate to the "
            f"following link to login: {link}"
        )
    # start response server
    cancel_process = multiprocessing.Process(
        target=_delayed_request,
        kwargs=dict(
            url=f"http://localhost:{callback_port}/login-cancelled",
            delay=delay_seconds,
        ),
    )
    # cancel_process.start()
    app.run(host="0.0.0.0", port=callback_port, debug=False)
    # cancel_process.terminate()
    # received a response
    if cancelled:
        raise Exception(
            "User login cancelled. User must be logged in to use DataJoint SciOps CLI tools."
        )
    else:
        # generate user info
        connection = http.client.HTTPSConnection(lookup_service_domain)
        headers = {
            "Content-type": "application/json",
            "Origin": lookup_service_allowed_origin,
        }
        body = json.dumps(
            {
                "auth_provider": lookup_service_auth_provider,
                "redirect_uri": f"http://localhost:{callback_port}/login-completed",
                "code_verifier": code_verifier,
                "client_id": auth_client_id,
                "code": code,
            }
        )
        connection.request("POST", lookup_service_route, body, headers)
        userdata = json.loads(connection.getresponse().read().decode())
        log.info("User successfully authenticated.")
        return userdata["access_token"], userdata["username"], userdata["refresh_token"]


def _delayed_request(*, url: str, delay: str = 0):
    time.sleep(delay)
    return urllib.request.urlopen(url)


def _decode_bearer_token(bearer_token):
    log.debug(f"bearer_token: {bearer_token}")
    jwt_data = json.loads(
        base64.b64decode((bearer_token.split(".")[1] + "==").encode()).decode()
    )
    log.debug(f"jwt_data: {jwt_data}")
    return jwt_data


class Session:
    def __init__(
        self,
        aws_account_id: str,
        s3_role: str,
        auth_client_id: str,
        bearer_token: str = None,
    ):
        self.aws_account_id = aws_account_id
        self.s3_role = s3_role
        self.auth_client_id = auth_client_id
        self.sts_arn = f"arn:aws:iam::{aws_account_id}:role/{s3_role}"

        # OAuth2.0 authorization
        if not bearer_token:
            self.bearer_token, self.user, self.refresh_token = _oidc_login(
                auth_client_id=auth_client_id,
            )
            self.jwt = _decode_bearer_token(self.bearer_token)
        else:
            self.jwt = _decode_bearer_token(self.bearer_token)
            time_to_live = (self.jwt["exp"] - datetime.utcnow().timestamp()) / 60 / 60
            log.info(
                f"Reusing provided bearer token with a life of {time_to_live} [HR]"
            )
            self.bearer_token, self.user = (bearer_token, self.jwt["sub"])

        self.sts_token = RefreshableBotoSession(session=self).refreshable_session()
        self.s3 = self.sts_token.resource("s3")

    def refresh_bearer_token(
        self,
        lookup_service_allowed_origin: str = LOOKUP_SERVICE_ALLOWED_ORIGIN,
        lookup_service_domain: str = LOOKUP_SERVICE_DOMAIN,
        lookup_service_route: str = LOOKUP_SERVICE_ROUTE,
        lookup_service_auth_provider: str = LOOKUP_SERVICE_AUTH_PROVIDER,
    ):

        # generate user info
        connection = http.client.HTTPSConnection(lookup_service_domain)
        headers = {
            "Content-type": "application/json",
            "Origin": lookup_service_allowed_origin,
        }
        body = json.dumps(
            {
                "auth_provider": lookup_service_auth_provider,
                "refresh_token": self.refresh_token,
                "client_id": self.auth_client_id,
            }
        )
        log.debug(f"Original refresh_token: {self.refresh_token}")
        connection.request("PATCH", lookup_service_route, body, headers)
        response = connection.getresponse().read().decode()
        log.debug(f"response: {response}")
        userdata = json.loads(response)
        log.debug("User successfully reauthenticated.")
        self.bearer_token = userdata["access_token"]
        self.user = userdata["username"]
        self.refresh_token = userdata["refresh_token"]
        log.debug(f"refresh_token: {self.refresh_token}")
        self.jwt = _decode_bearer_token(self.bearer_token)


class RefreshableBotoSession:
    """
    Boto Helper class which lets us create refreshable session, so that we can cache the client or resource.

    Usage
    -----
    session = RefreshableBotoSession().refreshable_session()

    client = session.client("s3") # we now can cache this client object without worrying about expiring credentials
    """

    def __init__(self, session, session_ttl: int = 12 * 60 * 60):
        """
        Initialize `RefreshableBotoSession`

        Parameters
        ----------
        session : Session
            The session object to refresh

        session_ttl : int (optional)
            An integer number to set the TTL for each session. Beyond this session, it will renew the token.
        """

        self.session = session
        self.session_ttl = session_ttl

    def __get_session_credentials(self):
        """
        Get session credentials
        """
        sts_client = boto3.client(service_name="sts")
        try:
            sts_response = sts_client.assume_role_with_web_identity(
                RoleArn=self.session.sts_arn,
                RoleSessionName=self.session.user,
                WebIdentityToken=self.session.bearer_token,
                DurationSeconds=self.session_ttl,
            ).get("Credentials")
        except botocore.exceptions.ClientError as error:
            log.debug(f"Error code: {error.response['Error']['Code']}")
            if error.response["Error"]["Code"] == "ExpiredTokenException":
                log.debug("Bearer token has expired... Reauthenticating now")
                self.session.refresh_bearer_token()
                sts_response = sts_client.assume_role_with_web_identity(
                    RoleArn=self.session.sts_arn,
                    RoleSessionName=self.session.user,
                    WebIdentityToken=self.session.bearer_token,
                    DurationSeconds=self.session_ttl,
                ).get("Credentials")
            else:
                raise error
        # Token expire time logging
        bearer_expire_time = datetime.fromtimestamp(self.session.jwt["exp"]).strftime(
            "%H:%M:%S"
        )
        log.debug(f"Bearer token expire time: {bearer_expire_time}")
        if "sts_token" in self.session.__dict__:
            sts_expire_time = (
                self.session.sts_token._session.get_credentials()
                .__dict__["_expiry_time"]
                .replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
                .strftime("%H:%M:%S")
            )
            log.debug(f"STS token expire time: {sts_expire_time}")

        credentials = {
            "access_key": sts_response.get("AccessKeyId"),
            "secret_key": sts_response.get("SecretAccessKey"),
            "token": sts_response.get("SessionToken"),
            "expiry_time": sts_response.get("Expiration").isoformat(),
        }

        return credentials

    def refreshable_session(self) -> boto3.Session:
        """
        Get refreshable boto3 session.
        """
        # get refreshable credentials
        refreshable_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.__get_session_credentials(),
            refresh_using=self.__get_session_credentials,
            method="sts-assume-role-with-web-identity",
        )

        # attach refreshable credentials current session
        session = get_session()
        session._credentials = refreshable_credentials
        autorefresh_session = boto3.Session(botocore_session=session)

        return autorefresh_session
