import time
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_auth.models import UserSocialAuth
from django.conf import settings
from oauthlib.oauth2 import TokenExpiredError
from hs_restclient import HydroShare, HydroShareAuthOAuth2
@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    logger = logging.getLogger('django')
    logger.error('Entering controller.py...')
    res_output = ""
   
    client_id = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_KEY", "None") 
    client_secret = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_SECRET", "None")
    token = request.user.social_auth.get(provider='hydroshare').extra_data['token_dict']
    
    token_dict_str = "Token: {0}".format(str(token))
    logger.error(token_dict_str)
    auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
    try:
        logger.error("Fetching resource list from playground.hydroshare.org")
        hs = HydroShare(auth=auth, hostname='playground.hydroshare.org')
        for resource in hs.getResourceList():
            res_output += str(resource) 
     
        context = {"res_output": res_output, "token_dict_str": token_dict_str}
    
        return render(request, 'oauth_user_demo/home.html', context)
    
    except TokenExpiredError as e:
        # TODO: redirect back to login view, giving this view as the view to return to
        logger.error("TokenExpiredError: TODO: redirect to login view")
        raise e
        

