<?php
/**
 * Klop Watersport — ontvangt offerte- en hulpaanvragen uit de Maxima configurator
 * en mailt deze naar de verkoop. Verwacht een JSON-POST (zie configurator.js → payload()).
 *
 * Antwoord: {"ok":true} of {"ok":false,"error":"..."} met passende HTTP-status.
 */
declare(strict_types=1);

const TO_EMAIL   = 'verkoop@klopwatersport.nl';
const FROM_EMAIL = 'noreply@klopwatersport.nl';
const RATE_LIMIT = 5;      // max. aanvragen per IP ...
const RATE_WINDOW = 3600;  // ... per uur

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
$lines[] = 'Configuratie';
$lines[] = str_repeat('-', 60);
$lines[] = str_pad('Basisprijs', 46) . $eur($in['basePrice'] ?? 0);
foreach ((array)($in['options'] ?? []) as $o) {
    if (!is_array($o)) continue;
    $lines[] = str_pad($clean($o['step'] ?? '', 40) . ': ' . $clean($o['name'] ?? ''), 46) . $eur($o['price'] ?? 0);
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

if (!mail(TO_EMAIL, $subject, implode("\n", $lines), $headers)) {
    respond(500, ['ok' => false, 'error' => 'Versturen mislukt.']);
}
respond(200, ['ok' => true]);
