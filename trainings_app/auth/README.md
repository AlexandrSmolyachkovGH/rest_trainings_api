### Generation of keys for JWT

In this project, we use **JWT (JSON Web Token) authentication** to protect sensitive client data.
To enhance security, we have chosen **RSA-based encoding and decoding** for JWT signing and verification.
Below are the commands to generate a **private** and **public** key:

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