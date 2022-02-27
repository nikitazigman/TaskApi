from rest_framework_simplejwt.tokens import AccessToken


class NoVerrificationAccessToken(AccessToken):
    def __init__(self, token=None):
        super().__init__(token, verify=False)
