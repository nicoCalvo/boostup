import logging

from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
#from jinja2 import TemplateNotFound

from models.deal import Deal
from models.token import Token

from services.hubspot.hubspot_api import HubSpotApi

from models.token import Token


logger = logging.getLogger(__name__)

home_page = Blueprint('home_page', __name__,
                      template_folder='templates')


AUTH_REDIRECT_URL = 'https://localhost:9999/callback'

SCOPES = ['contacts']


@home_page.route('/')
def get():
    token = Token.objects.first()
    if token is None:
        auth_url = HubSpotApi.get_auth_url(AUTH_REDIRECT_URL, SCOPES)
        return redirect(auth_url)
    elif not token.is_valid():
        try:
            new_token = HubSpotApi.get_new_token(token.refresh_token)
            token.delete()
            Token(**new_token).save()
        except:
            logger.exception('Error updating access token')
            abort(500)
    return redirect(url_for('.deals'))


@home_page.route("/callback", methods=["GET"])
def callback():
    code = request.values.get("code")
    token = HubSpotApi.fetch_token(code=code, auth_resp_url=request.url, auth_callback_url=AUTH_REDIRECT_URL)
    try:
        Token(**token).save()
    except:
        logger.exception('Error storing new token')
        abort(500)
    return redirect(url_for('.deals'))


@home_page.route("/deals", methods=["GET"])
def deals():
    # TODO: apply fetch of deals
    pass