export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname.startsWith("/api/")) {
      const backendUrl = new URL(request.url);
      backendUrl.hostname = "";
      backendUrl.protocol = "https:";
      backendUrl.pathname = url.pathname;

      return fetch(backendUrl, request);
    }

    return env.ASSETS.fetch(request);
  },
};