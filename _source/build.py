#!/usr/bin/env python3
"""Builds the Pauwi Na static site into ./site"""
import os, shutil, html

SITE = "https://pauwina.com"
OUT = os.path.join(os.path.dirname(__file__), "site")
SRC = os.path.join(os.path.dirname(__file__), "src")
CHECKED = "November 2026"

NAV = [
    ("chapter-1.html", "The guide", "guide"),
    ("checklist.html", "Am I ready?", "checklist"),
    ("carriers.html", "Carriers", "carriers"),
    ("ai-helper.html", "AI helper", "ai"),
    ("costs.html", "Costs", "costs"),
    ("glossary.html", "Glossary", "glossary"),
]

CHAPTERS = [
    ("chapter-1.html", "1", "Before you ship"),
    ("chapter-2.html", "2", "On the water"),
    ("chapter-3.html", "3", "The 60-day rule"),
    ("chapter-4.html", "4", "It's arrived in Manila"),
    ("chapter-5.html", "5", "Customs, by yourself"),
    ("chapter-6.html", "6", "Release &amp; delivery"),
]


def page(fname, title, desc, body, section=None, scripts=False):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if key == section else ""}>{label}</a>'
        for href, label, key in NAV
    )
    canonical = SITE + "/" + ("" if fname == "index.html" else fname)
    full_title = title if fname == "index.html" else f"{title} | Pauwi Na"
    js = '<script src="assets/app.js" defer></script>' if scripts else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pauwi Na">
<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<meta name="theme-color" content="#FFF8EE">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&amp;family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WL6CDM4P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
</script>
<link rel="stylesheet" href="assets/style.css">
{js}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/img/logo.svg" alt="" width="44" height="44"><span><b>Pauwi Na</b><small>The balikbayan container guide</small></span></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p class="bye">Ingat sa biyahe. Safe travels home.</p>
    <p><strong>Pauwi Na</strong> is a free guide written by families who've shipped their homes back to the Philippines. It isn't legal advice, and customs rules change. Always confirm with the Bureau of Customs.</p>
    <p>Sources: Customs Modernization and Tariff Act (RA 10863), CAO 06-2016, CMO 15-2017. <a href="glossary.html#links">Official links</a> · Last checked {CHECKED}.</p>
    <p><a href="index.html">Home</a> · <a href="chapter-1.html">The guide</a> · <a href="checklist.html">Am I ready?</a> · <a href="carriers.html">Carriers</a> · <a href="glossary.html">Glossary</a> · <a href="about.html">About &amp; contact</a> · <a href="about.html#privacy">Privacy</a></p>
  </div>
</footer>
</body>
</html>
"""


ILLUS = {
    "chapter-1.html": ("us-home.svg", "Movers loading a container outside a family home abroad"),
    "chapter-2.html": ("hero.svg", "A container ship crossing the ocean toward the Philippines"),
    "chapter-4.html": ("manila-port.svg", "A container ship unloading at the Manila port"),
    "chapter-6.html": ("new-home.svg", "A family unloading their container at their new home"),
}


def chapter(fname, num, eyebrow_title, h1, lead, body, prev, nxt, desc):
    if fname in ILLUS:
        src, alt = ILLUS[fname]
        body = f'    <img class="illus" src="assets/img/{src}" alt="{alt}" width="480" height="300" loading="lazy">\n' + body
    side = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{n} · {t}</a>'
        for h, n, t in CHAPTERS
    )
    pv = f'<a class="btn btn-ghost" href="{prev[0]}">← {prev[1]}</a>' if prev else "<span></span>"
    nx = f'<a class="btn btn-primary" href="{nxt[0]}">{nxt[1]} →</a>' if nxt else ""
    b = f"""<div class="wrap layout">
  <nav class="side" aria-label="Chapters"><p>The guide</p>{side}</nav>
  <article class="prose">
    <div class="stack" style="gap:12px">
      <p class="eyebrow">Chapter {num}</p>
      <h1>{h1}</h1>
      <p style="font-size:20px;color:var(--muted)">{lead}</p>
    </div>
{body}
    <div class="pager">{pv}{nx}</div>
  </article>
</div>"""
    return page(fname, f"Chapter {num}: {eyebrow_title}", desc, b, "guide")


PAGES = {}

# ---------------- HOME ----------------
PAGES["index.html"] = page("index.html", "Pauwi Na: the balikbayan container guide",
"A free, step-by-step guide for Filipino families shipping household goods home by container: the 60-day duty-free rule, customs, costs and carriers.",
open(os.path.join(SRC, "home_body.html"), encoding="utf-8").read(), None)

# ---------------- CHAPTER 1 ----------------
PAGES["chapter-1.html"] = chapter("chapter-1.html", "1", "Before you ship", "Before the truck comes",
"Most of the trouble at Manila customs starts right here, in your driveway. A few hours of paperwork now can save you weeks, and a lot of pesos, later.",
"""    <h2>Decide whose name goes on it</h2>
    <p>The person named as <strong>consignee</strong> on the bill of lading is the one who can clear the container. If someone in your family is a returning Filipino, put <em>their</em> name, exactly as it appears in their passport. Only they can claim the duty-free allowance.</p>

    <h2>Make the list customs actually wants</h2>
    <p>Movers' inventory forms are usually handwritten, and they never have prices. Customs wants every item, a plain description, and what it's worth <strong>today, used</strong>.</p>
    <div class="tbl-wrap"><table class="tbl">
      <thead><tr><th scope="col" class="bad">Not like this</th><th scope="col" class="ok">Like this</th></tr></thead>
      <tbody>
        <tr><td>Paintings (2)</td><td>Framed prints, reproductions (2) · ₱1,000</td></tr>
        <tr><td>TVs (2)</td><td>Used 55-inch TV, 2019 (1) · ₱8,000</td></tr>
        <tr><td>Couch</td><td>Used 3-seat fabric couch (1) · ₱6,000</td></tr>
      </tbody>
    </table></div>
    <p class="muted" style="font-size:15px">Values above are examples only. Use what your own items would sell for, used, today. The <a href="ai-helper.html">AI helper</a> can turn a handwritten list into a typed one.</p>

    <h2>What to leave out</h2>
    <ul>
      <li>Anything in <strong>commercial quantity</strong>: ten of the same thing looks like stock for selling.</li>
      <li>Medicines beyond small personal amounts. Hand-carry those.</li>
      <li>Plants, seeds and soil, which need a Bureau of Plant Industry permit.</li>
      <li>Pets, which need a Bureau of Animal Industry permit and travel separately.</li>
      <li>A vehicle, unless it has its own bill of lading and import permit.</li>
    </ul>

    <h2>Questions to ask your forwarder</h2>
    <ol>
      <li>When does it actually <strong>sail</strong>, not just get picked up? From which port?</li>
      <li>Can I have an <strong>express or telex release</strong> instead of a paper original? Then nothing has to be couriered.</li>
      <li>Who is your agent in Manila, and who are their contacts?</li>
      <li>What's included, and what will I pay on arrival?</li>
      <li>Are you on DTI's list of accredited sea-freight forwarders? See <a href="carriers.html">Carriers</a>.</li>
    </ol>

    <div class="box box-blue stack" style="gap:8px">
      <h3 style="font-size:20px">Before you go, keep copies of</h3>
      <span>Your passport photo page · your US address proof · purchase receipts for big items · the signed mover's inventory · your forwarder's invoice and booking</span>
    </div>""",
None, ("chapter-2.html", "2 · On the water"),
"Before you ship household goods to the Philippines: choosing the consignee, making a valued inventory customs accepts, what not to pack, and what to ask your forwarder.")

# ---------------- CHAPTER 2 ----------------
PAGES["chapter-2.html"] = chapter("chapter-2.html", "2", "On the water", "Your life is somewhere on the ocean",
"For the next six to ten weeks there's nothing to lift. But there's one piece of paper you need to understand, and a few emails to watch for.",
"""    <h2>The bill of lading is your ticket</h2>
    <p>The <strong>bill of lading</strong> (B/L) is the receipt and ownership document for your container. Whoever holds it can claim the goods. It comes in two kinds:</p>
    <div class="grid" style="gap:16px">
      <div class="card stack" style="gap:8px;font-size:16px"><h3 style="font-size:20px">Original (paper)</h3><span>It has to be couriered to you, signed on the back, and handed to the shipping line before release. If it's late, your container waits, and storage charges pile up.</span></div>
      <div class="card stack" style="gap:8px;font-size:16px;border:1.5px solid var(--blue)"><h3 style="font-size:20px">Telex / express release</h3><span>Released electronically. No courier and no lost paper. You usually sign a short Letter of Undertaking instead. <strong>Ask for this.</strong></span></div>
    </div>
    <p class="muted" style="font-size:16px">If a forwarder booked your shipment, there may be two bills of lading: theirs (a "house" B/L) and the shipping line's. In Manila you'll deal with the one where you're named as consignee.</p>

    <h2>Track it yourself</h2>
    <p>Every container has a number: four letters and seven digits, like <code>MSBU2735321</code>. Type it into the shipping line's "track a shipment" page. ETAs slip often, so check every few days.</p>

    <h2>The arrival notice</h2>
    <p>About a week before the ship docks, the shipping line emails an <strong>arrival notice</strong>. It's the most useful page you'll get. Look for:</p>
    <ul>
      <li><strong>Estimated date of arrival:</strong> your clocks start from the actual unloading.</li>
      <li><strong>Port of discharge vs. terminal of pick-up:</strong> they can be different places, such as Manila North Harbour and MICT.</li>
      <li><strong>Consignee:</strong> it should be your name, spelled exactly as in your passport.</li>
      <li><strong>Type of document:</strong> "Original" means you need the paper B/L in hand.</li>
      <li><strong>The small print:</strong> how many free days you get, and when storage starts.</li>
    </ul>
    <div class="box box-blue" style="display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between">
      <span style="flex:1 1 340px">Not sure what yours says? Our AI prompt pulls out the dates and deadlines for you.</span>
      <a class="btn btn-primary" href="ai-helper.html#arrival">Read my arrival notice</a>
    </div>""",
("chapter-1.html", "1 · Before you ship"), ("chapter-3.html", "3 · The 60-day rule"),
"Understanding the bill of lading (original vs. telex release), tracking your container, and reading the shipping line's arrival notice.")

# ---------------- CHAPTER 3 ----------------
PAGES["chapter-3.html"] = chapter("chapter-3.html", "3", "The 60-day rule", "The 60-day rule nobody warns you about",
"You've packed the container and booked your flight. Here's the part that decides whether you pay nothing at customs, or tens of thousands of pesos.",
"""    <h2>What the rule says</h2>
    <p>If you're a Filipino coming home after living abroad, the law lets you bring your used household goods in <strong>duty- and tax-free</strong>, up to a limit. There's a catch: the goods have to arrive within <strong>60 days of the day you land</strong>.</p>
    <p>The clock starts with <em>your</em> arrival stamp, not the day the container ships.</p>
    <div class="tbl-wrap"><table class="tbl">
      <thead><tr><th scope="col">Time you lived abroad</th><th scope="col">Duty-free up to</th></tr></thead>
      <tbody>
        <tr><td>6 months to under 5 years</td><td>₱150,000</td></tr>
        <tr><td>5 to under 10 years</td><td>₱250,000</td></tr>
        <tr><td>10 years or more</td><td>₱350,000</td></tr>
      </tbody>
    </table></div>
    <p class="muted" style="font-size:16px">A dependent spouse and children count too. Anything over the limit is taxed. You apply through the DOF Revenue Office for a Tax Exemption Indorsement, and declare your goods on the PHED form.</p>

    <h2>How families miss it</h2>
    <p>It's rarely carelessness. Your goods get picked up, sit in a warehouse, get trucked to a port in another state, then wait for a ship. From the US East Coast, the ocean trip alone can take two months.</p>
    <div class="card stack" style="gap:14px">
      <p class="muted" style="margin:0;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase">A real timeline</p>
      <div class="timeline">
        <div><strong>Jul 3</strong><span>Family lands in Manila. The 60-day clock starts.</span></div>
        <div class="late"><strong>Sep 1</strong><span>The 60 days run out.</span></div>
        <div><strong>Sep 11</strong><span>The container finally sails from Miami, after a truck leg from North Carolina.</span></div>
        <div><strong>Nov 20</strong><span>The ship reaches Manila, 140 days after the family.</span></div>
      </div>
    </div>

    <h2>How to stay inside the window</h2>
    <p>Ship your container <strong>before you fly</strong>. Book pickup 6–8 weeks ahead of your flight, and ask the forwarder for the real sailing date, not just the pickup date. If the timing can't work, ask whether a West Coast port is faster.</p>

    <div class="box box-amber stack" id="missed">
      <h2 style="font-size:28px">What if I already missed it?</h2>
      <p>We'll be straight with you: the customs rules don't describe an extension or an appeal for late shipments. But they don't forbid asking either. Here's what to try, in order:</p>
      <ol>
        <li><strong>Ask in writing.</strong> Write to the DOF Revenue Office and the Bureau of Customs at your port, requesting the exemption anyway. Explain that the delay came from the shipping chain, not from you. <a href="ai-helper.html#letter" style="color:var(--amber-hd)">Draft it with AI</a></li>
        <li><strong>Attach proof.</strong> Booking confirmation, pickup receipt, warehouse and trucking records, the bill of lading dates, and your passport stamps.</li>
        <li><strong>If they say no, make the value fair.</strong> Duties are charged on what customs says your goods are worth. A clear, itemized list of <em>used</em> values matters more than anything else.</li>
        <li><strong>Check the assessment before you pay.</strong> If the values look wrong, ask for the computation in writing. You can file a formal protest, but the deadline is short, so ask customs for it on the spot.</li>
      </ol>
    </div>

    <p class="muted" style="font-size:15px">Where this comes from: CMTA (RA 10863) Section 800(f) · CAO 06-2016 · CMO 15-2017 (Annex A). <a href="glossary.html#links">Official links</a></p>""",
("chapter-2.html", "2 · On the water"), ("chapter-4.html", "4 · It's arrived in Manila"),
"The 60-day rule for returning Filipino residents: duty-free limits of ₱150,000 to ₱350,000, how families miss the window, and what to do if you already have.")

# ---------------- CHAPTER 4 ----------------
PAGES["chapter-4.html"] = chapter("chapter-4.html", "4", "It's arrived in Manila", "The ship is in. Now the clocks start.",
"Once your container is unloaded, three deadlines run at the same time. Miss them and you pay storage every day, or worse.",
"""    <div class="clocks">
      <div class="clock amber"><strong>A few days</strong><span>The shipping line's free time. One carrier's notice says that after <strong>3 days</strong> it can move your container to bonded storage, at your cost.</span></div>
      <div class="clock blue"><strong>15 days</strong><span>To file your customs declaration. You can ask for 15 more, but only <strong>before</strong> the first 15 run out.</span></div>
      <div class="clock red"><strong>30 days</strong><span>Uncollected goods can be treated as abandoned and sold. Don't let it get anywhere near this.</span></div>
    </div>

    <h2>Your first week, in order</h2>
    <ol>
      <li><strong>Email the shipping line's import desk.</strong> Ask for the actual unloading date, their invoice of local charges, your free days, and where to return the empty container. Contacts are on the <a href="carriers.html">Carriers</a> page.</li>
      <li><strong>Send their customer information sheet.</strong> It's written for companies. Fill it in as an individual: name, address, mobile, TIN. Mark PEZA "No".</li>
      <li><strong>Pay their charges and the container deposit.</strong> Hand over the original B/L, or sign the Letter of Undertaking for a telex release.</li>
      <li><strong>Get the delivery order.</strong> The terminal won't release your container without it.</li>
      <li><strong>Go to customs at the port where the container is</strong> (Chapter 5). For Manila, check whether it's MICT/MICP in Tondo or South Harbor.</li>
    </ol>

    <div class="box box-blue stack" style="gap:8px">
      <h3 style="font-size:20px">Arrives on a weekend?</h3>
      <span>The port runs every day, but customs and shipping-line offices may be closed. Spend the weekend on paperwork, and be at the window first thing Monday.</span>
    </div>
    <div class="box box-blue stack" style="gap:8px">
      <h3 style="font-size:20px">Need more time to file?</h3>
      <span>Ask customs for the 15-day extension in writing, before day 15. Our <a href="ai-helper.html#extension">AI prompt</a> drafts the request.</span>
    </div>""",
("chapter-3.html", "3 · The 60-day rule"), ("chapter-5.html", "5 · Customs, by yourself"),
"Your container arrived in Manila: the carrier's free days, the 15-day customs filing deadline, abandonment after 30 days, and your first-week checklist.")

# ---------------- CHAPTER 5 ----------------
PAGES["chapter-5.html"] = chapter("chapter-5.html", "5", "Customs, by yourself", "Yes, you can do customs yourself",
"The law doesn't require a broker. If you're the consignee, you can file. It takes patience and a folder of copies.",
"""    <h2>Your folder</h2>
    <div class="card folder">
      <label><input type="checkbox"> Bill of lading (original or telex)</label>
      <label><input type="checkbox"> Arrival notice and delivery order</label>
      <label><input type="checkbox"> Passports, with copies of the photo page and stamps</label>
      <label><input type="checkbox"> Itemized list with used values</label>
      <label><input type="checkbox"> PHED form (household effects declaration)</label>
      <label><input type="checkbox"> TIN</label>
      <label><input type="checkbox"> Proof you lived abroad (lease, utility bill)</label>
      <label><input type="checkbox"> Three photocopies of everything</label>
    </div>

    <h2>At the customs office</h2>
    <ol>
      <li><strong>Ask for the section that handles personal and household effects.</strong> It's usually the informal entry desk at that port.</li>
      <li><strong>Lodge your declaration and PHED.</strong> If you're asking for the returning-resident exemption, bring your Tax Exemption Indorsement request from the DOF Revenue Office, or ask how to file it there.</li>
      <li><strong>X-ray, and maybe an inspection.</strong> Be there in person. If they open the container, your clear list makes it quick.</li>
      <li><strong>Assessment.</strong> Customs sets a value and computes duty (about 15%) and VAT (12%). Ask for the computation in writing.</li>
      <li><strong>Pay</strong> at the cashier or the bank they name. Keep every official receipt.</li>
    </ol>

    <div class="box box-amber stack" style="gap:8px">
      <h3 style="font-size:20px">If the assessment looks wrong</h3>
      <span>Don't pay and walk away angry. Ask how they reached the value, show your used values and receipts, and ask about filing a protest. The deadline is short, so ask on the spot.</span>
    </div>

    <h2 id="broker">Do it yourself, or hire a broker?</h2>
    <p>The law doesn't require a broker if you're the consignee: you can file the declaration yourself. Here's how to decide.</p>
    <div class="tbl-wrap"><table class="tbl">
      <thead><tr><th scope="col" class="ok">Doing it yourself makes sense if…</th><th scope="col">A broker is worth it if…</th></tr></thead>
      <tbody>
        <tr><td>Your name is on the bill of lading as consignee</td><td>Someone else has to clear it for you, or you're still abroad</td></tr>
        <tr><td>You live near the port and can take several weekdays off</td><td>You can't take weekdays off, or you live far from the port</td></tr>
        <tr><td>It's ordinary used household goods</td><td>There's a vehicle, many of the same item, or anything needing a permit</td></tr>
        <tr><td>Your papers are complete: bill of lading, valued list, PHED, passports</td><td>Customs flags your shipment for a full inspection, or the assessment is disputed</td></tr>
        <tr><td>You're patient with queues and repeat visits</td><td>You're up against the free days or the 15-day deadline</td></tr>
      </tbody>
    </table></div>

    <h3>What a broker is, and what only they can do</h3>
    <p>A customs broker is a <strong>licensed professional</strong> regulated by the Professional Regulation Commission (PRC) under the Customs Brokers Act (RA 9280). When you hire one, the declaration is filed and signed under <em>their</em> license. Before you hire, ask for their PRC license number and check it. People who aren't licensed shouldn't be preparing or filing customs paperwork for a fee, whatever they call themselves.</p>

    <h3>What brokers should charge</h3>
    <p>There is an official schedule of brokerage fees (Customs Administrative Order 1-2001). Household goods usually go through informal entry, where the official brokerage fee is <strong>₱469.22 to ₱700 per entry</strong>. For formal entries, the fee rises with the shipment's dutiable value; above ₱200,000 it is ₱5,300 plus 0.375% of the amount over ₱200,000.</p>
    <p>In practice brokers often charge more than the schedule, and the schedule itself is being reviewed by the Bureau of Customs and the brokers' association. But it tells you something important: <strong>the broker's own fee should be a small part of your total.</strong> Most of a big quote is usually duties and VAT, port and shipping-line charges, storage, and trucking. Those are paid to someone else, with official receipts.</p>

    <div class="box box-amber stack" style="gap:8px">
      <h3 style="font-size:20px">Got a big "all-in" quote? Ask these five questions</h3>
      <ol>
        <li>How much of this is <strong>duties and VAT</strong>, and how did you compute it?</li>
        <li>How much is <strong>port, terminal and shipping-line charges</strong>?</li>
        <li>How much is <strong>storage or container late fees</strong>, and from what date?</li>
        <li>How much is <strong>trucking</strong>?</li>
        <li>What is <strong>your own professional fee</strong>, and what's your PRC license number?</li>
      </ol>
      <span>A good broker answers all five in writing and gives you official receipts for everything paid to the government, port and shipping line. If they won't, get another quote. Use our <a href="costs.html">duty estimator</a> to sanity-check the duties.</span>
    </div>

    <h3>If you do hire one</h3>
    <ul>
      <li>Hire for the <strong>filing only</strong> if you can handle the shipping line and trucking yourself. It's cheaper.</li>
      <li>Get the fee <strong>in writing before</strong> you hand over documents.</li>
      <li>Keep copies of everything you give them, and ask for copies of everything they file.</li>
      <li>Don't hand over cash for "facilitation" without an official receipt.</li>
    </ul>""",
("chapter-4.html", "4 · It's arrived"), ("chapter-6.html", "6 · Release &amp; delivery"),
"How to clear household goods through Philippine customs yourself: documents, informal entry, PHED, x-ray, assessment, and when a broker is worth it.")

# ---------------- CHAPTER 6 ----------------
PAGES["chapter-6.html"] = chapter("chapter-6.html", "6", "Release &amp; delivery", "The last mile home",
"Customs is paid. Now get the container out of the port, to your door, and the empty box back where it belongs.",
"""    <h2>At the terminal</h2>
    <ol>
      <li><strong>Pay port handling (arrastre) and any storage</strong> at the terminal's billing window.</li>
      <li><strong>Get the gate pass.</strong> You'll need the customs release, the delivery order and your receipts.</li>
      <li><strong>Check the container is ready</strong> before your truck goes. Otherwise you pay for a wasted trip.</li>
    </ol>

    <h2>Booking the truck</h2>
    <ul>
      <li>Use a trucker <strong>accredited to enter that terminal</strong>. Ask before you book.</li>
      <li>Check the street can fit a 20-foot container truck, and ask the barangay or subdivision about entry hours.</li>
      <li>Agree on how many hours you get to unload. Extra waiting time is often charged.</li>
      <li><strong>Going outside Metro Manila,</strong> to Palawan, Cebu, Mindanao? Plan an inter-island leg, or unpack in Manila and send the goods on.</li>
    </ul>

    <h2>Unloading day</h2>
    <p>Photograph the seal number <strong>before</strong> it's cut. Then photograph the doors opening and any damage. Check items off your list as they come out.</p>

    <h2>Return the empty, get your deposit</h2>
    <p>Return the container <strong>clean and empty</strong> to the depot the shipping line names, using their return reference number. Late returns are charged by the day and come out of your deposit.</p>

    <div class="box box-green stack" style="gap:8px">
      <h3>Maligayang pagbabalik. Welcome home.</h3>
      <span>Done? Help the next family. Share what you paid and how long each step took, and we'll add it to the guide.</span>
      <a href="about.html#share" style="font-weight:600">Share your experience</a>
    </div>""",
("chapter-5.html", "5 · Customs"), ("index.html", "Back to home"),
"Getting your container out of the Manila port: terminal charges, gate pass, booking a truck, unloading day, and getting your container deposit back.")

# ---------------- CHECKLIST ----------------
PAGES["checklist.html"] = page("checklist.html", "Am I ready? Balikbayan container checklist",
"Eight quick questions to see if your container shipment is ready for Philippine customs, and what to do next.",
"""<div class="wrap" style="padding:56px 24px 80px;display:flex;flex-direction:column;gap:36px">
  <div class="stack" style="gap:12px;max-width:720px">
    <p class="eyebrow">Am I ready?</p>
    <h1>Let's see where you stand.</h1>
    <p class="lead" style="max-width:none">Answer eight quick questions. We'll tell you what you already have, what's missing, and what to do next. Nothing you enter leaves your phone.</p>
  </div>
  <div class="two-col">
    <section class="main" aria-label="Questions">
      <div class="progress"><div class="bar"><i id="bar"></i></div><span id="count" style="font-size:14px;font-weight:600;color:var(--muted)">0 of 8 answered</span></div>
      <div id="questions" class="stack"><noscript><p>This checklist needs JavaScript turned on.</p></noscript></div>
    </section>
    <aside class="aside"><div class="card stack sticky" aria-live="polite">
      <h2 style="font-size:26px">Your next steps</h2>
      <div id="results" class="results"></div>
      <div style="border-top:1px solid var(--line);padding-top:16px;display:flex;flex-direction:column;gap:10px">
        <button type="button" id="reset" class="btn btn-outline" style="min-height:44px">Start over</button>
        <a href="chapter-1.html">Read the full guide</a>
      </div>
    </div></aside>
  </div>
  <p class="muted" style="margin:0;font-size:14px">This checklist is a guide, not legal advice. The Bureau of Customs makes the final call on every shipment.</p>
</div>""", "checklist", scripts=True)

# ---------------- COSTS ----------------
PAGES["costs.html"] = page("costs.html", "What it costs: Manila port charges and duty estimator",
"Typical Manila-side charges for a 20-foot container of household goods, plus a rough duty and VAT estimator for returning residents.",
"""<div class="wrap" style="padding:56px 24px 80px;display:flex;flex-direction:column;gap:44px">
  <div class="stack" style="gap:12px;max-width:720px">
    <p class="eyebrow">What it really costs</p>
    <h1>Where your money goes once the ship docks.</h1>
    <p class="lead" style="max-width:none">The freight you paid abroad is only part of it. These are the charges waiting in Manila for a 20-foot container of household goods.</p>
  </div>
  <div class="two-col">
    <div class="main"><div class="tbl-wrap"><table class="tbl">
      <thead><tr><th scope="col">Charge</th><th scope="col">Paid to</th><th scope="col">Typical (estimate)</th></tr></thead>
      <tbody>
        <tr><td>Local charges and delivery order</td><td class="muted">Shipping line</td><td>₱17,000–35,000</td></tr>
        <tr><td>Container deposit</td><td class="muted">Shipping line</td><td>Refundable, varies by line</td></tr>
        <tr><td>Port handling (arrastre) and wharfage</td><td class="muted">Terminal</td><td>₱6,000–15,000</td></tr>
        <tr><td>Customs fees, stamps, x-ray</td><td class="muted">Bureau of Customs</td><td>₱2,000–6,000</td></tr>
        <tr><td>Duties and VAT</td><td class="muted">Bureau of Customs</td><td><strong>Use the estimator</strong></td></tr>
        <tr><td>Trucking to your home</td><td class="muted">Trucker</td><td>₱9,000–25,000 (Metro Manila)</td></tr>
        <tr><td>Storage and late container return</td><td class="muted">Terminal / line</td><td style="color:var(--rust);font-weight:600">₱0 if you're fast</td></tr>
        <tr><td>Customs broker (optional)</td><td class="muted">Broker</td><td>Official rate ₱469–700 per informal entry; market rates higher. <a href="chapter-5.html#broker">What to expect</a></td></tr>
      </tbody>
    </table></div>
    <p class="muted" style="font-size:14px;margin:12px 0 0">Ranges are rough estimates from families' experience, last checked """ + CHECKED + """. Charges change. Ask your shipping line for its current invoice.</p></div>

    <aside class="aside"><div class="card est" aria-label="Duty estimator">
      <h2 style="font-size:26px">Duty estimator</h2>
      <div class="stack" style="gap:6px">
        <label for="val" style="font-weight:600;font-size:15px">What your goods are worth today (used)</label>
        <div class="big" id="valText">₱250,000</div>
        <input id="val" type="range" min="0" max="1000000" step="10000" value="250000">
      </div>
      <div class="stack" style="gap:8px">
        <span id="caplabel" style="font-weight:600;font-size:15px">Your duty-free allowance</span>
        <div class="caps" role="group" aria-labelledby="caplabel">
          <button type="button" class="opt" data-cap="0" aria-pressed="true">None</button>
          <button type="button" class="opt" data-cap="150000" aria-pressed="false">₱150,000</button>
          <button type="button" class="opt" data-cap="250000" aria-pressed="false">₱250,000</button>
          <button type="button" class="opt" data-cap="350000" aria-pressed="false">₱350,000</button>
        </div>
      </div>
      <div class="sum" aria-live="polite">
        <div><span>Taxable after allowance</span><strong id="taxable">₱250,000</strong></div>
        <div><span>Duty (~15%)</span><strong id="duty">₱37,500</strong></div>
        <div><span>VAT (12%)</span><strong id="vat">₱34,500</strong></div>
        <div class="total"><span style="font-weight:600">Rough total</span><strong id="total">₱72,000</strong></div>
      </div>
      <p class="muted" style="margin:0;font-size:13px;line-height:1.55">A rough guide only. Customs sets the value and the rates, and it can add freight and other charges to the taxable amount.</p>
    </div></aside>
  </div>
  <div class="box box-amber stack" style="gap:10px;max-width:860px">
    <h2 style="font-size:24px">Quoted a huge number? Ask for the breakdown.</h2>
    <p style="margin:0;font-size:17px">A ₱500,000 quote for a container of used furniture should raise questions. Ask what share is duties, storage, port fees, and the broker's own fee. Then compare it with this page.</p>
  </div>
</div>""", "costs", scripts=True)

# ---------------- CARRIERS ----------------
carriers = [
    ("MSC", "phl-import@msc.com · +63 2 8663 9000", "Yes (MSC Philippines local information page)"),
    ("Maersk", "ph.import@maersk.com · +63 2 8231 3126", "Yes (Maersk Philippines import page)"),
    ("Hapag-Lloyd", "See Hapag-Lloyd Philippines site", "Yes (PDF of local charges)"),
    ("ONE (Ocean Network Express)", "See ONE Philippines site", "Partly (Philippines site)"),
    ("CMA CGM / APL", "See CMA CGM Philippines site", "Not yet checked"),
    ("COSCO / OOCL", "See COSCO / OOCL Philippines site", "Not yet checked"),
    ("Evergreen", "See Evergreen Philippines site", "Not yet checked"),
    ("Yang Ming", "See Yang Ming Philippines site", "Not yet checked"),
    ("HMM", "See HMM Philippines site", "Not yet checked"),
    ("ZIM", "See ZIM Philippines site", "Not yet checked"),
    ("Wan Hai", "See Wan Hai Philippines site", "Not yet checked"),
    ("RCL", "See RCL Philippines site", "Yes (PDF of local charges)"),
]
rows = "".join(f'<tr><th scope="row">{n}</th><td class="muted">{c}</td><td class="muted">{ch}</td><td class="muted">No reviews yet</td></tr>' for n, c, ch in carriers)
PAGES["carriers.html"] = page("carriers.html", "Shipping lines and forwarders for balikbayan containers",
"Ocean carriers serving Manila, their import contacts, and how to tell whether a forwarder or shipping line is balikbayan-friendly.",
"""<div class="wrap" style="padding:56px 24px 80px;display:flex;flex-direction:column;gap:44px">
  <div class="stack" style="gap:12px;max-width:760px">
    <p class="eyebrow">Carriers &amp; forwarders</p>
    <h1>Who's carrying your container, and are they good to families?</h1>
    <p class="lead" style="max-width:none">Ratings come from families who've actually shipped, not from ads. No company pays to be listed here.</p>
  </div>
  <div class="grid">
    <div class="card stack" style="gap:8px"><span style="font-size:14px;font-weight:600;color:var(--blue)">Who you hire</span><h2 style="font-size:24px">The forwarder</h2><span class="muted">Picks up from your house, books the ship, and issues your paperwork. This is the choice that matters most, and the one you actually make.</span></div>
    <div class="card stack" style="gap:8px"><span style="font-size:14px;font-weight:600;color:var(--blue)">Whose ship it's on</span><h2 style="font-size:24px">The ocean carrier</h2><span class="muted">MSC, Maersk, CMA CGM and others. You meet them in Manila, when you pay their local charges and collect the delivery order.</span></div>
  </div>
  <section class="stack" style="gap:16px">
    <h2>What "balikbayan-friendly" means here</h2>
    <div class="grid-sm" style="font-size:16px">
      <div class="box box-blue" style="padding:16px 18px"><strong>Answers individuals</strong><br><span class="muted">Replies to a family's email within a day, not just to brokers</span></div>
      <div class="box box-blue" style="padding:16px 18px"><strong>Publishes its charges</strong><br><span class="muted">Manila import fees posted online, no surprises</span></div>
      <div class="box box-blue" style="padding:16px 18px"><strong>Express release</strong><br><span class="muted">No waiting on a couriered paper bill of lading</span></div>
      <div class="box box-blue" style="padding:16px 18px"><strong>Fair free days</strong><br><span class="muted">Enough time for a first-timer to clear customs</span></div>
      <div class="box box-blue" style="padding:16px 18px"><strong>Deposit back fast</strong><br><span class="muted">Container deposit refunded promptly and in full</span></div>
    </div>
  </section>
  <section class="stack" style="gap:16px">
    <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:12px"><h2>Ocean carriers serving Manila</h2><span class="muted" style="font-size:14px">Last checked """ + CHECKED + """</span></div>
    <div class="tbl-wrap"><table class="tbl" style="min-width:820px">
      <thead><tr><th scope="col">Carrier</th><th scope="col">Manila import contact</th><th scope="col">Import charges online</th><th scope="col">Family rating</th></tr></thead>
      <tbody>""" + rows + """</tbody>
    </table></div>
    <p class="muted" style="margin:0;font-size:14px">Contacts change. Always use the one printed on your own arrival notice.</p>
    <a class="btn btn-primary" href="about.html#share" style="align-self:flex-start">Rate the carrier and forwarder you used</a>
  </section>
  <div class="grid">
    <div class="card stack">
      <h2 style="font-size:24px">Before you hire a forwarder</h2>
      <ol style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:8px">
        <li>Check it's on DTI's list of accredited sea-freight forwarders.</li>
        <li>Ask which carrier and which US port, and the real sailing date.</li>
        <li>Ask who its Manila agent is, and get their contacts.</li>
        <li>Get a written quote that says what is <em>not</em> included at destination.</li>
        <li>Ask for express or telex release.</li>
      </ol>
    </div>
    <div class="box box-amber stack" style="gap:10px">
      <h2 style="font-size:24px">Rules coming on local charges</h2>
      <p style="margin:0">A <strong>draft</strong> order from DOF, DOTr and DTI (July 2026) would require container deposits to be refunded within 15 days of the empty container's return. It would also stop detention charges when the delay is the shipping line's fault. It isn't final yet; we'll update this when it is.</p>
    </div>
  </div>
</div>""", "carriers")

# ---------------- AI HELPER ----------------
prompts = [
    ("arrival", "Read my arrival notice", "Upload your arrival notice (PDF or photo) along with this prompt.",
"""I'm a returning resident shipping household goods to the Philippines by container. I've attached my shipping line's arrival notice.

1. Pull out: vessel name, ETA, port of discharge, pick-up terminal, bill of lading number, container number, consignee name, and whether the bill of lading is "Original" or telex/express release.
2. I arrived in the Philippines on [MY ARRIVAL DATE]. Work out my 60-day date for the returning-resident duty exemption, and tell me if this shipment is inside or outside it.
3. List my deadlines as dates: the carrier's free days (if shown), the 15-day customs filing deadline from unloading, and the 30-day abandonment risk.
4. Tell me the next 3 things I should do, in order.

Explain in plain English. If something isn't on the notice, say so instead of guessing."""),
    ("inventory", "Turn my mover's list into a valued inventory", "Attach a photo of your handwritten inventory.",
"""I've attached the household goods inventory from my movers. Turn it into a typed table for Philippine customs with columns: Item no. | Plain description (say "used" and the material/size, e.g. "used 3-seat fabric couch") | Quantity | Estimated used value in PHP.

Rules:
- Use realistic second-hand values for the Philippines, not what I paid new.
- Describe printed art as "framed prints, reproductions".
- Flag anything that could look like commercial quantity, or that may need a permit (plants, seeds, raw wood, medicines, pets, vehicles).
- If you can't read an item, write [UNCLEAR] instead of guessing.
At the end, total the values and list the items I should double-check."""),
    ("letter", "Draft my exemption request (late shipment)", "For when your goods arrived after the 60-day window.",
"""Help me write a polite, formal letter to the Department of Finance Revenue Office (copy to the Bureau of Customs, [PORT]) asking them to still grant the returning-resident tax and duty exemption under CMTA Section 800(f) and CAO 06-2016, even though my household goods arrived after the 60-day window.

My facts:
- Name: [NAME], Filipino citizen, lived in [COUNTRY] for [YEARS] years
- Arrived in the Philippines: [DATE]
- Goods picked up from my home: [DATE]; sailed from [PORT] on [DATE]; arrived Manila [DATE]
- Bill of lading no.: [B/L NO.]
- Reason for delay: [e.g. forwarder consolidation, trucking to another state's port, vessel schedule]

Keep it to one page. Explain that the delay was outside my control, list the documents I'm attaching, and ask for consideration. Don't invent facts. Leave blanks for anything I haven't given you."""),
    ("extension", "Request a 15-day filing extension", "Send before the first 15 days after unloading run out.",
"""Write a short, formal letter to the District Collector, Bureau of Customs, [PORT, e.g. Manila International Container Port], requesting a 15-day extension to file the goods declaration for my household goods shipment, as allowed under the CMTA.

Details: consignee [NAME]; bill of lading [B/L NO.]; container [CONTAINER NO.]; vessel [VESSEL/VOYAGE]; discharged on [DATE].
Reason: [e.g. waiting for the original bill of lading / DOF exemption indorsement].
Keep it under 200 words, with blanks for anything missing."""),
    ("quote", "Explain a quote or invoice", "Paste or attach a broker's quote or a shipping line invoice.",
"""I've attached a quote/invoice for clearing my household goods container in Manila. For each line:
1. Explain in plain English what it is and who it is paid to (shipping line, terminal, Bureau of Customs, broker, trucker).
2. Say whether it's normally a government charge, a pass-through cost, or the broker's own fee.
3. Flag anything that looks unusual, duplicated, or high, and what questions I should ask.
Then give me a short summary: how much is government duties/taxes vs. everything else."""),
]
pblocks = ""
for pid, title, hint, text in prompts:
    pblocks += f"""<div class="card prompt" id="{pid}">
      <h3>{title}</h3>
      <p class="muted" style="margin:0;font-size:15px">{hint}</p>
      <pre id="p-{pid}">{html.escape(text)}</pre>
      <button type="button" class="btn btn-primary" data-copy="p-{pid}">Copy prompt</button>
    </div>
"""
PAGES["ai-helper.html"] = page("ai-helper.html", "AI helper: ready-made prompts for ChatGPT and Claude",
"Copy-and-paste AI prompts to read your arrival notice, value your inventory, and draft customs letters for your balikbayan container.",
"""<div class="wrap" style="padding:56px 24px 80px;display:flex;flex-direction:column;gap:36px">
  <div class="stack" style="gap:12px;max-width:760px">
    <p class="eyebrow">AI helper</p>
    <h1>Let AI do the paperwork with you.</h1>
    <p class="lead" style="max-width:none">You don't need to know how to "prompt." Copy one of these into ChatGPT, Claude or Gemini, attach your document, and fill in the blanks in [BRACKETS].</p>
  </div>
  <div class="grid">
    <div class="box box-blue stack" style="gap:10px">
      <h2 style="font-size:22px">Pauwi Na in ChatGPT and Claude</h2>
      <p style="margin:0">Soon you'll be able to add Pauwi Na straight into ChatGPT (as a custom GPT) and Claude (as a skill), with this whole guide built in.</p>
      <span class="muted" style="font-size:15px">Coming soon.</span>
    </div>
    <div class="box box-amber stack" style="gap:10px">
      <h2 style="font-size:22px">Protect your personal details</h2>
      <p style="margin:0">Use your own AI account. Before uploading, cover your <strong>passport number</strong>, date of birth and bank details. The AI doesn't need them to help.</p>
    </div>
  </div>
  <div class="stack" style="gap:20px">""" + pblocks + """</div>
  <p class="muted" style="margin:0;font-size:14px">AI can make mistakes. Check every date and number against your actual documents, and confirm anything important with the Bureau of Customs.</p>
</div>""", "ai", scripts=True)

# ---------------- GLOSSARY ----------------
TERMS = [
    ("Abandonment", "When goods aren't claimed within the legal period after unloading, customs can treat them as abandoned and sell them. Avoid it by filing within 15 days."),
    ("Arrastre", "The port's charge for handling your container at the terminal: lifting it off the ship, moving it in the yard. Paid to the terminal operator."),
    ("Arrival notice", "The email or PDF the shipping line sends shortly before your ship docks, with the ETA, terminal, bill of lading number and release conditions."),
    ("Assessment", "Customs' calculation of the value of your goods and the duties and taxes you owe. Always ask for it in writing."),
    ("Balikbayan", "A Filipino returning home from abroad. Also used for the famous balikbayan boxes of gifts and personal goods."),
    ("Balikbayan box", "A carton of personal effects sent home by a Filipino abroad. Covered by its own duty-free rules, separate from a full household container."),
    ("Bill of lading (B/L)", "The shipping document that works as the receipt, the contract and the ownership title for your container. Whoever holds it can claim the goods."),
    ("BOC", "Bureau of Customs, the Philippine agency that clears imports and collects duties."),
    ("Bonded storage", "A customs-controlled warehouse where uncleared goods can be moved, at the importer's cost, if not collected in time."),
    ("CAO / CMO", "Customs Administrative Order / Customs Memorandum Order: the rules that put the customs law into practice. CAO 06-2016 and CMO 15-2017 cover returning residents."),
    ("CMTA", "Customs Modernization and Tariff Act (Republic Act 10863), the main Philippine customs law. Section 800(f) covers returning residents' household goods."),
    ("Consignee", "The person named on the bill of lading as receiving the goods. Only the consignee (or their authorized agent) can clear the container."),
    ("Container deposit", "Money the shipping line holds until you return the empty container. Refundable, minus any late-return charges."),
    ("Customs broker", "A PRC-licensed professional (RA 9280) who prepares and files customs declarations for others. Optional for household goods if you're the consignee."),
    ("Brokerage fee", "The customs broker's own professional fee, separate from duties, VAT, port charges and trucking. The official schedule (CAO 1-2001) sets ₱469.22 to ₱700 per informal entry."),
    ("Delivery order (DO)", "The shipping line's release paper. The terminal won't hand over your container without it."),
    ("Demurrage", "Daily charges when a full container stays at the port past its free days."),
    ("Detention", "Daily charges when you keep the shipping line's container outside the port too long before returning it empty."),
    ("DOF Revenue Office", "The Department of Finance office that issues the Tax Exemption Indorsement for returning residents' duty-free goods."),
    ("Dutiable value", "The value customs uses to calculate duties. It can include freight and insurance, not just the goods themselves."),
    ("Duties", "Import tax on goods. For used household goods, often around 15%, plus 12% VAT."),
    ("Express release / telex release", "An electronic release of the bill of lading, so no paper original has to be couriered. Usually needs a signed Letter of Undertaking."),
    ("FCL / LCL", "Full Container Load (the whole container is yours) / Less than Container Load (you share a container with others)."),
    ("Formal entry", "The full customs declaration process for commercial goods. Household goods usually go through informal entry instead."),
    ("Forwarder", "The company you hire to pick up your goods and book them on a ship. It may issue its own 'house' bill of lading."),
    ("Free time / free days", "The days the shipping line or terminal gives you before storage, demurrage or detention charges start."),
    ("Gate pass", "The terminal's permission for your container to leave the port."),
    ("House B/L", "A bill of lading issued by a forwarder, as opposed to the master B/L issued by the shipping line."),
    ("Informal entry", "The simpler customs process that covers personal and household effects not in commercial quantity."),
    ("Letter of Undertaking (LOU)", "A letter you sign for the shipping line accepting its terms, usually needed for a telex or express release."),
    ("MICP / MICT", "Manila International Container Port (the customs district) / Manila International Container Terminal (the terminal in Tondo)."),
    ("Notify party", "The person the shipping line contacts when the cargo arrives. Often the same as the consignee."),
    ("OFW", "Overseas Filipino Worker. Returning OFWs get extra duty-free privileges for home appliances."),
    ("PHED", "Personal and Household Effects Declaration, the customs form listing what's in your shipment, used for the returning-resident exemption."),
    ("Port of discharge", "The port where your container is unloaded, such as Manila North Harbour. It can differ from the terminal where you pick it up."),
    ("Returning resident", "A Filipino national returning after at least 6 months abroad, including a dependent spouse and children. Eligible for duty-free household goods up to a limit."),
    ("Seal number", "The number on the security seal locking your container. Photograph it before it's cut."),
    ("Tax Exemption Indorsement (TEI)", "The DOF document that supports your claim to the duty-free privilege. Formerly called a Tax Exemption Certificate."),
    ("TEU", "Twenty-foot Equivalent Unit: one 20-foot container. A 40-footer is 2 TEU."),
    ("TIN", "Taxpayer Identification Number from the BIR, needed for customs filings."),
    ("VAT", "Value-Added Tax: 12% in the Philippines, charged on imports on top of duties."),
    ("Wharfage", "A Philippine Ports Authority fee for use of the port, charged per container."),
]
TERMS.sort(key=lambda t: t[0].lower())
letters_used = sorted({t[0][0].upper() for t in TERMS})
letters = "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters_used)
gl = ""
seen = set()
for term, d in TERMS:
    L = term[0].upper()
    anchor = f' id="letter-{L}"' if L not in seen else ""
    seen.add(L)
    gl += f'<div class="term"{anchor}><dt>{html.escape(term)}</dt><dd>{html.escape(d)}</dd></div>'

LINKS = [
    ("Official rules", [
        ("Bureau of Customs", "https://customs.gov.ph/", "The Philippine customs agency"),
        ("Who is entitled to duty and tax-free privileges? (BOC FAQ)", "https://customs.gov.ph/?p=10263", "Returning residents, OFWs and others under CMTA Section 800"),
        ("Balikbayan box FAQ (BOC)", "https://customs.gov.ph/?p=40141", "What's allowed duty-free in balikbayan boxes"),
        ("CMO 15-2017: returning residents' household goods (PDF)", "https://customs.gov.ph/wp-content/uploads/2023/01/cmo-15-2017-Guidelines-on-the-Implementation-of-CAO-06-2016.pdf", "The 60-day rule, PHED form, exemption limits"),
        ("CAO 06-2016 (Department of Finance)", "https://www.dof.gov.ph/?p=18015", "The order on duty-exempt imports of returning residents and OFWs"),
        ("CMTA, Republic Act 10863 (PDF)", "https://customs.gov.ph/wp-content/uploads/2023/05/RA-10863-CMTA-Law.docx.pdf", "The full customs law"),
        ("Draft order on shipping-line charges, July 2026 (PDF)", "https://www.dof.gov.ph/wp-content/uploads/2026/07/JAO_Guidelines_3July2026.pdf", "Draft rules on container deposits and detention. Not final."),
    ]),
    ("Other agencies", [
        ("DTI Import Facilitation", "https://dti.gov.ph/negosyo/bis/import-facilitation", "Who can file a goods declaration, and import basics"),
        ("DTI balikbayan box FAQ", "https://dti.gov.ph/resources/faqs-tech-tools", "Forwarder accreditation and balikbayan box questions"),
        ("Bureau of Internal Revenue (TIN)", "https://www.bir.gov.ph/", "Get a Taxpayer Identification Number"),
        ("Bureau of Plant Industry", "https://www.buplant.da.gov.ph/", "Permits for plants, seeds and plant products"),
        ("Philippine Consulate General, Los Angeles: duty-free shipments", "https://losangelespcg.org/consular-services-2/notar1als/related-services/duty-free-shipment-of-personal-and-household-effects-into-the-philippines/", "Consulate guide to duty-free household effects"),
    ]),
    ("Shipping lines (Philippines)", [
        ("MSC Philippines: local information", "https://www.msc.com/en/local-information/asia-pacific/philippines", "Import charges, detention and demurrage, release procedure"),
        ("Maersk Philippines: import", "https://www.maersk.com/local-information/asia-pacific/philippines/import", "Import charges and contacts"),
        ("Hapag-Lloyd Philippines local charges (PDF)", "https://www.hapag-lloyd.com/content/dam/website/downloads/detention_demurrage/Philippines_local_charges_service_fees_Jun2026.pdf", "Published Philippine fees"),
    ]),
]
lk = ""
for group, items in LINKS:
    lis = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a><span>{html.escape(d)}</span></li>' for t, u, d in items)
    lk += f'<div class="stack" style="gap:12px"><h3>{group}</h3><ul class="links-list">{lis}</ul></div>'

PAGES["glossary.html"] = page("glossary.html", "Glossary of shipping and customs terms",
"Plain-English definitions of shipping and Philippine customs terms (arrastre, bill of lading, demurrage, PHED and more), plus official links.",
"""<div class="wrap" style="padding:56px 24px 80px;display:flex;flex-direction:column;gap:36px">
  <div class="stack" style="gap:12px;max-width:760px">
    <p class="eyebrow">Glossary &amp; links</p>
    <h1>What do all these words mean?</h1>
    <p class="lead" style="max-width:none">Shipping and customs come with their own language. Here it is in plain English, plus the official sources we use.</p>
  </div>
  <div class="stack" style="gap:14px">
    <label for="gsearch" style="font-weight:600">Search the glossary</label>
    <input id="gsearch" class="search" type="search" placeholder="e.g. demurrage">
    <nav class="letters" aria-label="Jump to letter">""" + letters + """</nav>
  </div>
  <dl class="glossary" style="margin:0">""" + gl + """</dl>
  <section id="links" class="stack" style="gap:24px;padding-top:24px">
    <h2>Official links</h2>
    <p class="muted" style="margin:0">Government pages move often. If a link breaks, tell us on the <a href="about.html">contact page</a>.</p>
    """ + lk + """
  </section>
</div>""", "glossary", scripts=True)

# ---------------- ABOUT ----------------
PAGES["about.html"] = page("about.html", "About Pauwi Na and contact",
"Who's behind Pauwi Na, the free balikbayan container guide, and how to share your shipping experience.",
"""<div class="wrap" style="padding:56px 24px 80px;display:flex;flex-direction:column;gap:32px;max-width:820px">
  <div class="stack" style="gap:12px">
    <p class="eyebrow">About</p>
    <h1>Written by a family who just did this.</h1>
    <p class="lead" style="max-width:none">We moved home from North Carolina in 2026. Our container arrived months after we did, we missed the 60-day window, and a broker quoted us ₱500,000. We built this guide so the next family knows what we didn't.</p>
  </div>
  <img class="illus" src="assets/img/family.svg" alt="Illustration of a family in front of their delivered container" width="480" height="360" loading="lazy">
  <div class="card stack">
    <h2 style="font-size:24px">Our promise</h2>
    <ul style="margin:0;padding-left:22px;display:flex;flex-direction:column;gap:8px">
      <li>It's free, and no company pays to be listed or rated.</li>
      <li>We link to the official rules, and say clearly when something is our estimate.</li>
      <li>We update the guide when the rules change.</li>
    </ul>
  </div>
  <div class="box box-green stack" id="share" style="gap:10px">
    <h2 style="font-size:24px;color:var(--green-ink)">Share your experience</h2>
    <p style="margin:0">Which forwarder and shipping line did you use? What did you pay in Manila, and how long did each step take? Your story helps the next family.</p>
    <a class="btn btn-dark" href="mailto:hello@pauwina.com?subject=My%20container%20experience" style="align-self:flex-start">Email us your story</a>
  </div>
  <div class="card stack" id="privacy" style="gap:10px">
    <h2 style="font-size:24px">Privacy</h2>
    <p style="margin:0">We use Google Analytics (through Google Tag Manager) to count visits and see which pages help people most. It uses cookies and collects things like the pages you view, your device type and your approximate location. We don't sell this data or use it for ads.</p>
    <p style="margin:0">Our checklist and duty estimator run only in your browser. Nothing you type into them is sent to us or to Google. The AI prompts are for you to use in your own ChatGPT or Claude account.</p>
    <p style="margin:0">You can block analytics cookies in your browser settings, or with Google's opt-out browser add-on. Questions? Email <a href="mailto:hello@pauwina.com">hello@pauwina.com</a>.</p>
  </div>
  <p class="muted" style="margin:0;font-size:15px">Contact: <a href="mailto:hello@pauwina.com">hello@pauwina.com</a></p>
</div>""", None)

# ---------------- 404 ----------------
PAGES["404.html"] = page("404.html", "Page not found", "Page not found.",
"""<div class="wrap stack" style="padding:96px 24px;gap:16px;max-width:640px">
  <p class="eyebrow">404</p><h1>This page got lost at sea.</h1>
  <p class="lead">Let's get you back on course.</p>
  <div class="btn-row"><a class="btn btn-primary" href="index.html">Go home</a><a class="btn btn-outline" href="chapter-1.html">Read the guide</a></div>
</div>""", None)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    for name, content in PAGES.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(content)
    shutil.copy(os.path.join(SRC, "style.css"), os.path.join(OUT, "assets", "style.css"))
    shutil.copy(os.path.join(SRC, "app.js"), os.path.join(OUT, "assets", "app.js"))
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "assets", "img"))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}/{'' if n == 'index.html' else n}</loc></url>" for n in PAGES if n != "404.html")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(OUT, ".htaccess"), "w") as f:
        f.write("ErrorDocument 404 /404.html\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [L,R=301]\nRewriteCond %{HTTP_HOST} ^www\\.(.*)$ [NC]\nRewriteRule ^(.*)$ https://%1/$1 [L,R=301]\n")
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    main()
