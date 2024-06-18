const cacheVersion = 'v2.0';
const filesToCache = [
  '/manifest.json',
  '/static/icons/icon_512.png',
  '/static/icons/icon_192.png',
  '/static/icons/icon_144.png', 
  '/static/icons/web-icon.svg', 
  '/static/icons/monochrome.svg',
  '/static/svgs/loading.svg', 
  '/static/svgs/success.svg', 
  '/static/svgs/warning.svg', 
  '/static/css/style.css',
  '/static/css/connection.css',
  '/static/css/form.css',
  '/static/css/table.css',
  '/',
  '/chart',
  'load_css'
];

self.addEventListener('install', event => {
  console.log('[ServiceWorker] Install');
  event.waitUntil(
    caches.open(cacheVersion)
    .then(cache => {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activate');
});

self.addEventListener('fetch', event => {
  console.log('[ServiceWorker] fetch', event.request);
  event.respondWith(
    caches.match(event.request)
    .then(response => response || fetch(event.request))
  );
});
