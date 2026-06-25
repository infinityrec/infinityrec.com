/* =========================================================
   translate.js — IPTV PRO v3.0
   Auto-detects visitor country via IP, translates key UI
   Supported: en, fr, es, ar, de, nl, pt, it
   ========================================================= */

(function () {
  'use strict';

  // Country → language code mapping
  var countryLang = {
    // French
    FR:'fr', BE:'fr', CH:'fr', LU:'fr', MC:'fr', SN:'fr', CI:'fr', ML:'fr', BF:'fr', NE:'fr',
    TG:'fr', BJ:'fr', GN:'fr', CD:'fr', CG:'fr', CM:'fr', CF:'fr', TD:'fr', GA:'fr', MG:'fr',
    DZ:'fr', MA:'fr', TN:'fr', HT:'fr',
    // Spanish
    ES:'es', MX:'es', CO:'es', AR:'es', PE:'es', VE:'es', CL:'es', EC:'es', GT:'es', CU:'es',
    BO:'es', DO:'es', HN:'es', PY:'es', SV:'es', NI:'es', CR:'es', PA:'es', UY:'es', GQ:'es',
    // Arabic
    SA:'ar', AE:'ar', EG:'ar', IQ:'ar', SY:'ar', JO:'ar', LB:'ar', KW:'ar', QA:'ar', BH:'ar',
    OM:'ar', YE:'ar', LY:'ar', SD:'ar', SO:'ar', MR:'ar', KM:'ar', DJ:'ar', PS:'ar',
    // German
    DE:'de', AT:'de', LI:'de',
    // Dutch
    NL:'nl', SR:'nl',
    // Portuguese
    PT:'pt', BR:'pt', AO:'pt', MZ:'pt', CV:'pt', GW:'pt', ST:'pt', TL:'pt',
    // Italian
    IT:'it', SM:'it', VA:'it',
    // Default English — all others
    US:'en', GB:'en', CA:'en', AU:'en', NZ:'en', IE:'en', ZA:'en', IN:'en', SG:'en', PH:'en'
  };

  // Translation dictionary — key phrases used in data-i18n attributes
  var dict = {
    en: {
      'nav.home': 'Home',
      'nav.started': 'Get Started',
      'nav.blog': 'Blog',
      'nav.guide': 'IPTV Guide',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Get Your Free 24H Trial',
      'hero.learn': '📖 Learn More',
      'hero.channels': 'Live Channels',
      'hero.customers': 'Happy Customers',
      'hero.uptime': 'Uptime Guarantee',
      'hero.years': 'In Business',
      'pricing.title': 'Choose Your Plan',
      'pricing.subtitle': 'All plans include the same features. Only the duration differs. 1 device per subscription.',
      'pricing.1month': '1 Month',
      'pricing.3months': '3 Months',
      'pricing.6months': '6 Months',
      'pricing.1year': '1 Year',
      'pricing.best': '🏆 Best Value',
      'pricing.subscribe': '💬 Subscribe via WhatsApp',
      'pricing.trial': '🚀 Start Free Trial',
      'pricing.device': '📱 1 Device Only per subscription',
      'features.title': 'Everything You Need in One IPTV Package',
      'btn.trial': 'Get Your Free 24H Trial',
      'btn.whatsapp': '💬 WhatsApp Us Now',
      'btn.subscribe': '📺 Subscribe Now',
      'faq.title': 'Frequently Asked Questions',
      'footer.rights': 'All rights reserved.',
      'footer.quicklinks': 'Quick Links',
      'footer.support': 'Support',
      'footer.legal': 'Legal',
      'popup.purchased': 'just purchased the',
      'popup.plan': 'Plan 🎉'
    },
    fr: {
      'nav.home': 'Accueil',
      'nav.started': 'Commencer',
      'nav.blog': 'Blog',
      'nav.guide': 'Guide IPTV',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Essai Gratuit 24H',
      'hero.learn': '📖 En savoir plus',
      'hero.channels': 'Chaînes en direct',
      'hero.customers': 'Clients satisfaits',
      'hero.uptime': 'Disponibilité garantie',
      'hero.years': "Années d'activité",
      'pricing.title': 'Choisissez votre forfait',
      'pricing.subtitle': 'Tous les forfaits incluent les mêmes fonctionnalités. Seule la durée diffère. 1 appareil par abonnement.',
      'pricing.1month': '1 Mois',
      'pricing.3months': '3 Mois',
      'pricing.6months': '6 Mois',
      'pricing.1year': '1 An',
      'pricing.best': '🏆 Meilleure offre',
      'pricing.subscribe': '💬 S\'abonner via WhatsApp',
      'pricing.trial': '🚀 Essai gratuit',
      'pricing.device': '📱 1 Appareil par abonnement',
      'features.title': 'Tout ce dont vous avez besoin',
      'btn.trial': 'Essai Gratuit 24H',
      'btn.whatsapp': '💬 Contactez-nous sur WhatsApp',
      'btn.subscribe': '📺 S\'abonner maintenant',
      'faq.title': 'Questions fréquentes',
      'footer.rights': 'Tous droits réservés.',
      'footer.quicklinks': 'Liens rapides',
      'footer.support': 'Support',
      'footer.legal': 'Légal',
      'popup.purchased': 'vient d\'acheter le forfait',
      'popup.plan': '🎉'
    },
    es: {
      'nav.home': 'Inicio',
      'nav.started': 'Comenzar',
      'nav.blog': 'Blog',
      'nav.guide': 'Guía IPTV',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Prueba Gratis 24H',
      'hero.learn': '📖 Saber más',
      'hero.channels': 'Canales en vivo',
      'hero.customers': 'Clientes satisfechos',
      'hero.uptime': 'Disponibilidad garantizada',
      'hero.years': 'Años de experiencia',
      'pricing.title': 'Elige tu plan',
      'pricing.subtitle': 'Todos los planes incluyen las mismas funciones. Solo difiere la duración. 1 dispositivo por suscripción.',
      'pricing.1month': '1 Mes',
      'pricing.3months': '3 Meses',
      'pricing.6months': '6 Meses',
      'pricing.1year': '1 Año',
      'pricing.best': '🏆 Mejor oferta',
      'pricing.subscribe': '💬 Suscribirse por WhatsApp',
      'pricing.trial': '🚀 Prueba gratuita',
      'pricing.device': '📱 1 Dispositivo por suscripción',
      'features.title': 'Todo lo que necesitas en un paquete IPTV',
      'btn.trial': 'Prueba Gratis 24H',
      'btn.whatsapp': '💬 Contáctenos por WhatsApp',
      'btn.subscribe': '📺 Suscribirse ahora',
      'faq.title': 'Preguntas frecuentes',
      'footer.rights': 'Todos los derechos reservados.',
      'footer.quicklinks': 'Enlaces rápidos',
      'footer.support': 'Soporte',
      'footer.legal': 'Legal',
      'popup.purchased': 'acaba de comprar el plan',
      'popup.plan': '🎉'
    },
    ar: {
      'nav.home': 'الرئيسية',
      'nav.started': 'ابدأ الآن',
      'nav.blog': 'المدونة',
      'nav.guide': 'دليل IPTV',
      'nav.whatsapp': '💬 واتساب',
      'hero.trial': '🚀 تجربة مجانية 24 ساعة',
      'hero.learn': '📖 اعرف المزيد',
      'hero.channels': 'قناة مباشرة',
      'hero.customers': 'عميل سعيد',
      'hero.uptime': 'ضمان الاستمرارية',
      'hero.years': 'سنوات خبرة',
      'pricing.title': 'اختر باقتك',
      'pricing.subtitle': 'جميع الباقات تشمل نفس المميزات. الفرق فقط في المدة. جهاز واحد لكل اشتراك.',
      'pricing.1month': 'شهر واحد',
      'pricing.3months': '3 أشهر',
      'pricing.6months': '6 أشهر',
      'pricing.1year': 'سنة كاملة',
      'pricing.best': '🏆 أفضل قيمة',
      'pricing.subscribe': '💬 اشترك عبر واتساب',
      'pricing.trial': '🚀 جرب مجاناً',
      'pricing.device': '📱 جهاز واحد فقط لكل اشتراك',
      'features.title': 'كل ما تحتاجه في باقة IPTV واحدة',
      'btn.trial': 'تجربة مجانية 24 ساعة',
      'btn.whatsapp': '💬 تواصل معنا عبر واتساب',
      'btn.subscribe': '📺 اشترك الآن',
      'faq.title': 'الأسئلة الشائعة',
      'footer.rights': 'جميع الحقوق محفوظة.',
      'footer.quicklinks': 'روابط سريعة',
      'footer.support': 'الدعم',
      'footer.legal': 'القانونية',
      'popup.purchased': 'اشترى للتو باقة',
      'popup.plan': '🎉'
    },
    de: {
      'nav.home': 'Startseite',
      'nav.started': 'Loslegen',
      'nav.blog': 'Blog',
      'nav.guide': 'IPTV-Leitfaden',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Kostenlose 24H-Testversion',
      'hero.learn': '📖 Mehr erfahren',
      'hero.channels': 'Live-Kanäle',
      'hero.customers': 'Zufriedene Kunden',
      'hero.uptime': 'Verfügbarkeitsgarantie',
      'hero.years': 'Jahre Erfahrung',
      'pricing.title': 'Wählen Sie Ihren Plan',
      'pricing.subtitle': 'Alle Pläne enthalten die gleichen Funktionen. Nur die Laufzeit unterscheidet sich. 1 Gerät pro Abonnement.',
      'pricing.1month': '1 Monat',
      'pricing.3months': '3 Monate',
      'pricing.6months': '6 Monate',
      'pricing.1year': '1 Jahr',
      'pricing.best': '🏆 Bestes Angebot',
      'pricing.subscribe': '💬 Via WhatsApp abonnieren',
      'pricing.trial': '🚀 Kostenlose Testversion',
      'pricing.device': '📱 1 Gerät pro Abonnement',
      'features.title': 'Alles in einem IPTV-Paket',
      'btn.trial': 'Kostenlose 24H-Testversion',
      'btn.whatsapp': '💬 WhatsApp kontaktieren',
      'btn.subscribe': '📺 Jetzt abonnieren',
      'faq.title': 'Häufig gestellte Fragen',
      'footer.rights': 'Alle Rechte vorbehalten.',
      'footer.quicklinks': 'Schnelllinks',
      'footer.support': 'Support',
      'footer.legal': 'Rechtliches',
      'popup.purchased': 'hat gerade den Plan gekauft',
      'popup.plan': '🎉'
    },
    nl: {
      'nav.home': 'Home',
      'nav.started': 'Aan de slag',
      'nav.blog': 'Blog',
      'nav.guide': 'IPTV Gids',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Gratis 24U Proefperiode',
      'hero.learn': '📖 Meer informatie',
      'hero.channels': 'Live kanalen',
      'hero.customers': 'Tevreden klanten',
      'hero.uptime': 'Uptime garantie',
      'hero.years': 'Jaar actief',
      'pricing.title': 'Kies uw abonnement',
      'pricing.subtitle': 'Alle abonnementen bevatten dezelfde functies. Alleen de duur verschilt. 1 apparaat per abonnement.',
      'pricing.1month': '1 Maand',
      'pricing.3months': '3 Maanden',
      'pricing.6months': '6 Maanden',
      'pricing.1year': '1 Jaar',
      'pricing.best': '🏆 Beste waarde',
      'pricing.subscribe': '💬 Abonneren via WhatsApp',
      'pricing.trial': '🚀 Gratis proefperiode',
      'pricing.device': '📱 1 Apparaat per abonnement',
      'features.title': 'Alles in één IPTV-pakket',
      'btn.trial': 'Gratis 24U Proefperiode',
      'btn.whatsapp': '💬 Contact via WhatsApp',
      'btn.subscribe': '📺 Nu abonneren',
      'faq.title': 'Veelgestelde vragen',
      'footer.rights': 'Alle rechten voorbehouden.',
      'footer.quicklinks': 'Snelle links',
      'footer.support': 'Ondersteuning',
      'footer.legal': 'Juridisch',
      'popup.purchased': 'heeft zojuist het plan aangeschaft',
      'popup.plan': '🎉'
    },
    pt: {
      'nav.home': 'Início',
      'nav.started': 'Começar',
      'nav.blog': 'Blog',
      'nav.guide': 'Guia IPTV',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Teste Grátis 24H',
      'hero.learn': '📖 Saber mais',
      'hero.channels': 'Canais ao vivo',
      'hero.customers': 'Clientes satisfeitos',
      'hero.uptime': 'Garantia de disponibilidade',
      'hero.years': 'Anos de experiência',
      'pricing.title': 'Escolha o seu plano',
      'pricing.subtitle': 'Todos os planos incluem os mesmos recursos. Apenas a duração é diferente. 1 dispositivo por assinatura.',
      'pricing.1month': '1 Mês',
      'pricing.3months': '3 Meses',
      'pricing.6months': '6 Meses',
      'pricing.1year': '1 Ano',
      'pricing.best': '🏆 Melhor valor',
      'pricing.subscribe': '💬 Assinar via WhatsApp',
      'pricing.trial': '🚀 Teste gratuito',
      'pricing.device': '📱 1 Dispositivo por assinatura',
      'features.title': 'Tudo o que precisa num pacote IPTV',
      'btn.trial': 'Teste Grátis 24H',
      'btn.whatsapp': '💬 Contacte-nos pelo WhatsApp',
      'btn.subscribe': '📺 Assinar agora',
      'faq.title': 'Perguntas frequentes',
      'footer.rights': 'Todos os direitos reservados.',
      'footer.quicklinks': 'Links rápidos',
      'footer.support': 'Suporte',
      'footer.legal': 'Legal',
      'popup.purchased': 'acabou de comprar o plano',
      'popup.plan': '🎉'
    },
    it: {
      'nav.home': 'Home',
      'nav.started': 'Inizia',
      'nav.blog': 'Blog',
      'nav.guide': 'Guida IPTV',
      'nav.whatsapp': '💬 WhatsApp',
      'hero.trial': '🚀 Prova Gratuita 24H',
      'hero.learn': '📖 Scopri di più',
      'hero.channels': 'Canali in diretta',
      'hero.customers': 'Clienti soddisfatti',
      'hero.uptime': 'Garanzia di disponibilità',
      'hero.years': 'Anni di attività',
      'pricing.title': 'Scegli il tuo piano',
      'pricing.subtitle': 'Tutti i piani includono le stesse funzionalità. Differisce solo la durata. 1 dispositivo per abbonamento.',
      'pricing.1month': '1 Mese',
      'pricing.3months': '3 Mesi',
      'pricing.6months': '6 Mesi',
      'pricing.1year': '1 Anno',
      'pricing.best': '🏆 Miglior valore',
      'pricing.subscribe': '💬 Abbonati via WhatsApp',
      'pricing.trial': '🚀 Prova gratuita',
      'pricing.device': '📱 1 Dispositivo per abbonamento',
      'features.title': 'Tutto in un unico pacchetto IPTV',
      'btn.trial': 'Prova Gratuita 24H',
      'btn.whatsapp': '💬 Contattaci su WhatsApp',
      'btn.subscribe': '📺 Abbonati ora',
      'faq.title': 'Domande frequenti',
      'footer.rights': 'Tutti i diritti riservati.',
      'footer.quicklinks': 'Link rapidi',
      'footer.support': 'Supporto',
      'footer.legal': 'Legale',
      'popup.purchased': 'ha appena acquistato il piano',
      'popup.plan': '🎉'
    }
  };

  function applyTranslations(lang) {
    if (lang === 'en' || !dict[lang]) return;
    var trans = dict[lang];
    // Apply to all data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (trans[key]) el.textContent = trans[key];
    });
    // RTL for Arabic
    if (lang === 'ar') {
      document.documentElement.setAttribute('dir', 'rtl');
      document.documentElement.setAttribute('lang', 'ar');
    }
    // Mark active language button
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
    });
  }

  function detectAndTranslate() {
    // Check for manually selected language first
    var manual = localStorage.getItem('iptv_lang');
    if (manual) { applyTranslations(manual); return; }

    // Detect by IP
    fetch('https://ipapi.co/json/', { method: 'GET', mode: 'cors' })
      .then(function (r) { return r.json(); })
      .catch(function () { return {}; })
      .then(function (data) {
        var country = (data && data.country_code) ? data.country_code.toUpperCase() : 'US';
        var lang = countryLang[country] || 'en';
        if (lang !== 'en') applyTranslations(lang);
      });
  }

  // Manual language selection buttons (added by build.py)
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var lang = btn.getAttribute('data-lang');
        localStorage.setItem('iptv_lang', lang);
        applyTranslations(lang);
        if (lang !== 'ar') {
          document.documentElement.removeAttribute('dir');
        }
      });
    });

    detectAndTranslate();
  });

  // Expose for popup translations
  window.iptvTrans = { dict: dict, apply: applyTranslations };

})();
