<?php
/**
 * Router voor de ingebouwde PHP-server: site + Maxima-configurator op één adres.
 *
 *   php -S localhost:8080 tools/dev-router.php      (vanuit de root van de repo)
 *
 *   /                                → de nieuwe site, op de Maxima-configurator
 *   /site/                           → de nieuwe site
 *   /maxima-configurator/public/     → de configurator los
 *   /maxima-configurator/aanvragen/  → afgeschermd (bewaarde aanvragen)
 *
 * Alleen voor lokaal testen; op de echte server regelt de webserver dit.
 */
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) ?: '/';

if ($path === '/' || $path === '/index.html') {
    header('Location: /site/#/stel-samen/maxima', true, 302);
    exit;
}
if (str_starts_with($path, '/maxima-configurator/aanvragen') || str_starts_with($path, '/.git')) {
    http_response_code(403);
    exit('Niet toegankelijk.');
}
return false; // statische bestanden en .php gewoon laten afhandelen
