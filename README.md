# vaultwarden-render-deploy
Vaultwarden on Render.com infrastructure

**This is still a work in progress and may reflect in progress changes. PRs are welcome, the Python code is atrocious...**

## Notes

Render's API does not allow us to create new service using the free tier via the API. So we need to create the service manually and then use the API to update the service.

You will need to supply your own database for this purposes. I am using the free tier of filess.io. You can use any other database provider as long as it is supported by the upstream MySQL project. 

With exception, Planetscale is not supported by the upstream project due to its needs to connect via TLS, which Diesel does not support in Vaultwarden's current status.

## Create Process

1. Create a new account on Render.com
2. Create a new `Web Service` on Render.com using this fokred repository in your own account. You may use `Public Git Repository` and enter your own repo URL.
3. In the Create screen, select a name for your Vaultwarden instance, environment type set to `Docker`, region wherever is closest to you (and your database), branch as `main`, and lastly the `Free` plan. Click create and take note of your application name.
4. After clicking create, your Vaultwarden instance will be built from the Dockerfile in this repository. This will take a few minutes.
5. Add environment variables as needed from the below list, you may reference this via the [Vaultwarden Wiki](https://github.com/dani-garcia/vaultwarden/wiki):

| Name | Description | Example | Required |
| --- | --- | --- | --- |
| `_ENABLE_DUO` | Enable Duo integration for pre-configured databases | `true` | No |
| `DATABASE_URL` | The database URL of your MySQL or PostgresSQL database | `mysql://[[user]:[password]@]host[:port][/database]` | Yes |
| `DUO_SKEY` | Duo Authentication SKEY, found in account | `abc123` | No |
| `DUO_IKEY` | Duo Authentication SKey, found in account | `acb123` | No |
| `DUO_HOST` | Duo Authentication Host, found in account | `api-23423tgf.duosecurity.com` | No |
| `SMTP_HOST` | The hostname for mail sending | `mail.mailserver.ccom` | No |
| `SMTP_FROM` | The email address listed in FROM field received by user | `vaultwarden@mailserver.com` | No |
| `SMTP_PORT` | The port for SMTP sending | `587` | No |
| `SMTP_SECURITY` | The security options to set for SMTP sending, following options: `starttls`, `force_tls` and `off` | `starttls` | No |
| `SMTP_USERNAME` | The username of your SMTP login | `vaultwarden@mailserver.com` | No |
| `SMTP_PASSWORD` | The password of your SMTP login | `mysupersecretpassword` | No |

