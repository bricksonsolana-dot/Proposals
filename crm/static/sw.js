/**
 * Devox Sales — service worker
 * Handles push notifications from the server.
 */

self.addEventListener('install', (event) => {
  // Activate immediately on install — we don't precache anything yet.
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('push', (event) => {
  let payload = {};
  try {
    payload = event.data ? event.data.json() : {};
  } catch (e) {
    payload = { title: 'Devox Sales', body: event.data ? event.data.text() : '' };
  }
  const title = payload.title || 'Devox Sales';
  const options = {
    body: payload.body || '',
    icon: '/static/icon-192.png',
    badge: '/static/icon-192.png',
    tag: payload.tag || undefined,
    data: payload.data || { url: '/' },
    requireInteraction: false,
    silent: false,
  };
  if (payload.image) options.image = payload.image;
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const target = (event.notification.data && event.notification.data.url) || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((windowClients) => {
        // Focus an existing window if we have one
        for (const client of windowClients) {
          if (client.url.includes(self.registration.scope) && 'focus' in client) {
            client.postMessage({ type: 'navigate', url: target });
            return client.focus();
          }
        }
        // Otherwise open a new window
        if (self.clients.openWindow) {
          return self.clients.openWindow(target);
        }
      })
  );
});
