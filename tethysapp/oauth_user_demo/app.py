from tethys_sdk.base import TethysAppBase, url_map_maker


class OauthUserDemo(TethysAppBase):
    """
    Tethys app class for OAuth User Demo.
    """

    name = 'OAuth User Demo'
    index = 'oauth_user_demo:home'
    icon = 'oauth_user_demo/images/icon.gif'
    package = 'oauth_user_demo'
    root_url = 'oauth-user-demo'
    color = '#2ecc71'
        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='oauth-user-demo',
                           controller='oauth_user_demo.controllers.home'),
        )

        return url_maps