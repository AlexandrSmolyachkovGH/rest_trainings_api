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