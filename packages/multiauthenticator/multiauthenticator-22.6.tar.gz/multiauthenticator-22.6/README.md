# multiauthenticator

An authenticator plugin for JupyterHub that allows you to configure several authentication services.

Example configuration is below:

```python
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
]
```