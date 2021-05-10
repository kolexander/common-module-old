from social_core.backends.linkedin import LinkedinOAuth2

class Linkedin(LinkedinOAuth2):
    def do_auth(self, access_token, *args, **kwargs):
        data = self.user_data(access_token, *args, **kwargs)
        response = kwargs.get('response') or {}
        response.update(data or {})
        if 'access_token' not in response:
            response['access_token'] = access_token
        kwargs.update({'response': response, 'backend': self})