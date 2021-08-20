# Vue Azure Static Web App - Cosmos DB - AD B2C

This project demonstrates a basic VueJS web app built using Azure Static Web Apps, supported by two Python APIs, integrated with Azure Active Directory B2C for authentication, and backed by an Azure Cosmos DB database.  

### To do

1. Set up and test Azure Monitor

2. Set global headers according to this guide: https://content-security-policy.com/


## Project setup

The static web app is designed to integrate with an Azure Active Directory B2C tenant and an Azure Cosmos database. You may wish to set these resources up first (see **_Setting up Azure resources_** below). Alternatively, you can set up the web app first and leave the relevant configuration parameters for _AADB2C_ and _COSMOSDB_ blank for now.  

1. Create a new repo from the template and clone to local device.
2. Make a venv in the /api folder: 
    1. $ `cd api`
    2. Either...
        - Generic: $ `python3 -m venv .venv`
        - Mac M1 dev machine: $ `python3 -m virtualenv -p="/usr/local/homebrew/opt/python@3.8/bin/python3" .venv`
3. Activate the venv and confirm Python is using it:
    1. $ `source .venv/bin/activate`
    2. $ `which python3`
4. Install the Python packages: $ `pip3 install -r requirements.txt`
5. Create a  _/api/local.settings.json_ file and add:
    ```yaml
    {
        "IsEncrypted": false,
        "Values": {
            "AzureWebJobStorage": "",
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "Host": {
                "CORS": "http://localhost:4280"
            }
            "AADB2C_ID": <your-azure-ad-b2c-app-id>,
            "AADB2C_SECRET": <your-azure-ad-b2c-app-secret>,
            "COSMOSDB_URL": <your-cosmosdb-url>,
            "COSMOSDB_KEY": <your-cosmosdb-key>,
            "COSMOSDB_DATABASE": <your-cosmosdb-database-name>
        }
    }
    ```
6. Install the required yarn packages: 
    1. $ `cd ..`
    2. $ `yarn install`
7. Globally add vue-template-compiler: $ `npm i -g vue-template-compiler`
8. Run the app locally: $ `bash run.sh`
9. Launch the Azure Static Web App:
    1. In Visual Studio Code click on the Azure button.
    2. Go to 'Static Web Apps'.
    3. Click '+' to create a new static web app.
    4. Enter a name for the app. Select _Vue.js_. App code is in _/_ folder. Build output is _dist_.
    5. Wait for the app to build.
    6. Add the variables from api/local.settings.json to the Azure Static Web App's configuration.

#### Debugging runtime errors

1. Ensure that the /api/.venv activated and is using the correct Python version, especially when building on an Apple M1 chip. Run $ `which python3` from inside the venv to check.

#### Debugging deployment errors
1. Ensure that .github/workflows/azure-static-web-apps-xx-xx-xxx.yaml file has correct info. APIs should be at "/api" not "api".
2. Ensure that you've listed all devDependencies in package.json

## Running the project locally

```bash
bash run.sh
```

## Building on top of the boilerplate

1. Confirm that the app runs properly locally.
2. Use F1 to create a new Python API.

## Setting up Azure resources

Follow these steps to set the project up on Azure and link it to the required Azure resources. More information can be found below under 'Configuration'.

1. Register an Azure Active Directory B2C
2. Create a user flow for signup signin called 'signupsignin1'.
3. Create an application, then create a secret for that application.
4. Add ID and Secret to local.settings.json(AADB2C_ID and AADB2C_SECRET).
5. Add ID and Secret to web app configuration.
6. Under the 'Authentication' section of Azure AD add redirects (see below).
7. Create Cosmos DB serverless

## Configuration

Here is a complete description of the configuration variables you will need to set.  

### Development

#### /api/local.settings.json
These are values used by the Python APIs.  
- Values.AADB2C_ID: the application (client) ID of the static web app registered in Azure Active Directory B2C.  
- Values.AADB2C_SECRET: the value of the client secret generated in Azure Active Directory B2C for this web app.  
- Values.COSMOSDB_URL: the URL of the Cosmos DB.  
- Values.COSMOSDB_KEY: the secret key of the Cosmos DB.  
- Values.COSMOSDB_DATABASE: the name of the Cosmos DB database used by this web app.  

#### staticwebapp.config.json
These values are used by the Azure Static Web App.  
- routes /logout redirect: `https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{name-of-b2c-login-userflow}/oauth2/v2.0/logout?post_logout_redirect={static-webapp-url}/.auth/logout`
- auth.identityProviders.customOpenIdConnectProviders: we can name Azure Active Directory B2C anything here, but we'll call it 'aadb2c' to make things easy.
- auth.identityProviders.customOpenIdConnectProviders.aadb2c.registration.clientIdSettingName: should be kept as "AADB2C_ID" so that it pulls the variable 'AADB2C_ID' from _staticwebapp.config.json_.
- auth.identityProviders.customOpenIdConnectProviders.aadb2c.registration.clientCredential.clientSecretSettingName: should be kept as "AADB2C_SECRET" so that it pulls the variable 'AADB2C_SECRET' from _staticwebapp.config.json_.
- auth.identityProviders.customOpenIdConnectProviders.aadb2c.registration.openIdConnectConfiguration.wellKnownOpenIdConfiguration: `https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/v2.0/.well-known/openid-configuration?p={name-of-b2c-login-userflow}`.
- auth.identityProviders.customOpenIdConnectProviders.aadb2c.login.nameClaimType: "emails".
- auth.identityProviders.customOpenIdConnectProviders.aadb2c.login/scopes: ["openid", "profile"]

#### .env
These values are used by the Vue app.  
VUE_APP_NAME='name-of-your-web-app`  
VUE_APP_MAILTO=`mailto:your@emailaddress.com'  

### Production

#### /api/local.settings.json
Enter each value into the 'Configuration' page of the Azure Static Web App in the Azure Portal, or upload using the Azure CLI.  

#### staticwebapp.config.json
No action required: these variables are included in git and automatically deployed to production.  

#### .env
No action required: these variables are included in git and automatically deployed to production. The entire VueJS codebase is visible to users, so this .env file should **not** contain any sensitive variables. Use it only for the convenience of having variables in one place. Sensitive variables must instead be added to the 'Configuration' page of the Azure Static Web App in the Azure Portal, or upload using the Azure CLI.  

#### Azure AD B2C
Configure a _signupsignin_ user flow and a _passwordreset_ user flow. You must then create a web app in Azure AD B2C and configure the web app to use both user flows. On the web app's 'Authentication' page in the Azure Portal select 'Web' and configure 'Redirect URIs' to: `{webapp-url}.auth/login/aadb2c/callback` and `{webapp-url}.auth/logout/aadb2c/callback`. Front channel logout URL can be set to `https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{name-of-b2c-login-userflow}/oauth2/v2.0/logout/post_logout_redirect={webapp-url}/.auth/logout`, however at the time of writing the front channel logout URL appeared to have no impact on functionality. Tick both boxes for 'Access tokens' and 'ID tokens'.  

## Authentication

### Development

#### Login
When running locally, Azure Static Web Apps automatically mocks a login page to simulate a third-party authentication provider. Simply hit the 'Login' button and enter any username/email then click login.  

#### Logout
Manually navigate to `http://localhost:4280/.auth/logout` to log yourself out. The 'Logout' button is designed for the production version of the app and will not work in development.  

### Production

#### Login
The static web app is configured to use Azure Active Directory B2C as the authentication provider. Login follows the B2C _signupsignin_ user flow.  

#### Logout  
The route '/logout' is configured in the _staticwebapp.config.json_ file. It is set to redirect to the logout URL assigned to the _signupsignin_ login user flow. The logout URL logs the user out of B2C, takes care of their id token (so the user can't revalidate without signing in again), then redirects the user to the static web app's _/.auth/logout_ route.  

#### Password reset
The user simply clicks 'Forgot password' on the login screen then follows steps to reset or change password.

#### About authentication
*OAuth 2.0:* provides secure delegated access. An app can take actions or access resources from a server on behalf of the user, without them having to share their credentials. It does this by allowing the identity provider (IdP) to issue tokens to third-party applications with the user’s approval.  
*OpenID Connect:* is built on the OAuth 2.0 protocol and uses an additional JSON Web Token (JWT), called an ID token, for scopes and endpoint discovery. It is specifically focused on user authentication and is widely used to enable user logins on consumer websites and mobile apps. IdPs use this so that users can sign in to the IdP, and then access other websites and apps without having to log in or share their sign-in information. 

## Staging environments
1. Create a new branch
2. Make changes and commit to branch
3. Open a pull request on GitHub (Pull Requests > Compare & pull request > Create pull request)
    - A pull request is essentially a way of saying to the merge master "please pull my changes into main".
4. GitHub deployment workflow will now auto-run and auto-deploy to a pre-prod env.
5. GitHub bot will add a comment to the pull request with URL for pre-prod env.
6. Click on the link and manually check the URL to inspect changes.
7. Once satisfied click on Merge pull request (under Pull Requests tab same as earlier).
8. Delete the unneeded branch.

## Routing
In order to make use of Vue Router we use `to=""` in Bootstrap-Vue HTML components rather than `href=""`. This ensures that the `beforeEach()` and `afterEach()` functions in main.js are run correctly.  

## Cosmos DB
The web app is linked to a Cosmos DB that stores data uploaded from the form on the home page. New users are added with id = their Azure AD B2C id. This is because the Azure AD id is visible on the frontend anyway via a ping to /.auth/me.   
For reference when comparing Cosmos DB concepts to standard db concepts:  
- Database == Database
- Container == Table
- Partition + ID == Primary Key
- Item == Row
Enforce unique keys per partition and unique partitions.
