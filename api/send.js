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

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  const { SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_TO, MAIL_FROM } = process.env;
  if (!SMTP_HOST || !SMTP_USER || !SMTP_PASS || !MAIL_TO) return res.status(503).json({ ok: false, error: 'smtp-not-configured' });

  let data = req.body || {};
  if (typeof data === 'string') { try { data = JSON.parse(data); } catch (e) { data = {}; } }
  if (data.website) return res.status(200).json({ ok: true }); // pot de miel
  if (!data.nom || !(data.email || data.tel)) return res.status(400).json({ ok: false, error: 'missing-fields' });

  const entries = Object.keys(data).filter((k) => k !== 'website' && String(data[k]).length < 5000);
  const text = entries.map((k) => `${LABELS[k] || k} : ${data[k]}`).join('\n');
  const html = '<table cellpadding="6" style="font-family:Arial,sans-serif;font-size:14px">' +
    entries.map((k) => `<tr><td style="color:#555">${esc(LABELS[k] || k)}</td><td><b>${esc(data[k])}</b></td></tr>`).join('') + '</table>';

  const port = Number(SMTP_PORT || 465);
  const transporter = nodemailer.createTransport({ host: SMTP_HOST, port, secure: port === 465, auth: { user: SMTP_USER, pass: SMTP_PASS } });
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
    console.error(e);
    return res.status(502).json({ ok: false, error: 'send-failed' });
  }
};
