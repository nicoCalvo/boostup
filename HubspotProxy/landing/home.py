import json
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
from services.hubspot.endpoints.endpoint import Endpoint


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
            token.update(**new_token)
            token.save()
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
    """
    Deals endpoint fetches all deals in HubSpot API
    If token is not valid nor present, the data it's considered obsolete and
    new deals are pulled from the API.

    """
    token = Token.objects.first()
    if token is None:
        Deal.objects.all().delete()
        return redirect(url_for('home_page.get'))
    elif not token.is_valid():
        Deal.objects.all().delete()
        new_token = HubSpotApi.get_new_token(token.refresh_token)
        token.update(**new_token)
        token.save()
    try:
        hubspot_api = HubSpotApi(token)
        deal_endpoint = Endpoint.create('deals')
        response = deal_endpoint.fetch_data(hubspot_api)
        Deal.objects.all().delete()
        deals = [Deal(**data) for data in response]
        Deal.objects.insert(deals, load_bulk=False)
    except Exception:
        logger.exception(f'Error accessing requested endpoint {deal_endpoint.get_url()}')
        abort(500)
    return render_template('deals.html', deals=json.loads(Deal.objects().to_json()))

