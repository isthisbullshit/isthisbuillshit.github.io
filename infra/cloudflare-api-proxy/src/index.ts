const BACKEND_URL = "https://isthisbullshit-backend-385552504501.europe-west1.run.app/";

export default {
  async fetch(request: Request): Promise<Response> {
    const incomingUrl = new URL(request.url);
    const backendUrl = new URL(BACKEND_URL);

    // /api/foo -> /foo
    backendUrl.pathname = incomingUrl.pathname;
    backendUrl.search = incomingUrl.search;

    const headers = new Headers(request.headers);
    headers.set("Host", backendUrl.host);
    headers.set("X-Forwarded-Host", incomingUrl.host);
    headers.set("X-Forwarded-Proto", incomingUrl.protocol.replace(":", ""));

    return fetch(backendUrl.toString(), {
      method: request.method,
      headers,
      body: request.body,
      redirect: "manual",
    });
  },
};