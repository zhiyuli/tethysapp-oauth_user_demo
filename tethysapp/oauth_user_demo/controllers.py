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
    output = ""
    current_user = request.user
    
    social = request.user.social_auth.get(provider='hydroshare')
    #access_token_old = request.user.social_auth.get(provider='hydroshare').extra_data['access_token']
    #output += "old token: " + str(access_token_old)
    refresh = social.refresh_token()
    output += str("refresh:") + str(refresh)
    access_token = request.user.social_auth.get(provider='hydroshare').extra_data['access_token']
    output += str("new token: ")+str(access_token)
    client_id = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_KEY", "None") 
    client_secret = getattr(settings, "SOCIAL_AUTH_HYDROSHARE_SECRET", "None")
    access_token = request.user.social_auth.get(provider='hydroshare').extra_data['access_token']
  
    for key in social.extra_data:
      output +=  str(key) +  str('-->') + str(social.extra_data[key])
    
    token = {
       "access_token": access_token,
       "token_type": "Bearer",
       "expires_in": request.user.social_auth.get(provider='hydroshare').extra_data['expires'],
       "refresh_token": "123",
       "scope": "read write groups"
                 }
    auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
    output += str("clientid:") + str(client_id) +";__  "+str("client_secret: ")+str(client_secret)
    try:
    	hs = HydroShare(auth=auth, hostname='playground.hydroshare.org')
    	for resource in hs.getResourceList():
          output += str(resource)
    except TokenExpiredError as e:
        output += str("Token Expired!")
        request.user.social_auth.get(provider='hydroshare').refresh_token()
        new_access_token = request.user.social_auth.get(provider='hydroshare').extra_data['access_token']
        output += str('new_access_token: ') + str(new_access_token)
        auth = HydroShareAuthOAuth2(client_id, client_secret, token=token)
        hs = HydroShare(auth=auth, hostname='playground.hydroshare.org')
        for resource in hs.getResourceList():
          output += str(resource)
    except:
        output += str("error!")    
        
    abstract = 'My abstract'
    title = 'My resource'
    keywords = ('my keyword 1', 'my keyword 2')
    rtype = 'GenericResource'
    fpath = '/tmp/icon.gif'
    resource_id = hs.createResource(rtype, title, resource_file=fpath, keywords=keywords, abstract=abstract)
    
    context = {"output": output, "resource_id": resource_id}
    
    return render(request, 'oauth_user_demo/home.html', context)
