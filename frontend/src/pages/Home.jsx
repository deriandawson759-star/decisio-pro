import React from 'react'
import { useNavigate } from 'react-router-dom'

const NAVY = '#1C2B4A'
const GOLD = '#C9A84C'
const LIGHT = '#F7F8FA'
const TEXT = '#1A1A2E'
const MUTED = '#6B7280'

const globalStyle = {
  margin: 0,
  padding: 0,
  fontFamily: "'Source Sans 3', Arial, sans-serif",
  color: TEXT,
  background: 'white',
}

export default function Home() {
  const navigate = useNavigate()

  return (
    <div style={globalStyle}>
      {/* ==================== NAVBAR ==================== */}
      <nav style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '16px 40px', background: 'white',
        borderBottom: `1px solid #eee`, position: 'sticky', top: 0, zIndex: 100,
      }}>
        <div style={{ fontFamily: "'Playfair Display', Georgia, serif", fontSize: 22, fontWeight: 900, color: NAVY }}>
          DECISIO
        </div>
        <div style={{ display: 'flex', gap: 32, fontSize: 14, fontWeight: 600 }}>
          <a href="#methode" style={{ color: TEXT, textDecoration: 'none' }}>La Methode</a>
          <a href="#offres" style={{ color: TEXT, textDecoration: 'none' }}>Offres</a>
          <a href="#contact" style={{ color: TEXT, textDecoration: 'none' }}>Contact</a>
        </div>
      </nav>

      {/* ==================== HERO ==================== */}
      <section style={{
        background: NAVY, color: 'white',
        padding: '80px 40px', textAlign: 'center',
        minHeight: 500, display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
      }}>
        <div style={{
          fontSize: 10, fontWeight: 700, color: GOLD,
          letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: 24,
        }}>
          AUDIT STRATEGIQUE B2B
        </div>
        <h1 style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 48, fontWeight: 900, lineHeight: 1.1,
          maxWidth: 700, margin: '0 auto 24px',
        }}>
          Prenez de meilleures decisions. Plus vite.
        </h1>
        <p style={{
          fontSize: 18, fontWeight: 300, color: 'rgba(255,255,255,0.7)',
          maxWidth: 500, lineHeight: 1.6, marginBottom: 40,
        }}>
          Methode D3 — Diagnostic, Decision, Deploiement.
          Un audit strategique complet en 48 heures.
        </p>
        <button
          onClick={() => navigate('/audit')}
          style={{
            background: GOLD, color: NAVY, border: 'none',
            padding: '14px 36px', fontSize: 15, fontWeight: 700,
            borderRadius: 6, cursor: 'pointer', letterSpacing: '0.05em',
          }}
        >
          LANCER MON AUDIT
        </button>
      </section>

      {/* ==================== PROBLEME ==================== */}
      <section style={{ padding: '60px 40px', maxWidth: 900, margin: '0 auto' }}>
        <div style={{
          fontSize: 10, fontWeight: 700, color: GOLD,
          letterSpacing: '0.15em', textTransform: 'uppercase', marginBottom: 12,
        }}>
          LE PROBLEME
        </div>
        <h2 style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 30, fontWeight: 700, color: NAVY, marginBottom: 32,
        }}>
          Pourquoi vos decisions vous coutent de l'argent
        </h2>
        <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
          {[
            { titre: 'Decisions au feeling', desc: 'Vous decidez par intuition au lieu de vous baser sur des donnees. Chaque mauvaise decision coute du temps et de l\'argent.' },
            { titre: 'Pas de vision claire', desc: 'Vous travaillez dur mais sans plan strategique precis. Les efforts se dispersent et les resultats stagnent.' },
            { titre: 'Solitude du dirigeant', desc: 'Personne ne vous dit la verite sur votre business. Vous avez besoin d\'un regard exterieur objectif.' },
          ].map((p, i) => (
            <div key={i} style={{
              flex: '1 1 260px', background: LIGHT,
              padding: 24, borderRadius: 8,
              borderLeft: `4px solid ${GOLD}`,
            }}>
              <h3 style={{ fontSize: 16, fontWeight: 700, color: NAVY, marginBottom: 8 }}>{p.titre}</h3>
              <p style={{ fontSize: 14, color: MUTED, lineHeight: 1.6 }}>{p.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ==================== METHODE D3 ==================== */}
      <section id="methode" style={{ padding: '60px 40px', background: LIGHT }}>
        <div style={{ maxWidth: 900, margin: '0 auto' }}>
          <div style={{
            fontSize: 10, fontWeight: 700, color: GOLD,
            letterSpacing: '0.15em', textTransform: 'uppercase', marginBottom: 12,
          }}>
            NOTRE METHODE
          </div>
          <h2 style={{
            fontFamily: "'Playfair Display', Georgia, serif",
            fontSize: 30, fontWeight: 700, color: NAVY, marginBottom: 40,
          }}>
            La Methode D3 — Diagnostic, Decision, Deploiement
          </h2>
          <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
            {[
              { num: '01', titre: 'DIAGNOSTIC', color: '#C0392B', desc: 'Analyse First Principles. On deconstruit votre business jusqu\'a la racine avec les 5 Pourquoi. On identifie le vrai probleme — pas les symptomes.' },
              { num: '02', titre: 'DECISION', color: '#C4621A', desc: '3 options strategiques scorees objectivement. ROI, difficulte, probabilite de succes. Vous savez exactement quoi choisir et pourquoi.' },
              { num: '03', titre: 'DEPLOIEMENT', color: '#1A7A45', desc: 'Plan d\'action jour par jour. Quick Win 48h. Tresorerie previsionnelle M+1 et M+6. Vous passez a l\'action immediatement.' },
            ].map((step, i) => (
              <div key={i} style={{
                flex: '1 1 260px', background: 'white',
                padding: 28, borderRadius: 8,
                borderTop: `4px solid ${step.color}`,
              }}>
                <div style={{
                  width: 36, height: 36, borderRadius: '50%',
                  background: step.color, color: 'white',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 13, fontWeight: 700, marginBottom: 16,
                }}>{step.num}</div>
                <h3 style={{ fontSize: 16, fontWeight: 700, color: NAVY, marginBottom: 8, letterSpacing: '0.05em' }}>{step.titre}</h3>
                <p style={{ fontSize: 14, color: MUTED, lineHeight: 1.6 }}>{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ==================== OFFRES ==================== */}
      <section id="offres" style={{ padding: '60px 40px', maxWidth: 1000, margin: '0 auto' }}>
        <div style={{
          fontSize: 10, fontWeight: 700, color: GOLD,
          letterSpacing: '0.15em', textTransform: 'uppercase', marginBottom: 12, textAlign: 'center',
        }}>
          NOS OFFRES
        </div>
        <h2 style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 30, fontWeight: 700, color: NAVY, marginBottom: 40, textAlign: 'center',
        }}>
          Choisissez votre niveau d'accompagnement
        </h2>
        <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', justifyContent: 'center' }}>
          {[
            {
              nom: 'Audit Flash', prix: '490', desc: 'Diagnostic rapide + 1 probleme identifie + 3 leviers d\'action',
              items: ['Diagnostic decisionnel', '1 probleme principal', '3 leviers d\'action', 'Livraison 48h'],
              highlight: false,
            },
            {
              nom: 'Audit Premium', prix: '2 490', desc: 'Audit strategique complet avec plan d\'action detaille',
              items: ['Diagnostic complet + First Principles', '3 problemes racines minimum', 'Options scorees A/B/C', 'Tresorerie M+1 et M+6', 'Plan semaine jour par jour', 'Quick Win 48h', 'Posture "Si j\'etais a votre place"'],
              highlight: true,
            },
            {
              nom: 'Transformation', prix: '6 900', desc: 'Audit + accompagnement + implementation guidee',
              items: ['Tout l\'Audit Premium', 'Accompagnement 3 mois', 'Implementation guidee', 'Revue hebdomadaire', 'Ajustements tactiques', 'Implication forte'],
              highlight: false,
            },
          ].map((offre, i) => (
            <div key={i} style={{
              flex: '1 1 280px', maxWidth: 320,
              background: offre.highlight ? NAVY : 'white',
              color: offre.highlight ? 'white' : TEXT,
              padding: 32, borderRadius: 12,
              border: offre.highlight ? 'none' : `1px solid ${LIGHT}`,
              boxShadow: offre.highlight ? '0 12px 40px rgba(28,43,74,0.25)' : '0 2px 12px rgba(0,0,0,0.06)',
              position: 'relative',
              transform: offre.highlight ? 'scale(1.04)' : 'none',
            }}>
              {offre.highlight && (
                <div style={{
                  position: 'absolute', top: -12, left: '50%', transform: 'translateX(-50%)',
                  background: GOLD, color: NAVY, fontSize: 10, fontWeight: 700,
                  padding: '4px 16px', borderRadius: 20, letterSpacing: '0.1em',
                }}>RECOMMANDE</div>
              )}
              <div style={{ fontSize: 13, fontWeight: 600, color: offre.highlight ? GOLD : MUTED, marginBottom: 8 }}>{offre.nom}</div>
              <div style={{
                fontFamily: "'Playfair Display', Georgia, serif",
                fontSize: 36, fontWeight: 900, marginBottom: 4,
              }}>
                {offre.prix} <span style={{ fontSize: 16, fontWeight: 400 }}>EUR</span>
              </div>
              <p style={{ fontSize: 13, color: offre.highlight ? 'rgba(255,255,255,0.6)' : MUTED, marginBottom: 20, lineHeight: 1.5 }}>{offre.desc}</p>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {offre.items.map((item, j) => (
                  <li key={j} style={{
                    fontSize: 13, lineHeight: 1.6,
                    paddingLeft: 16, position: 'relative', marginBottom: 6,
                    color: offre.highlight ? 'rgba(255,255,255,0.85)' : TEXT,
                  }}>
                    <span style={{
                      position: 'absolute', left: 0, top: 7,
                      width: 6, height: 6, borderRadius: '50%',
                      background: GOLD,
                    }}></span>
                    {item}
                  </li>
                ))}
              </ul>
              <button
                onClick={() => navigate('/audit')}
                style={{
                  width: '100%', marginTop: 24,
                  background: offre.highlight ? GOLD : NAVY,
                  color: offre.highlight ? NAVY : 'white',
                  border: 'none', padding: '12px 0',
                  fontSize: 13, fontWeight: 700, borderRadius: 6, cursor: 'pointer',
                }}
              >
                COMMENCER
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* ==================== CONTACT ==================== */}
      <section id="contact" style={{ padding: '60px 40px', background: NAVY, color: 'white', textAlign: 'center' }}>
        <h2 style={{
          fontFamily: "'Playfair Display', Georgia, serif",
          fontSize: 28, fontWeight: 700, marginBottom: 16,
        }}>
          Pret a prendre de meilleures decisions ?
        </h2>
        <p style={{ fontSize: 16, color: 'rgba(255,255,255,0.6)', marginBottom: 32 }}>
          Contactez DECISIO Agency pour votre audit strategique.
        </p>
        <div style={{ display: 'flex', gap: 40, justifyContent: 'center', flexWrap: 'wrap', marginBottom: 32 }}>
          <div>
            <div style={{ fontSize: 11, color: GOLD, fontWeight: 700, letterSpacing: '0.1em', marginBottom: 4 }}>EMAIL</div>
            <div style={{ fontSize: 15 }}>contact@decisio.pro</div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: GOLD, fontWeight: 700, letterSpacing: '0.1em', marginBottom: 4 }}>SITE</div>
            <div style={{ fontSize: 15 }}>decisio.pro</div>
          </div>
        </div>
        <button
          onClick={() => navigate('/audit')}
          style={{
            background: GOLD, color: NAVY, border: 'none',
            padding: '14px 40px', fontSize: 15, fontWeight: 700,
            borderRadius: 6, cursor: 'pointer',
          }}
        >
          LANCER MON AUDIT MAINTENANT
        </button>
      </section>

      {/* ==================== FOOTER ==================== */}
      <footer style={{ padding: '20px 40px', background: '#0D1B2A', color: 'rgba(255,255,255,0.3)', fontSize: 12, textAlign: 'center' }}>
        DECISIO AGENCY - Audit Strategique B2B - Methode D3 - 2026
      </footer>
    </div>
  )
}
