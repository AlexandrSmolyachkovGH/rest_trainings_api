### Generation of keys for JWT

In this project, we use **JWT (JSON Web Token) authentication** to protect sensitive client data.
To enhance security, we have chosen **RSA-based encoding and decoding** for JWT signing and verification.
Here are the commands and detailed instructions how to generate a **private** and **public** keys:

1. Create the certs package:
    - Inside the current `auth` package, create a new folder named `certs`.
2. Navigate to the certs package:
    - Open your terminal and switch to the created `certs` directory.
3. Generate the keys:
    - Run the following commands in the terminal to create the `.pem` files.

**Generate an RSA Private Key**
```shell
openssl genrsa -out jwt-private.pem 2048
```

**Extract the public key from the key pair**
```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

**Important: Key Security Best Practices:**
- Do not expose keys in your repository, logs, or public platforms.
- Add .pem files to .gitignore to prevent accidental commits.

###  How to Receive Tokens for Using the Application
Follow the steps below to obtain all the required tokens.

1. Log in and Get the Telegram Link:
   - Send a request to the `POST /jwt-auth/login/`;
   - In the response, you will receive a Telegram link.
2. Verify Your Account via Telegram:
   - Click on the telegram_link received in the response;
   - You will be redirected to Telegram, where you will receive a verification code.
3. Get a Refresh Token:
   - Send a request to `POST /jwt-auth/verification/`;
   - Pass the verification code obtained from Telegram;
   - In response, you will receive a refresh token.
4. Get an Access Token:
   - Send a request to the `POST /jwt-auth/get-access-token/`;
   - Pass your refresh token in the request;
   - In response, you will receive an access token.