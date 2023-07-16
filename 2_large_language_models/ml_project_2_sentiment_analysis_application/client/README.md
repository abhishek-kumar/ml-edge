# Frontend Svelte Client

This is the code for the Svelte frontend.

This is JavaScript code that gets downloaded to the client (their browser), and gets executed there. In Svelte, there are multiple mechanisms for choosing what files stay on the server to be executed, and which ones are downloaded to the client.

To run this code, you just `cd` into the `client` directory, run:

```bash
npm install
```

And then you can run:

```bash
make frontend
```

This should spawn a client service running on `http://localhost:5173`.
