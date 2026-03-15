import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

const NAVY = '#1C2B4A'
const GOLD = '#C9A84C'
const LIGHT = '#F7F8FA'
const TEXT = '#1A1A2E'
const MUTED = '#6B7280'

const API_URL = '/api/generate'
const PDF_API_URL = import.meta.env.VITE_PDF_API_URL || 'https://decisio-pro-backend.up.railway.app'

const STEPS = ['Identification', 'Finances', 'Probleme', 'Objectifs', 'Qualification']

const PROMPT_V3 = `Tu es le consultant strategique senior de DECISIO AGENCY.

Tu appliques deux methodologies combinees :
1. La Methode D3 proprietaire : Diagnostic - Decision - Deploiement
2. L'approche First Principles (Elon Musk) : deconstruction du probleme jusqu'a la racine

REGLE ABSOLUE : Pas de blabla. Chaque recommandation doit etre actionnable immediatement. Tu es direct, honnete, parfois brutal dans tes constats. Tu parles comme un mentor qui veut vraiment aider, pas comme un consultant qui veut plaire.

GENERE UN RAPPORT EN SUIVANT CETTE STRUCTURE EXACTE :

## SYNTHESE EXECUTIVE
- Le vrai probleme en 2 lignes
- La recommandation principale
- L'impact chiffre attendu
- La probabilite de succes

## QUICK WIN 48H
- 1 action concrete a faire AUJOURD'HUI
- Resultat attendu dans 48h
- Script exact / message exact si applicable

# PARTIE 1 - DIAGNOSTIC

## 1.1 ANALYSE FIRST PRINCIPLES - LES 5 POURQUOI
Pourquoi 1 : [probleme de surface]
Pourquoi 2 : [cause intermediaire]
Pourquoi 3 : [cause plus profonde]
Pourquoi 4 : [cause structurelle]
Pourquoi 5 : [CAUSE RACINE - Verite Fondamentale]

> Verite Fondamentale : [La phrase qui resume tout]

## 1.2 ANALYSE FINANCIERE
- Taux de marge actuel
- Revenu horaire reel
- Cout du probleme par mois et par an
- Seuil de rentabilite

## 1.3 ANALYSE CONCURRENTIELLE
| Concurrent | Forces | Faiblesses | Prix |
Positionnement actuel vs marche

## 1.4 DIAGNOSTIC SECTORIEL
Contexte specifique au secteur du client. Tendances. Menaces. Opportunites.

# PARTIE 2 - DECISION

## 2.1 LES 3 OPTIONS STRATEGIQUES

OPTION A - [Nom de l'option recommandee]
- Description
- ROI estime : X
- Difficulte : /10
- Probabilite de succes : X%
- Score : (ROI x 0.4) + (Probabilite x 0.4) - (Difficulte x 0.2) = /10

OPTION B - [Alternative]
(meme structure)

OPTION C - [Option a eviter - expliquer pourquoi c'est dangereux]
(meme structure)

## 2.2 RECOMMANDATION
Quelle option et pourquoi. Argumentation chiffree.

## 2.3 RISQUES
- Risque financier
- Risque operationnel
- Risque marche
- Plan de mitigation pour chaque risque

# PARTIE 3 - DEPLOIEMENT

## 3.1 PLAN SEMAINE 1 - JOUR PAR JOUR
Lundi : [action precise]
Mardi : [action precise]
Mercredi : [action precise]
Jeudi : [action precise]
Vendredi : [action precise]

## 3.2 OBJECTIFS CHIFFRES
- M+1 : [objectif chiffre]
- M+3 : [objectif chiffre]
- M+6 : [objectif chiffre]

## 3.3 TRESORERIE PREVISIONNELLE
| Periode | Actuel | Projete | Variation |

## 3.4 SEUILS STOP / PIVOT
- Si [condition] alors STOP
- Si [condition] alors PIVOTER vers [alternative]

## 3.5 LES 3 REGLES
Si j'etais a votre place, voici les 3 regles que je m'imposerais :
1. [Regle 1]
2. [Regle 2]
3. [Regle 3]

---
Rapport genere par DECISIO AGENCY - Methode D3 - contact@decisio.pro`

function renderMarkdown(text) {
  if (!text) return ''
  const lines = text.split('\\n')
  let html = ''
  let inList = false
  let listType = ''

  function flushList() {
    if (inList) {
      html += listType === 'ul' ? '</ul>' : '</ol>'
      inList = false
    }
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd()
    const trimmed = line.trim()

    if (!trimmed) {
      flushList()
      html += '<br/>'
      continue
    }

    if (trimmed === '---') {
      flushList()
      html += `<hr style="border:none;border-top:1px solid #E2E5EB;margin:16px 0"/>`
      continue
    }

    // H1
    if (/^#\s+/.test(trimmed)) {
      flushList()
      const t = trimmed.replace(/^#\s+/, '')
      html += `<h1 style="font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:${NAVY};margin:24px 0 12px;border-bottom:2px solid ${GOLD};padding-bottom:6px">${t}</h1>`
      continue
    }
    // H2
    if (/^##\s+/.test(trimmed)) {
      flushList()
      const t = trimmed.replace(/^##\s+/, '')
      html += `<h2 style="font-size:16px;font-weight:700;color:${NAVY};margin:20px 0 8px;padding:8px 12px;background:${LIGHT};border-left:4px solid ${GOLD}">${t}</h2>`
      continue
    }
    // H3
    if (/^###\s+/.test(trimmed)) {
      flushList()
      const t = trimmed.replace(/^###\s+/, '')
      html += `<h3 style="font-size:14px;font-weight:700;color:${NAVY};margin:16px 0 6px">${t}</h3>`
      continue
    }

    // Verite fondamentale
    if (/verite fondamentale/i.test(trimmed)) {
      flushList()
      const t = trimmed.replace(/.*verite fondamentale\s*:?\s*/i, '')
      html += `<div style="background:${NAVY};border-left:4px solid ${GOLD};padding:12px 16px;margin:12px 0;border-radius:4px"><div style="font-size:10px;font-weight:700;color:${GOLD};letter-spacing:0.1em;margin-bottom:4px">VERITE FONDAMENTALE</div><div style="font-size:14px;font-weight:600;font-style:italic;color:white">${t}</div></div>`
      continue
    }

    // Blockquote
    if (/^>/.test(trimmed)) {
      flushList()
      const t = trimmed.replace(/^>\s*/, '')
      html += `<blockquote style="background:${LIGHT};border-left:3px solid #2563A8;padding:8px 12px;margin:8px 0;font-style:italic;color:#333">${t}</blockquote>`
      continue
    }

    // Table
    if (/^\|/.test(trimmed)) {
      flushList()
      if (/^\|[-| :]+\|$/.test(trimmed)) continue
      const cells = trimmed.split('|').filter(c => c.trim())
      const isHeader = !html.includes('</table>') || html.lastIndexOf('</table>') < html.lastIndexOf('<table')
      const tag = 'td'
      html += '<table style="width:100%;border-collapse:collapse;margin:8px 0;font-size:13px"><tr>'
      cells.forEach(c => {
        html += `<${tag} style="padding:6px 10px;border:1px solid #E2E5EB;background:${LIGHT}">${c.trim()}</${tag}>`
      })
      html += '</tr></table>'
      continue
    }

    // Bullet list
    if (/^[-*]\s/.test(trimmed)) {
      if (!inList || listType !== 'ul') {
        flushList()
        html += '<ul style="padding-left:20px;margin:8px 0">'
        inList = true
        listType = 'ul'
      }
      const t = trimmed.replace(/^[-*]\s/, '')
      html += `<li style="margin-bottom:4px;font-size:14px">${boldify(t)}</li>`
      continue
    }

    // Numbered list
    if (/^\d+\.\s/.test(trimmed)) {
      if (!inList || listType !== 'ol') {
        flushList()
        html += '<ol style="padding-left:20px;margin:8px 0">'
        inList = true
        listType = 'ol'
      }
      const t = trimmed.replace(/^\d+\.\s/, '')
      html += `<li style="margin-bottom:4px;font-size:14px">${boldify(t)}</li>`
      continue
    }

    // OPTION A/B/C
    if (/^OPTION\s+[A-C]/i.test(trimmed)) {
      flushList()
      const letter = trimmed.match(/OPTION\s+([A-C])/i)?.[1] || ''
      const rest = trimmed.replace(/^OPTION\s+[A-C]\s*[-–]?\s*/i, '')
      const color = letter === 'A' ? '#C4621A' : letter === 'B' ? '#2563A8' : MUTED
      html += `<div style="display:flex;gap:10px;align-items:flex-start;background:${LIGHT};border-left:5px solid ${color};padding:12px;margin:8px 0;border-radius:4px"><div style="background:${color};color:white;font-weight:700;font-size:16px;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">${letter}</div><div style="font-weight:700;color:${NAVY};font-size:14px">${rest}</div></div>`
      continue
    }

    flushList()
    html += `<p style="margin:6px 0;font-size:14px;line-height:1.7">${boldify(trimmed)}</p>`
  }
  flushList()
  return html
}

function boldify(s) {
  return s
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
}

export default function AuditApp() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [report, setReport] = useState('')
  const [error, setError] = useState('')
  const progressRef = useRef(null)

  const [form, setForm] = useState({
    nom: '', entreprise: '', secteur: '', anciennete: '', equipe: '', decideur: 'Oui',
    ca: '', benefice: '', depense: '',
    probleme: '', duree: '', tentatives: '', echec: '',
    objectif: '', cout: '',
    budget: '', urgence: 'Immediat', concurrents: '', differenciation: '',
  })

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const field = (label, key, placeholder, multi = false) => (
    <div style={{ marginBottom: 16 }}>
      <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: NAVY, marginBottom: 4 }}>{label}</label>
      {multi ? (
        <textarea
          value={form[key]} onChange={e => set(key, e.target.value)}
          placeholder={placeholder}
          style={{ width: '100%', padding: 10, border: `1px solid #ddd`, borderRadius: 6, fontSize: 14, minHeight: 80, fontFamily: 'inherit', resize: 'vertical' }}
        />
      ) : (
        <input
          value={form[key]} onChange={e => set(key, e.target.value)}
          placeholder={placeholder}
          style={{ width: '100%', padding: 10, border: `1px solid #ddd`, borderRadius: 6, fontSize: 14, fontFamily: 'inherit' }}
        />
      )}
    </div>
  )

  const select = (label, key, options) => (
    <div style={{ marginBottom: 16 }}>
      <label style={{ display: 'block', fontSize: 13, fontWeight: 600, color: NAVY, marginBottom: 4 }}>{label}</label>
      <select
        value={form[key]} onChange={e => set(key, e.target.value)}
        style={{ width: '100%', padding: 10, border: `1px solid #ddd`, borderRadius: 6, fontSize: 14, fontFamily: 'inherit' }}
      >
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  )

  const steps = [
    <>
      {field('Nom / Prenom', 'nom', 'Thomas Mercier')}
      {field('Entreprise', 'entreprise', 'TM Plomberie')}
      {field('Secteur', 'secteur', 'Artisan plombier')}
      {field('Anciennete', 'anciennete', '4 ans')}
      {field('Taille equipe', 'equipe', 'Seul / 2 personnes / 5+')}
      {select('Seul decideur ?', 'decideur', ['Oui', 'Non'])}
    </>,
    <>
      {field('Chiffre d\'affaires mensuel', 'ca', '5 000 EUR')}
      {field('Benefice net mensuel', 'benefice', '2 200 EUR')}
      {field('Plus grosse depense', 'depense', 'Loyer 800 EUR/mois')}
    </>,
    <>
      {field('Quel est votre probleme principal ?', 'probleme', 'Decrivez votre situation...', true)}
      {field('Depuis combien de temps ?', 'duree', '2 ans')}
      {field('Qu\'avez-vous deja essaye ?', 'tentatives', 'J\'ai essaye de...', true)}
      {field('Pourquoi ca n\'a pas marche ?', 'echec', 'Parce que...', true)}
    </>,
    <>
      {field('Objectif dans 6 mois', 'objectif', 'Gagner 3500 EUR net en travaillant 45h', true)}
      {field('Combien ce probleme vous coute par mois ?', 'cout', '1 300 EUR/mois')}
    </>,
    <>
      {field('Budget disponible', 'budget', '500-1000 EUR')}
      {select('Urgence', 'urgence', ['Immediat', 'Dans 1 mois', 'Dans 3 mois', 'Pas de deadline'])}
      {field('Vos concurrents principaux', 'concurrents', '3 concurrents dans ma ville')}
      {field('Votre differenciation', 'differenciation', 'Ce qui vous rend unique...', true)}
    </>,
  ]

  async function generate() {
    setLoading(true)
    setError('')
    setProgress(0)

    progressRef.current = setInterval(() => {
      setProgress(p => p >= 90 ? 90 : p + Math.random() * 8)
    }, 500)

    const clientData = `
Nom: ${form.nom}
Entreprise: ${form.entreprise}
Secteur: ${form.secteur}
Anciennete: ${form.anciennete}
Equipe: ${form.equipe}
Decideur: ${form.decideur}
CA mensuel: ${form.ca}
Benefice net: ${form.benefice}
Depense principale: ${form.depense}
Probleme: ${form.probleme}
Duree: ${form.duree}
Tentatives: ${form.tentatives}
Echec: ${form.echec}
Objectif 6 mois: ${form.objectif}
Cout du probleme: ${form.cout}
Budget: ${form.budget}
Urgence: ${form.urgence}
Concurrents: ${form.concurrents}
Differenciation: ${form.differenciation}
`
    const fullPrompt = PROMPT_V3 + '\n\nDONNEES CLIENT :\n' + clientData

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 8000,
          messages: [{ role: 'user', content: fullPrompt }],
        }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.error?.message || `Erreur API: ${res.status}`)
      }

      const data = await res.json()
      const text = data.content?.[0]?.text || data.choices?.[0]?.message?.content || ''
      setReport(text)
      setProgress(100)
    } catch (e) {
      setError(e.message)
    } finally {
      clearInterval(progressRef.current)
      setLoading(false)
    }
  }

  async function downloadPdf() {
    try {
      const res = await fetch(`${PDF_API_URL}/generate-pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          report: report,
          nom: form.nom,
          secteur: form.secteur,
          mode: 'premium',
        }),
      })
      if (!res.ok) throw new Error('Erreur generation PDF')
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `DECISIO_Audit_${form.nom.replace(/\s/g, '_')}.pdf`
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      alert('Erreur: ' + e.message)
    }
  }

  // ==================== ECRAN RAPPORT ====================
  if (report) {
    return (
      <div style={{ fontFamily: "'Source Sans 3', Arial, sans-serif", background: LIGHT, minHeight: '100vh' }}>
        <div style={{
          background: NAVY, color: 'white', padding: '16px 32px',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        }}>
          <div style={{ fontFamily: "'Playfair Display', serif", fontSize: 20, fontWeight: 900 }}>DECISIO</div>
          <div style={{ display: 'flex', gap: 12 }}>
            <button onClick={downloadPdf} style={{
              background: GOLD, color: NAVY, border: 'none', padding: '8px 20px',
              fontSize: 13, fontWeight: 700, borderRadius: 6, cursor: 'pointer',
            }}>TELECHARGER PDF</button>
            <button onClick={() => { setReport(''); setStep(0) }} style={{
              background: 'transparent', color: 'white', border: `1px solid rgba(255,255,255,0.3)`,
              padding: '8px 20px', fontSize: 13, fontWeight: 600, borderRadius: 6, cursor: 'pointer',
            }}>NOUVEL AUDIT</button>
          </div>
        </div>
        <div style={{ maxWidth: 800, margin: '24px auto', padding: 32, background: 'white', borderRadius: 8 }}>
          <div dangerouslySetInnerHTML={{ __html: renderMarkdown(report) }} />
        </div>
      </div>
    )
  }

  // ==================== ECRAN FORMULAIRE ====================
  return (
    <div style={{ fontFamily: "'Source Sans 3', Arial, sans-serif", background: LIGHT, minHeight: '100vh' }}>
      <div style={{
        background: NAVY, color: 'white', padding: '16px 32px',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      }}>
        <div onClick={() => navigate('/')} style={{ fontFamily: "'Playfair Display', serif", fontSize: 20, fontWeight: 900, cursor: 'pointer' }}>DECISIO</div>
        <div style={{ fontSize: 12, color: GOLD, fontWeight: 600 }}>METHODE D3 - AUDIT STRATEGIQUE</div>
      </div>

      <div style={{ maxWidth: 600, margin: '32px auto', padding: 32, background: 'white', borderRadius: 8 }}>
        {/* Progress bar */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
          {STEPS.map((s, i) => (
            <div key={i} style={{ flex: 1, textAlign: 'center' }}>
              <div style={{
                height: 4, borderRadius: 2,
                background: i <= step ? NAVY : '#E2E5EB',
                marginBottom: 6, transition: 'background 0.3s',
              }} />
              <div style={{ fontSize: 10, fontWeight: i === step ? 700 : 400, color: i <= step ? NAVY : MUTED }}>{s}</div>
            </div>
          ))}
        </div>

        <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: 22, color: NAVY, marginBottom: 20 }}>
          {STEPS[step]}
        </h2>

        {steps[step]}

        {error && <div style={{ background: '#FEE', color: '#C00', padding: 12, borderRadius: 6, marginBottom: 16, fontSize: 13 }}>{error}</div>}

        {loading && (
          <div style={{ marginBottom: 16 }}>
            <div style={{ background: '#E2E5EB', height: 8, borderRadius: 4, overflow: 'hidden' }}>
              <div style={{ background: NAVY, height: '100%', width: `${progress}%`, transition: 'width 0.5s', borderRadius: 4 }} />
            </div>
            <div style={{ fontSize: 12, color: MUTED, marginTop: 6, textAlign: 'center' }}>
              Analyse en cours... {Math.round(progress)}%
            </div>
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 16 }}>
          {step > 0 ? (
            <button onClick={() => setStep(s => s - 1)} style={{
              background: 'transparent', color: NAVY, border: `1px solid ${NAVY}`,
              padding: '10px 24px', fontSize: 13, fontWeight: 600, borderRadius: 6, cursor: 'pointer',
            }}>Retour</button>
          ) : <div />}

          {step < STEPS.length - 1 ? (
            <button onClick={() => setStep(s => s + 1)} style={{
              background: NAVY, color: 'white', border: 'none',
              padding: '10px 24px', fontSize: 13, fontWeight: 700, borderRadius: 6, cursor: 'pointer',
            }}>Suivant</button>
          ) : (
            <button onClick={generate} disabled={loading} style={{
              background: GOLD, color: NAVY, border: 'none',
              padding: '10px 24px', fontSize: 13, fontWeight: 700, borderRadius: 6,
              cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.6 : 1,
            }}>
              {loading ? 'Generation...' : 'GENERER L\'AUDIT'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
