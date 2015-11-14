from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_auth.models import UserSocialAuth
from django.conf import settings
# from oauthlib.oauth2 import TokenExpiredError
from hs_restclient import HydroShare, HydroShareAuthOAuth2

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    output = ""
    current_user = request.user
    
    social = request.user.social_auth.get(provider='hydroshare')
    
    client_id = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_KEY", "None") 
    client_secret = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_SECRET", "None")
    access_token = social.extra_data['access_token']
    token = {
       "access_token": access_token,
       "token_type": "Bearer",
       "expires_in": 36000,
       "refresh_token": "123",
       "scope": "read write groups"
                 }
    auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
    try:
    	hs = HydroShare(auth=auth)
    	for resource in hs.getResourceList():
          output += str(resource)
    except:
    	output += str("error!") 
    
    output += str(access_token) +"\n"+ str(client_id) +"\n"+str(client_secret)
    context = {"output": output}

    return render(request, 'oauth_user_demo/home.html', context)
