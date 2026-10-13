// Envoi des formulaires du site (rendez-vous, contact, candidature) par SMTP.
// Variables d'environnement à renseigner dans Vercel > Settings > Environment Variables :
//   SMTP_HOST, SMTP_PORT (465 ou 587), SMTP_USER, SMTP_PASS,
//   MAIL_TO (boîte qui reçoit, ex. mickael@mthiollierconseils.fr), MAIL_FROM (optionnel)
const nodemailer = require('nodemailer');

const LABELS = {
  form: 'Formulaire', nom: 'Nom', prenom: 'Prénom', tel: 'Téléphone', email: 'E-mail',
  objet: 'Objet', profil: 'Profil', creneau: 'Créneau souhaité', format: 'Format',
  message: 'Message', experience: 'Expérience', ville: 'Secteur', _page: 'Page', _date: 'Date'
};
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const env = (k) => (process.env[k] || '').trim();
const makeTransport = () => {
  const port = Number(env('SMTP_PORT') || 465);
  return nodemailer.createTransport({
    host: env('SMTP_HOST'), port, secure: port === 465, requireTLS: port !== 465,
    auth: { user: env('SMTP_USER'), pass: process.env.SMTP_PASS || '' },
    connectionTimeout: 10000, greetingTimeout: 10000, socketTimeout: 15000
  });
};

module.exports = async (req, res) => {
  const SMTP_HOST = env('SMTP_HOST'), SMTP_USER = env('SMTP_USER'), SMTP_PASS = process.env.SMTP_PASS || '', MAIL_TO = env('MAIL_TO'), MAIL_FROM = env('MAIL_FROM');
  const missing = ['SMTP_HOST', 'SMTP_USER', 'SMTP_PASS', 'MAIL_TO'].filter((k) => !(k === 'SMTP_PASS' ? SMTP_PASS : env(k)));

  // Diagnostic : https://www.mthiollierconseils.fr/api/send?check=1 (aucun secret n'est renvoyé)
  if (req.method === 'GET') {
    if (!req.query || !req.query.check) return res.status(405).json({ ok: false });
    if (missing.length) return res.status(200).json({ ok: false, step: 'variables', missing, hint: 'Ajouter les variables dans Vercel > Settings > Environment Variables (environnement Production), puis redéployer.' });
    try { await makeTransport().verify(); return res.status(200).json({ ok: true, step: 'smtp', host: SMTP_HOST, port: env('SMTP_PORT') || '465', user: SMTP_USER, to: MAIL_TO }); }
    catch (e) { return res.status(200).json({ ok: false, step: 'smtp', host: SMTP_HOST, port: env('SMTP_PORT') || '465', user: SMTP_USER, error: String(e && e.message || e).slice(0, 300) }); }
  }
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  if (missing.length) { console.error('SMTP non configuré, variables manquantes :', missing.join(', ')); return res.status(503).json({ ok: false, error: 'smtp-not-configured', missing }); }

  let data = req.body || {};
  if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { data = {}; } }
  if (data.website) return res.status(200).json({ ok: true }); // pot de miel
  if (!data.nom || !(data.email || data.tel)) return res.status(400).json({ ok: false, error: 'missing-fields' });

  const entries = Object.keys(data).filter((k) => k !== 'website' && String(data[k]).length < 5000);
  const text = entries.map((k) => `${LABELS[k] || k} : ${data[k]}`).join('\n');
  const html = '<table cellpadding="6" style="font-family:Arial,sans-serif;font-size:14px">' +
    entries.map((k) => `<tr><td style="color:#555">${esc(LABELS[k] || k)}</td><td><b>${esc(data[k])}</b></td></tr>`).join('') + '</table>';

  const transporter = makeTransport();
  try {
    await transporter.sendMail({
      from: MAIL_FROM || `"Site M. Thiollier Conseils" <${SMTP_USER}>`,
      to: MAIL_TO,
      replyTo: data.email || undefined,
      subject: `${data._subject || 'Demande via le site'} – ${String(data.nom).slice(0, 80)}`,
      text, html
    });
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Échec SMTP :', e && e.message);
    return res.status(502).json({ ok: false, error: 'send-failed' });
  }
};
