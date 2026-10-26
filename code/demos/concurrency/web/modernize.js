// modernize.js - Paste into browser console (Chrome/Edge)
// Uses built-in $ (querySelector) and $$ (querySelectorAll)

// 1) Remove floating banner
$('#floatBanner')?.remove();

// 2) Kill all intervals (banner animation, marquee, status scroller)
for (var i = 1; i < 10000; i++) clearInterval(i);

// 3) Inject modern stylesheet
var s = document.createElement('style');
s.textContent = `
body { background:#f5f5f7!important; color:#1d1d1f!important;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif!important;
  margin:0; padding:0; line-height:1.5!important; }
font { color:inherit!important; font:inherit!important; }
a { color:#06c!important; text-decoration:none!important; transition:color .15s!important; }
a:hover { color:#003d99!important; text-decoration:underline!important; }
table { border-collapse:collapse!important; border:none!important; width:auto!important; }
td { border:none!important; padding:8px 12px!important; color:inherit!important;
  background:none!important; vertical-align:top!important; font:inherit!important; }
.mod-nav td, .mod-hero td, .mod-announce td, .mod-footer td { padding:0!important; }
tr { background:none!important; }
hr { border:none!important; border-top:1px solid #e8e8ed!important; margin:20px 0!important; }
img { max-width:100%!important; }
input[type="text"] { border:1px solid #d1d1d6!important; border-radius:980px!important;
  padding:9px 16px!important; font-size:14px!important; color:#1d1d1f!important;
  background:#fff!important; transition:border-color .2s,box-shadow .2s!important;
  outline:none!important; }
input[type="text"]:focus { border-color:#06c!important; box-shadow:0 0 0 3px rgba(0,102,204,0.12)!important; }
input[type="button"] { background:#06c!important; color:#fff!important; border:none!important;
  border-radius:980px!important; padding:9px 22px!important; font-size:14px!important;
  font-weight:600!important; cursor:pointer!important; transition:background .15s,transform .1s!important; }
input[type="button"]:hover { background:#004db3!important; }
input[type="button"]:active { transform:scale(0.97)!important; }
s { color:#86868b!important; text-decoration-color:#d1d1d6!important; }

body > center { max-width:1100px; margin:0 auto; padding:0 24px; display:block; text-align:left; }

/* NAV */
.mod-nav { background:rgba(251,251,253,0.8)!important; backdrop-filter:saturate(180%) blur(20px)!important;
  -webkit-backdrop-filter:saturate(180%) blur(20px)!important;
  border-radius:14px!important; margin:20px 0!important; padding:6px!important;
  display:flex!important; box-shadow:0 1px 3px rgba(0,0,0,0.06)!important;
  border:1px solid rgba(0,0,0,0.04)!important; }
.mod-nav td { flex:1; text-align:center; padding:10px 0!important; }
.mod-nav a { font-size:13px!important; font-weight:500!important; color:#1d1d1f!important;
  letter-spacing:-0.01em!important; }
.mod-nav a:hover { color:#06c!important; text-decoration:none!important; }

/* HERO */
.mod-hero { text-align:center!important; padding:56px 24px 40px!important;
  background:linear-gradient(180deg,#fbfbfd 0%,#f5f5f7 100%)!important;
  border-radius:18px!important; margin-bottom:20px!important;
  border:1px solid rgba(0,0,0,0.03)!important; }
.mod-hero blink { animation:none!important; text-decoration:none!important;
  font-size:52px!important; font-weight:700!important; color:#1d1d1f!important;
  letter-spacing:-0.03em!important; }
.mod-hero br+blink, .mod-hero br~blink { font-size:52px!important; }
.mod-hero td { text-align:center!important; padding:0!important; }
.mod-hero b { display:inline!important; }

/* ANNOUNCEMENT */
.mod-announce { background:#1d1d1f!important; color:rgba(255,255,255,0.9)!important;
  text-align:center!important; padding:11px 16px!important;
  border-radius:10px!important; font-size:13px!important;
  font-weight:500!important; letter-spacing:-0.01em!important;
  margin-bottom:20px!important; }

/* 3-COL GRID */
.mod-main { display:grid!important; grid-template-columns:220px 1fr 220px!important;
  gap:28px!important; align-items:start!important; }
@media(max-width:900px){ .mod-main{grid-template-columns:1fr!important;} }

/* FEATURED PRODUCTS */
.mod-products { background:#fff!important; border-radius:18px!important; padding:28px!important;
  box-shadow:0 2px 12px rgba(0,0,0,0.05)!important; margin-bottom:24px!important;
  border:1px solid rgba(0,0,0,0.03)!important; }
.mod-products > tr > td { display:inline-block!important; width:calc(33.33% - 12px)!important;
  margin:0 6px 12px!important; vertical-align:top!important; text-align:center!important;
  background:#fafafa!important; border-radius:14px!important; padding:20px 12px!important;
  transition:transform .2s ease,box-shadow .2s ease!important; }
.mod-products > tr > td:hover { transform:translateY(-3px)!important;
  box-shadow:0 6px 20px rgba(0,0,0,0.08)!important; }
.mod-products table { background:linear-gradient(135deg,#e8e8ed,#d2d2d7)!important;
  border-radius:12px!important; width:72px!important; height:72px!important;
  margin:0 auto 12px!important; }
.mod-products table td { display:flex!important; align-items:center!important;
  justify-content:center!important; font-size:26px!important; }

/* CONTENT CARD (welcome, hot deals) */
.mod-card { background:#fff!important; border-radius:18px!important; padding:28px!important;
  box-shadow:0 2px 12px rgba(0,0,0,0.05)!important; margin-bottom:24px!important;
  border:1px solid rgba(0,0,0,0.03)!important; }

/* HOT DEALS TABLE */
.mod-table { width:100%!important; }
.mod-table tr:first-child td { font-size:11px!important; font-weight:600!important;
  color:#86868b!important; text-transform:uppercase!important; letter-spacing:0.06em!important;
  padding:8px 14px 12px!important; border-bottom:1.5px solid #e8e8ed!important; }
.mod-table td { font-size:14px!important; padding:14px!important;
  border-bottom:1px solid #f5f5f7!important; }
.mod-table tr:last-child td { border-bottom:none!important; }
.mod-table tr:hover td { background:rgba(0,102,204,0.02)!important; }

/* SIDEBAR */
.mod-sidebar { background:#fff!important; border-radius:14px!important; padding:18px!important;
  margin-bottom:14px!important; box-shadow:0 1px 4px rgba(0,0,0,0.04)!important;
  border:1px solid rgba(0,0,0,0.03)!important; }
.mod-sidebar td { font-size:13px!important; line-height:1.6!important; }
.mod-sidebar a { font-size:13px!important; font-weight:500!important; }

/* NEWSLETTER */
.mod-newsletter { text-align:center!important; background:linear-gradient(135deg,#06c 0%,#5856d6 100%)!important;
  border-radius:18px!important; padding:36px 28px!important; color:#fff!important;
  box-shadow:0 4px 16px rgba(0,102,204,0.2)!important; }
.mod-newsletter * { color:#fff!important; }
.mod-newsletter input[type="text"] { background:rgba(255,255,255,0.15)!important;
  border:1px solid rgba(255,255,255,0.25)!important; color:#fff!important;
  backdrop-filter:blur(8px)!important; }
.mod-newsletter input[type="text"]::placeholder { color:rgba(255,255,255,0.5)!important; }
.mod-newsletter input[type="button"] { background:#fff!important; color:#06c!important; }

/* FOOTER */
.mod-footer { text-align:center!important; padding:36px 0!important;
  color:#86868b!important; font-size:12px!important;
  border-top:1px solid #e8e8ed!important; margin-top:12px!important; }
.mod-footer a { color:#86868b!important; font-weight:500!important; }
.mod-footer a:hover { color:#06c!important; }

.mod-hide { display:none!important; }
`;
document.head.appendChild(s);

// 4) Stop blink
var bs = document.createElement('style');
bs.textContent = 'blink{animation:none!important;text-decoration:none!important}';
document.head.appendChild(bs);

// 5) Nav bar (2nd table)
$$('body>center>table')[1]?.classList.add('mod-nav');

// 6) Hero (1st table)
$$('body>center>table')[0]?.classList.add('mod-hero');

// 7) Marquee/announcement (3rd table)
$$('body>center>table')[2]?.classList.add('mod-announce');

// 8) Main 3-column grid (4th table)
$$('body>center>table')[3]?.classList.add('mod-main');

// 9) Clean table/td attributes
$$('table').forEach(t => {
  ['bgcolor','border','bordercolor','cellpadding','cellspacing'].forEach(a => t.removeAttribute(a));
});
$$('td').forEach(t => {
  ['bgcolor','bordercolor'].forEach(a => t.removeAttribute(a));
});

// 10) Unwrap <font> tags
$$('font').forEach(f => {
  while(f.firstChild) f.parentNode.insertBefore(f.firstChild, f);
  f.remove();
});

// 11) Classify inner tables
var mainTbl = $$('body>center>table')[3];
if(mainTbl) mainTbl.querySelectorAll('table').forEach(t => {
  var txt = (t.innerText||'').toLowerCase();
  if(/visitors|web ring|weather|\.midi|now playing|featured products/.test(txt))
    t.classList.add('mod-hide');
  if(/catalog|shopping cart|awards|^news$|links/.test(txt.split('\n')[0]))
    t.classList.add('mod-sidebar');
  if(txt.includes('mailing list'))
    t.classList.add('mod-newsletter');
  if(txt.includes('reg. price'))
    t.classList.add('mod-table');
});

// 11b) Mark the product row (the 3 td table after "featured products")
if(mainTbl) mainTbl.querySelectorAll('table').forEach(t => {
  if(t.classList.contains('mod-hide') && (t.innerText||'').toLowerCase().includes('featured products')) {
    var productTable = t.nextElementSibling;
    if(productTable && productTable.tagName === 'TABLE')
      productTable.classList.add('mod-products');
  }
});

// 12) Footer (last table)
$$('body>center>table').at(-1)?.classList.add('mod-footer');

// 13) Button text
$$('input[type="button"]').forEach(b => {
  if(b.value==='BUY NOW!') b.value='Add to Cart';
  if(b.value==='JOIN!') b.value='Subscribe';
});

// 14) Email placeholder
$$('input[type="text"]').forEach(i => {
  if(i.value==='your@email.com'){ i.value=''; i.placeholder='your@email.com'; }
});

// 15) Title
document.title = 'Shopper — Modern Online Store';

console.log('%c Modernized! Welcome to 2026. ', 'background:#06c;color:#fff;padding:4px 8px;border-radius:4px;font-weight:bold');
