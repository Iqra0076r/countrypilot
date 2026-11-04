import {
  ArrowRight, ArrowUpRight, BadgeCheck, BookOpen, BriefcaseBusiness,
  Building2, CheckCircle2, ChevronDown, Compass, GraduationCap, HeartPulse,
  Landmark, Menu, Plane, Search, ShieldCheck, Sparkles, Wallet, Globe2
} from "lucide-react";

const categories = [
  { title: "Visas & immigration", desc: "Understand routes, eligibility and requirements.", icon: Plane, href: "/topics/" },
  { title: "Jobs abroad", desc: "Explore sponsored roles and work opportunities.", icon: BriefcaseBusiness, href: "/topics/" },
  { title: "Study overseas", desc: "Plan admissions, student visas and funding.", icon: GraduationCap, href: "/topics/" },
  { title: "Insurance", desc: "Understand health, travel and expat cover.", icon: HeartPulse, href: "/topics/" },
  { title: "Banking & money", desc: "Compare accounts, transfers and everyday costs.", icon: Wallet, href: "/topics/" },
  { title: "Moving & settling in", desc: "Prepare for housing, paperwork and a new start.", icon: Building2, href: "/topics/" },
];

const destinations = [
  { name: "United States", code: "US", detail: "Work, study & family routes", tone: "bg-[#e8f0fa]" },
  { name: "United Kingdom", code: "UK", detail: "Skilled Worker & student routes", tone: "bg-[#f3eaf2]" },
  { name: "Canada", code: "CA", detail: "Express Entry & provincial options", tone: "bg-[#fbece8]" },
  { name: "Australia", code: "AU", detail: "Skilled migration & study", tone: "bg-[#e9f2e9]" },
];

const guides = [
  { tag: "VISA GUIDE", title: "The documents to prepare before applying for a visa", desc: "A practical checklist to help you organise your application with fewer surprises.", time: "8 min read", color: "from-[#d9e9e3] to-[#b9d9cd]", icon: BookOpen },
  { tag: "MONEY & BANKING", title: "Understanding proof of funds for your next move", desc: "What financial evidence can mean across different visa pathways.", time: "10 min read", color: "from-[#f4e7d3] to-[#e8d1ac]", icon: Landmark },
  { tag: "INSURANCE", title: "How to think about health cover when moving abroad", desc: "Key questions to ask before choosing a policy in a new country.", time: "7 min read", color: "from-[#dce8f2] to-[#bed2e4]", icon: ShieldCheck },
];

export default function Home() {
  return (
    <main className="site-shell">
      <div className="bg-[#102f3d] text-white">
        <div className="container flex min-h-9 items-center justify-between gap-4 text-[11px] sm:text-xs">
          <span className="font-semibold tracking-wide text-white/90">Independent guidance for your next move</span>
          <span className="hidden items-center gap-2 text-white/70 sm:flex"><BadgeCheck size={14} /> Clear information. Better decisions.</span>
        </div>
      </div>

      <header className="relative z-20 border-b border-[#e7eeea] bg-white/90 backdrop-blur-xl">
        <div className="container flex h-[78px] items-center justify-between gap-6">
          <a href="/" className="flex items-center gap-2.5" aria-label="CountryPilot home">
            <span className="grid size-10 place-items-center rounded-[14px] bg-[#087e70] text-white shadow-lg shadow-emerald-900/10"><Compass size={22} strokeWidth={2.2} /></span>
            <span className="text-[23px] font-extrabold tracking-[-1.2px] text-[#142b3b]">Country<span className="text-[#087e70]">Pilot</span></span>
          </a>
          <nav className="hidden items-center gap-8 lg:flex" aria-label="Main navigation">
            <a className="nav-link" href="/topics/">Explore</a>
            <a className="nav-link" href="/topics/">Visas & immigration</a>
            <a className="nav-link" href="/topics/">Work & study</a>
            <a className="nav-link" href="/tools/">Tools</a>
            <a className="nav-link" href="/topics/">Resources</a>
          </nav>
          <div className="flex items-center gap-3">
            <a href="/topics/" className="hidden text-sm font-bold text-[#087e70] sm:inline-flex">Explore guides</a>
            <a href="/topics/" className="primary-btn !px-5 !py-3 !text-[13px]">Plan your move <ArrowRight size={15} /></a>
            <button className="grid size-10 place-items-center rounded-full border border-[#e3ece8] text-[#142b3b] lg:hidden" aria-label="Open navigation"><Menu size={20} /></button>
          </div>
        </div>
      </header>

      <section className="hero-bg relative">
        <div className="container grid items-center gap-12 py-16 sm:py-20 lg:grid-cols-[1.03fr_.97fr] lg:py-24">
          <div className="relative z-10">
            <span className="pill"><Sparkles size={14} /> Your next chapter starts here</span>
            <h1 className="mt-7 max-w-[650px] text-[clamp(2.8rem,6vw,5.25rem)] font-semibold leading-[1.02] tracking-[-.065em] text-[#142b3b]">
              Make your next move <span className="text-[#087e70]">with confidence.</span>
            </h1>
            <p className="mt-6 max-w-[540px] text-[17px] leading-8 text-[#5e707b] sm:text-[19px]">
              Clear, independent guidance for visas, jobs, study, insurance and life abroad — so you can make informed decisions at every step.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-4">
              <a href="/topics/" className="primary-btn">Explore your options <ArrowRight size={17} /></a>
              <a href="/tools/" className="inline-flex items-center gap-2 rounded-full px-3 py-3 text-sm font-bold text-[#315363] hover:text-[#087e70]">Browse planning tools <ArrowUpRight size={16} /></a>
            </div>
            <div className="mt-10 flex flex-wrap items-center gap-x-7 gap-y-3 border-t border-[#dce9e3] pt-6 text-[12px] font-semibold text-[#637581]">
              <span className="inline-flex items-center gap-2"><CheckCircle2 size={15} className="text-[#087e70]" /> Independent research</span>
              <span className="inline-flex items-center gap-2"><CheckCircle2 size={15} className="text-[#087e70]" /> Practical checklists</span>
              <span className="inline-flex items-center gap-2"><CheckCircle2 size={15} className="text-[#087e70]" /> Clear next steps</span>
            </div>
          </div>

          <div className="relative mx-auto w-full max-w-[540px]">
            <div className="destination-art relative min-h-[420px] overflow-hidden rounded-[34px] p-7 shadow-[0_28px_80px_rgba(26,83,68,.16)] sm:min-h-[470px] sm:p-9">
              <div className="absolute left-8 top-8 rounded-full border border-white/70 bg-white/75 px-4 py-2 text-[11px] font-extrabold uppercase tracking-[.13em] text-[#23675a] backdrop-blur">A world of possibilities</div>
              <div className="absolute inset-x-0 bottom-0 h-[64%] opacity-70">
                <svg viewBox="0 0 560 330" className="h-full w-full" fill="none" aria-hidden="true">
                  <path d="M-20 270 C80 190 120 230 205 158 C280 92 330 170 405 110 C470 58 520 92 590 22" stroke="#fff" strokeWidth="2" strokeDasharray="7 9" />
                  <path d="M-10 310 C80 255 150 286 230 215 C310 145 390 228 570 105" stroke="#fff" strokeWidth="1.5" opacity=".65" />
                  <circle cx="205" cy="158" r="7" fill="#fff"/><circle cx="405" cy="110" r="7" fill="#fff"/><circle cx="205" cy="158" r="17" stroke="#fff" opacity=".7"/><circle cx="405" cy="110" r="17" stroke="#fff" opacity=".7"/>
                </svg>
              </div>
              <div className="absolute bottom-8 left-7 right-7 grid grid-cols-2 gap-3 sm:bottom-9 sm:left-9 sm:right-9">
                <div className="rounded-2xl border border-white/70 bg-white/85 p-4 shadow-lg backdrop-blur-xl">
                  <span className="text-[10px] font-extrabold uppercase tracking-[.13em] text-[#71847d]">Your destination</span>
                  <div className="mt-2 flex items-center justify-between text-[14px] font-extrabold text-[#19394a]">Explore countries <Globe2 size={17} className="text-[#087e70]" /></div>
                </div>
                <div className="rounded-2xl border border-white/70 bg-white/85 p-4 shadow-lg backdrop-blur-xl">
                  <span className="text-[10px] font-extrabold uppercase tracking-[.13em] text-[#71847d]">Your next step</span>
                  <div className="mt-2 flex items-center justify-between text-[14px] font-extrabold text-[#19394a]">Find your pathway <ArrowUpRight size={17} className="text-[#087e70]" /></div>
                </div>
              </div>
              <div className="absolute right-7 top-[108px] grid size-[82px] place-items-center rounded-[25px] border border-white/70 bg-white/60 text-[#087e70] shadow-xl backdrop-blur-xl sm:right-10"><Plane size={34} strokeWidth={1.5} /></div>
              <div className="absolute bottom-[178px] left-8 rounded-full bg-[#fff7e8] px-4 py-2 text-[11px] font-extrabold text-[#8a632c] shadow-lg">Plan • Prepare • Go</div>
            </div>
            <div className="absolute -bottom-5 -left-5 hidden items-center gap-3 rounded-2xl border border-[#e4eee8] bg-white p-4 shadow-xl sm:flex">
              <span className="grid size-10 place-items-center rounded-xl bg-[#e8f5ef] text-[#087e70]"><ShieldCheck size={20}/></span>
              <span><strong className="block text-[13px] text-[#19394a]">Know before you go</strong><small className="text-[11px] text-[#72818a]">Make informed decisions</small></span>
            </div>
          </div>
        </div>
      </section>

      <section className="relative z-10 -mt-5">
        <div className="container">
          <div className="soft-card grid gap-5 p-5 sm:grid-cols-[1fr_auto] sm:items-center sm:p-7">
            <div><div className="eyebrow">Start with a destination</div><h2 className="mt-1 text-xl font-bold tracking-tight">Where are you thinking of going?</h2></div>
            <div className="flex flex-wrap gap-2">
              {destinations.map((d) => <a key={d.code} href="/topics/" className="flex min-w-[135px] items-center gap-2 rounded-xl border border-[#e6eeea] bg-[#fbfdfc] px-3 py-3 transition hover:border-[#a9d4c5] hover:bg-[#f1f8f4]"><span className={`grid size-8 place-items-center rounded-lg text-[10px] font-black text-[#345c58] ${d.tone}`}>{d.code}</span><span className="text-[12px] font-bold">{d.name}</span></a>)}
            </div>
          </div>
        </div>
      </section>

      <section className="container py-20 sm:py-24">
        <div className="flex flex-wrap items-end justify-between gap-5">
          <div><div className="eyebrow">Explore CountryPilot</div><h2 className="mt-3 text-3xl font-semibold tracking-[-.045em] sm:text-[42px]">Everything you need to move forward.</h2><p className="mt-3 max-w-[560px] text-[15px] leading-7 text-[#6a7b84]">From your first question to the details that make a move possible, find clear guidance in one place.</p></div>
          <a href="/topics/" className="text-link inline-flex items-center gap-2 text-sm">Explore all topics <ArrowRight size={16}/></a>
        </div>
        <div className="mt-9 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map(({title,desc,icon:Icon,href}) => <a href={href} key={title} className="soft-card category-card group p-6 sm:p-7"><span className="grid size-12 place-items-center rounded-[16px] bg-[#eaf5f0] text-[#087e70]"><Icon size={23} strokeWidth={1.8}/></span><div className="mt-6 flex items-center justify-between gap-3"><h3 className="text-[19px] font-bold tracking-tight">{title}</h3><ArrowUpRight size={18} className="text-[#8aa69b] transition group-hover:-translate-y-1 group-hover:translate-x-1 group-hover:text-[#087e70]"/></div><p className="mt-2 max-w-[290px] text-[13px] leading-6 text-[#71818a]">{desc}</p></a>)}
        </div>
      </section>

      <section className="bg-[#edf5f1] py-20 sm:py-24">
        <div className="container grid items-center gap-12 lg:grid-cols-[.8fr_1.2fr]">
          <div><div className="eyebrow">Popular destinations</div><h2 className="mt-3 text-3xl font-semibold leading-tight tracking-[-.045em] sm:text-[42px]">A clearer picture of what comes next.</h2><p className="mt-4 max-w-[420px] text-[15px] leading-7 text-[#657780]">Explore country-specific information and understand the routes, requirements and practical decisions involved.</p><a href="/topics/" className="primary-btn mt-7">Explore all destinations <ArrowRight size={16}/></a></div>
          <div className="grid gap-4 sm:grid-cols-2">
            {destinations.map((d,i) => <a href="/topics/" key={d.code} className="soft-card group flex items-center gap-4 p-5 transition hover:-translate-y-1 hover:shadow-lg"><span className={`grid size-[58px] shrink-0 place-items-center rounded-2xl text-sm font-black text-[#345c58] ${d.tone}`}>{d.code}</span><span className="min-w-0 flex-1"><strong className="block text-[16px]">{d.name}</strong><small className="mt-1 block text-[11px] leading-5 text-[#71818a]">{d.detail}</small></span><ArrowUpRight size={18} className="text-[#8ba69b] group-hover:text-[#087e70]"/></a>)}
          </div>
        </div>
      </section>

      <section className="container py-20 sm:py-24">
        <div className="flex flex-wrap items-end justify-between gap-5"><div><div className="eyebrow">Guides & insights</div><h2 className="mt-3 text-3xl font-semibold tracking-[-.045em] sm:text-[42px]">Good decisions start with good information.</h2></div><a href="/topics/" className="text-link inline-flex items-center gap-2 text-sm">Read all guides <ArrowRight size={16}/></a></div>
        <div className="mt-9 grid gap-5 md:grid-cols-3">
          {guides.map(({tag,title,desc,time,color,icon:Icon}) => <article key={title} className="soft-card guide-card group overflow-hidden"><div className={`relative grid h-[185px] place-items-center overflow-hidden bg-gradient-to-br ${color}`}><span className="grid size-[88px] place-items-center rounded-[27px] border border-white/60 bg-white/45 text-[#2d7666] shadow-lg backdrop-blur"><Icon size={39} strokeWidth={1.4}/></span><span className="absolute bottom-4 left-5 rounded-full bg-white/80 px-3 py-1.5 text-[9px] font-extrabold tracking-[.14em] text-[#356b5e]">{tag}</span></div><div className="p-6"><div className="text-[11px] font-semibold text-[#82918f]">{time}</div><h3 className="mt-3 text-[19px] font-bold leading-snug tracking-tight group-hover:text-[#087e70]">{title}</h3><p className="mt-3 text-[13px] leading-6 text-[#71818a]">{desc}</p><a href="/topics/" className="mt-5 inline-flex items-center gap-2 text-[13px] font-extrabold text-[#087e70]">Read guide <ArrowRight size={15}/></a></div></article>)}
        </div>
      </section>

      <section className="container pb-20 sm:pb-24">
        <div className="relative overflow-hidden rounded-[30px] bg-[#12394a] px-7 py-12 text-white sm:px-12 sm:py-16">
          <div className="absolute -right-20 -top-28 size-[360px] rounded-full border border-white/10"/><div className="absolute -right-5 -top-14 size-[230px] rounded-full border border-white/10"/>
          <div className="relative max-w-[650px]"><span className="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3 py-1.5 text-[11px] font-bold text-[#c4e8d9]"><Sparkles size={13}/> Take the next step</span><h2 className="mt-5 text-3xl font-semibold leading-tight tracking-[-.045em] sm:text-[42px]">Your next chapter deserves a good plan.</h2><p className="mt-4 max-w-[540px] text-[15px] leading-7 text-white/70">Explore practical guides and tools to help turn a big move into a series of clear next steps.</p><a href="/tools/" className="mt-7 inline-flex items-center gap-2 rounded-full bg-white px-6 py-3.5 text-sm font-extrabold text-[#12394a] transition hover:bg-[#dff2e9]">Explore planning tools <ArrowRight size={16}/></a></div>
        </div>
      </section>

      <footer className="border-t border-[#e3ece8] bg-white">
        <div className="container grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div><a href="/" className="text-[22px] font-extrabold tracking-[-1px]">Country<span className="text-[#087e70]">Pilot</span></a><p className="mt-3 max-w-[270px] text-[13px] leading-6 text-[#71818a]">Independent guidance for people planning a real move. Research clearly. Plan confidently.</p></div>
          <div><strong className="text-[13px]">Explore</strong><div className="mt-4 grid gap-3 text-[12px] text-[#71818a]"><a href="/topics/">Visa guides</a><a href="/topics/">Jobs abroad</a><a href="/topics/">Study abroad</a><a href="/topics/">Insurance</a></div></div>
          <div><strong className="text-[13px]">Plan</strong><div className="mt-4 grid gap-3 text-[12px] text-[#71818a]"><a href="/tools/">Planning tools</a><a href="/topics/">Country guides</a><a href="/topics/">Money & banking</a><a href="/topics/">Relocation</a></div></div>
          <div><strong className="text-[13px]">CountryPilot</strong><div className="mt-4 grid gap-3 text-[12px] text-[#71818a]"><a href="/about/">About us</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy policy</a><a href="/editorial-policy/">Editorial policy</a></div></div>
        </div>
        <div className="border-t border-[#edf1ee]"><div className="container flex flex-wrap justify-between gap-3 py-5 text-[11px] text-[#87958f]"><span>© {new Date().getFullYear()} CountryPilot. All rights reserved.</span><span>Independent information. Always verify requirements with official sources.</span></div></div>
      </footer>
    </main>
  );
}