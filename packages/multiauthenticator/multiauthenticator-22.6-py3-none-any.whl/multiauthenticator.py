"""
Authenticator allowing the use of multiple authentication mechanisms

Example of config:
    c.JupyterHub.authenticator_class = 'multiauthenticator.MultiAuthenticator'
    c.MultiAuthenticator.authenticators = [
        (GlobusOAuthenticator, '/globus', {
            'client_id': 'REDACTED',
            'client_secret': 'REDACTED',
            'oauth_callback_url': 'http://localhost:8000/hub/globus/oauth_callback'
        }),
        (GenePatternAuthenticator, '/genepattern', {
            'service_name': 'GenePattern',
            'users_dir_path': '/data/users',
            'default_nb_dir': '/data/default'
        }),
"""
from jupyterhub.auth import Authenticator
from jupyterhub.utils import url_path_join
from traitlets import List


class MultiAuthenticator(Authenticator):
    """Authenticator that proxies to more than one authentication provider for JupyterHub"""
    authenticators = List(help="List of authenticators to proxy", config=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._authenticators = []
        for (authenticator_class, url_proxy, authenticator_config) in self.authenticators:
            configuration = self.trait_values()
            configuration.pop("login_service")  # Prevent overwriting value of authenticator_class

            class AuthenticatorWrapper(authenticator_class):
                url_scope = url_proxy

                def login_url(self, base_url):
                    return super().login_url(url_path_join(base_url, self.url_scope))

                def logout_url(self, base_url):
                    return super().logout_url(url_path_join(base_url, self.url_scope))

                def get_handlers(self, app):
                    handlers = super().get_handlers(app)
                    return [(url_path_join(self.url_scope, path), handler) for path, handler in handlers]

            service_name = authenticator_config.pop("service_name", None)
            configuration.update(authenticator_config)
            authenticator = AuthenticatorWrapper(**configuration)
            if service_name: authenticator.service_name = service_name
            self._authenticators.append(authenticator)

    def get_custom_html(self, base_url):
        """Generate one sign on button per configured authenticator"""
        html = []
        for auth in self._authenticators:
            if hasattr(auth, "service_name"): auth_service = getattr(auth, "service_name")
            else: auth_service = auth.login_service
            login_url = auth.login_url(base_url)
            html.append(
                f"""<div class="service-login">
                        <a href='{login_url}'>
                            <object data="/hub/static/images/login-{auth_service}.png" type="image/png">
                                <a class='btn btn-jupyter btn-lg'>Sign in with {auth_service}</a>
                            </object>
                        </a>
                    </div>"""
            )
        return "\n".join(html)

    def get_handlers(self, app):
        """Return all handlers configured authenticators"""
        proxies = []
        for auth in self._authenticators:
            for path, handler in auth.get_handlers(app):
                class HandlerWrapper(handler):
                    """Handler configured for each authenticator"""
                    authenticator = auth
                proxies.append((path, HandlerWrapper))
        return proxies
