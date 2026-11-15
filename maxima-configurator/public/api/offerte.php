<?php
/**
 * Klop Watersport — ontvangt offerte- en hulpaanvragen uit de Maxima configurator
 * en mailt deze naar de verkoop. Verwacht een JSON-POST (zie configurator.js → payload()).
 *
 * Elke geldige aanvraag wordt eerst bewaard in LEADS_FILE (één JSON-regel per aanvraag), daarna gemaild.
 * Mislukt het mailen, dan is de aanvraag dus niet kwijt; de verkoop vindt hem in dat bestand.
 * LEADS_FILE staat buiten public/ en mag niet via het web bereikbaar zijn.
 *
 * Antwoord: {"ok":true,"mailed":bool} of {"ok":false,"error":"..."} met passende HTTP-status.
 */
declare(strict_types=1);

const TO_EMAIL   = 'verkoop@klopwatersport.nl';
const FROM_EMAIL = 'noreply@klopwatersport.nl';
const RATE_LIMIT = 5;      // max. aanvragen per IP ...
const RATE_WINDOW = 3600;  // ... per uur
define('LEADS_FILE', getenv('MX_LEADS_FILE') ?: dirname(__DIR__, 2) . '/aanvragen/aanvragen.jsonl');

header('Content-Type: application/json; charset=utf-8');

function respond(int $status, array $body): never {
    http_response_code($status);
    echo json_encode($body, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(405, ['ok' => false, 'error' => 'Method not allowed']);
}

$raw = file_get_contents('php://input', false, null, 0, 64 * 1024);
$in = json_decode($raw ?: '', true);
if (!is_array($in)) {
    respond(400, ['ok' => false, 'error' => 'Ongeldige aanvraag']);
}

$c = is_array($in['contact'] ?? null) ? $in['contact'] : [];
$clean = static fn($v, int $max = 200): string => mb_substr(trim(preg_replace('/[\r\n\t]+/', ' ', (string)$v)), 0, $max);

// Honeypot: bots vullen dit veld; stil "succes" teruggeven.
if (!empty($c['website'])) {
    respond(200, ['ok' => true]);
}

$type = ($in['type'] ?? '') === 'help' ? 'help' : 'quote';
$email = $clean($c['email'] ?? '');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(422, ['ok' => false, 'error' => 'Vul een geldig e-mailadres in.']);
}
$required = $type === 'help' ? ['name', 'phone'] : ['firstname', 'lastname', 'phone', 'city'];
foreach ($required as $f) {
    if ($clean($c[$f] ?? '') === '') {
        respond(422, ['ok' => false, 'error' => 'Niet alle verplichte velden zijn ingevuld.']);
    }
}

// Eenvoudige rate limit per IP (bestand in tmp-dir).
$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$rlFile = sys_get_temp_dir() . '/klop-cfg-' . hash('sha256', $ip);
$hits = array_filter(
    is_file($rlFile) ? (array)json_decode((string)file_get_contents($rlFile), true) : [],
    static fn($t) => is_int($t) && $t > time() - RATE_WINDOW
);
if (count($hits) >= RATE_LIMIT) {
    respond(429, ['ok' => false, 'error' => 'Te veel aanvragen. Probeer het later opnieuw of bel ons.']);
}
$hits[] = time();
file_put_contents($rlFile, json_encode(array_values($hits)), LOCK_EX);

$eur = static fn($n): string => '€ ' . number_format((float)$n, 2, ',', '.');
$model = $clean($in['model'] ?? 'Onbekend model', 100);

$labels = [
    'name' => 'Naam', 'firstname' => 'Voornaam', 'lastname' => 'Achternaam', 'email' => 'E-mail',
    'phone' => 'Telefoon', 'street' => 'Straat', 'housenumber' => 'Huisnummer', 'zipcode' => 'Postcode',
    'city' => 'Plaats', 'country' => 'Land', 'remarks' => 'Opmerking',
];
$lines = [];
$lines[] = ($type === 'help' ? 'Hulpaanvraag configurator' : 'Offerteaanvraag') . " — {$model}";
$lines[] = str_repeat('=', 60);
foreach ($labels as $k => $label) {
    $v = $clean($c[$k] ?? '', $k === 'remarks' ? 2000 : 200);
    if ($v !== '') $lines[] = str_pad($label . ':', 14) . $v;
}
$lines[] = '';
if ($type === 'quote' && array_key_exists('complete', $in) && !$in['complete']) {
    $lines[] = 'LET OP: de samenstelling is nog niet compleet (niet alle verplichte keuzes zijn gemaakt).';
}
$lines[] = 'Configuratie';
$lines[] = str_repeat('-', 60);
$lines[] = str_pad('Basisprijs', 46) . $eur($in['basePrice'] ?? 0);
foreach ((array)($in['options'] ?? []) as $o) {
    if (!is_array($o)) continue;
    $lines[] = str_pad($clean($o['step'] ?? '', 40) . ': ' . $clean($o['name'] ?? ''), 46) . $eur($o['price'] ?? 0);
    // Originele Maxima-naam en -id, zodat de bestelling 1-op-1 bij Maxima in te voeren is.
    $mxName = $clean($o['maximaName'] ?? '');
    if ($mxName !== '' && $mxName !== $clean($o['name'] ?? '')) {
        $lines[] = '    Maxima: ' . $mxName . (isset($o['maximaId']) ? ' (#' . (int)$o['maximaId'] . ')' : '');
    }
}
foreach ((array)($in['fixedCosts'] ?? []) as $f) {
    if (!is_array($f)) continue;
    $lines[] = str_pad($clean($f['label'] ?? ''), 46) . $eur($f['price'] ?? 0);
}
$lines[] = str_repeat('-', 60);
$lines[] = str_pad('Totaal (indicatief)', 46) . $eur($in['total'] ?? 0);
$lines[] = '';
$url = $clean($in['configUrl'] ?? '', 2000);
if ($url !== '') $lines[] = "Configuratie openen: {$url}";

$subject = '=?UTF-8?B?' . base64_encode(($type === 'help' ? 'Hulpaanvraag' : 'Offerteaanvraag') . " {$model}") . '?=';
$headers = implode("\r\n", [
    'From: Klop configurator <' . FROM_EMAIL . '>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
]);

// 1. Bewaren, zodat een aanvraag nooit verloren gaat.
$lead = [
    'ontvangen' => date('c'),
    'type' => $type,
    'model' => $model,
    'contact' => array_map(static fn($v) => $clean($v, 2000), array_intersect_key($c, $labels)),
    'opties' => array_values(array_filter((array)($in['options'] ?? []), 'is_array')),
    'totaal' => (float)($in['total'] ?? 0),
    'compleet' => (bool)($in['complete'] ?? true),
    'link' => $url,
];
$dir = dirname(LEADS_FILE);
$stored = (is_dir($dir) || @mkdir($dir, 0750, true))
    && @file_put_contents(LEADS_FILE, json_encode($lead, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX) !== false;

// 2. Mailen naar de verkoop.
$mailed = @mail(TO_EMAIL, $subject, implode("\n", $lines), $headers);

if (!$stored && !$mailed) {
    respond(500, ['ok' => false, 'error' => 'Versturen mislukt.']);
}
if (!$mailed) {
    error_log('Maxima-configurator: aanvraag bewaard maar niet gemaild (' . LEADS_FILE . ')');
}
respond(200, ['ok' => true, 'mailed' => $mailed]);
