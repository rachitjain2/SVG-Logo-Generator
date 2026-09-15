import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function AlternativesDrawer({ alternatives, onSelectAlternative }) {
  if (!alternatives || alternatives.length <= 1) return null;

  return (
    <div className="glass-card p-6" style={{ marginTop: '20px', padding: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
        <Sparkles size={16} color="#06B6D4" />
        <h3 style={{ fontSize: '15px', fontWeight: '700' }}>Alternative ML Recommendations</h3>
        <span style={{ fontSize: '11px', color: '#94A3B8' }}>(Top-k Candidates from Scikit-Learn Recommender)</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
        {alternatives.map((alt, idx) => (
          <div
            key={alt.id || idx}
            onClick={() => onSelectAlternative(alt)}
            className="glass-card-hover"
            style={{
              background: 'rgba(15, 23, 42, 0.6)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              borderRadius: '12px',
              padding: '14px',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: '10px',
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <span style={{ fontSize: '11px', color: '#38BDF8', fontWeight: '700' }}>
                  # {idx + 1} Candidate
                </span>
                <span style={{
                  fontSize: '11px',
                  background: 'rgba(6, 182, 212, 0.15)',
                  color: '#22D3EE',
                  padding: '2px 6px',
                  borderRadius: '999px',
                  fontWeight: '600'
                }}>
                  {(alt.similarity_score * 100).toFixed(1)}% Match
                </span>
              </div>
              <div style={{ fontSize: '13px', fontWeight: '600', color: '#F1F5F9', marginBottom: '8px' }}>
                {alt.name}
              </div>

              {/* Palette swatches preview */}
              <div style={{ display: 'flex', gap: '5px', marginBottom: '8px' }}>
                {Object.values(alt.palette).slice(0, 4).map((col, i) => (
                  <div
                    key={i}
                    style={{
                      width: '20px',
                      height: '20px',
                      borderRadius: '4px',
                      background: col,
                      border: '1px solid rgba(255, 255, 255, 0.15)'
                    }}
                    title={col}
                  />
                ))}
              </div>

              {/* Fonts */}
              <div style={{ fontSize: '11px', color: '#94A3B8' }}>
                Fonts: <span style={{ color: '#E2E8F0' }}>{alt.typography.primary_font}</span> & {alt.typography.secondary_font}
              </div>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              paddingTop: '8px',
              borderTop: '1px solid rgba(255, 255, 255, 0.06)',
              fontSize: '11px',
              color: '#38BDF8',
              fontWeight: '600'
            }}>
              <span>Apply Style</span>
              <ArrowRight size={12} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
