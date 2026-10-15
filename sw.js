const CACHE_NAME = "xauusd-pwa-v9-2-1";
const SHELL_FILES = new Set(["", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "sw.js"]);

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    const base = self.registration.scope;
    await cache.addAll([base, new URL("manifest.webmanifest", base).href, new URL("icon-192.png", base).href, new URL("icon-512.png", base).href]);
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith("xauusd-pwa-") && k !== CACHE_NAME).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin) return;

  const scopePath = new URL(self.registration.scope).pathname;
  if (!url.pathname.startsWith(scopePath)) return;
  const relativePath = decodeURIComponent(url.pathname.slice(scopePath.length));
  // Never cache dynamic trading data: cache only the app shell allowlist below.
  if (!SHELL_FILES.has(relativePath) || url.search) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    try {
      const response = await fetch(request, { cache: "no-cache" });
      if (response.ok) await cache.put(request, response.clone());
      return response;
    } catch (error) {
      const cached = await cache.match(request);
      if (cached) return cached;
      const baseCached = await cache.match(self.registration.scope);
      return baseCached || Response.error();
    }
  })());
});
