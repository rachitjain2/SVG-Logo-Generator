import React, { useState } from 'react';
import { Sliders, Type, Palette, Layout, Shapes, ChevronDown, ChevronUp } from 'lucide-react';

export default function OverridePanel({
  palette,
  typography,
  layout,
  shape,
  options,
  onOverrideChange,
}) {
  const [isOpen, setIsOpen] = useState(true);

  if (!palette || !typography) return null;

  const handleColorChange = (key, value) => {
    const updatedPalette = { ...palette, [key]: value };
    onOverrideChange({ palette: updatedPalette });
  };

  const handleTypographyChange = (key, value) => {
    const updatedTypography = { ...typography, [key]: value };
    onOverrideChange({ typography: updatedTypography });
  };

  const colorItems = [
    { key: 'primary', label: 'Primary Brand' },
    { key: 'secondary', label: 'Secondary Tone' },
    { key: 'accent', label: 'Vibrant Accent' },
    { key: 'background', label: 'Background' },
    { key: 'text', label: 'Text / Monogram' },
  ];

  return (
    <div className="glass-card" style={{ marginTop: '20px', overflow: 'hidden' }}>
      {/* Accordion Toggle Header */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        style={{
          padding: '16px 20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          cursor: 'pointer',
          background: 'rgba(255, 255, 255, 0.02)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            background: 'rgba(99, 102, 241, 0.15)',
            padding: '6px',
            borderRadius: '8px',
            color: '#818CF8',
            display: 'flex',
            alignItems: 'center'
          }}>
            <Sliders size={18} />
          </div>
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: '700' }}>Manual Overrides & Customizer</h3>
            <p style={{ fontSize: '11px', color: '#94A3B8' }}>Fine-tune colors, typography, geometric shapes & layouts in real-time</p>
          </div>
        </div>
        <button
          type="button"
          style={{ background: 'none', border: 'none', color: '#94A3B8', cursor: 'pointer' }}
        >
          {isOpen ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>
      </div>

      {isOpen && (
        <div style={{ padding: '20px', borderTop: '1px solid var(--border-subtle)', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* 1. Color Palette Overrides */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
              <Palette size={15} color="#06B6D4" />
              <span style={{ fontSize: '13px', fontWeight: '600', color: '#E2E8F0' }}>Palette Swatches</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '10px' }}>
              {colorItems.map(({ key, label }) => (
                <div
                  key={key}
                  style={{
                    background: 'rgba(15, 23, 42, 0.5)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '8px',
                    padding: '8px 10px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                >
                  <input
                    type="color"
                    value={palette[key] || '#FFFFFF'}
                    onChange={(e) => handleColorChange(key, e.target.value)}
                    style={{
                      width: '28px',
                      height: '28px',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      background: 'none',
                    }}
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: '10px', color: '#94A3B8', textTransform: 'uppercase' }}>{label}</div>
                    <div style={{ fontSize: '12px', fontWeight: '600', color: '#F8FAFC' }}>
                      {palette[key]?.toUpperCase()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 2. Layout & Geometric Shape Switchers */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
            {/* Layout */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Layout size={15} color="#818CF8" />
                <span style={{ fontSize: '13px', fontWeight: '600', color: '#E2E8F0' }}>Layout Placement</span>
              </div>
              <div style={{ display: 'flex', gap: '6px' }}>
                {[
                  { id: 'horizontal', label: 'Horizontal' },
                  { id: 'stacked', label: 'Stacked' },
                  { id: 'badge', label: 'Badge Frame' },
                ].map((l) => (
                  <button
                    key={l.id}
                    type="button"
                    onClick={() => onOverrideChange({ layout: l.id })}
                    style={{
                      flex: 1,
                      padding: '8px 4px',
                      borderRadius: '8px',
                      fontSize: '12px',
                      fontWeight: '600',
                      cursor: 'pointer',
                      border: layout === l.id ? '1px solid #6366F1' : '1px solid rgba(255, 255, 255, 0.08)',
                      background: layout === l.id ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                      color: layout === l.id ? '#A5B4FC' : '#94A3B8',
                      transition: 'all 0.15s',
                    }}
                  >
                    {l.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Shape Archetype */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Shapes size={15} color="#34D399" />
                <span style={{ fontSize: '13px', fontWeight: '600', color: '#E2E8F0' }}>Geometric Shape</span>
              </div>
              <select
                className="input-control"
                value={shape}
                onChange={(e) => onOverrideChange({ shape: e.target.value })}
                style={{ cursor: 'pointer' }}
              >
                {options?.shapes?.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.category})
                  </option>
                )) || (
                  <>
                    <option value="hex_interlock">Isometric Hex / Cube</option>
                    <option value="lettermark_geometric">Geometric Monogram</option>
                    <option value="dynamic_arcs">Dynamic Motion Arcs</option>
                    <option value="shield_minimal">Minimalist Shield</option>
                    <option value="nodes_network">Neural / AI Nodes</option>
                    <option value="circular_orbit">Concentric Orbits</option>
                    <option value="botanical_spiral">Organic Botanical</option>
                  </>
                )}
              </select>
            </div>
          </div>

          {/* 3. Typography Customizer */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Type size={15} color="#F59E0B" />
              <span style={{ fontSize: '13px', fontWeight: '600', color: '#E2E8F0' }}>Typography Pairings</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '12px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#94A3B8', marginBottom: '4px' }}>
                  Header Font (Brand Name)
                </label>
                <select
                  className="input-control"
                  value={typography.primary_font}
                  onChange={(e) => handleTypographyChange('primary_font', e.target.value)}
                >
                  {(options?.fonts || ['Space Grotesk', 'Inter', 'Cinzel', 'Syne', 'Outfit', 'Plus Jakarta Sans', 'Fraunces', 'Playfair Display', 'Poppins']).map((f) => (
                    <option key={f} value={f}>{f}</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#94A3B8', marginBottom: '4px' }}>
                  Tagline Font (Subtext)
                </label>
                <select
                  className="input-control"
                  value={typography.secondary_font}
                  onChange={(e) => handleTypographyChange('secondary_font', e.target.value)}
                >
                  {(options?.fonts || ['Inter', 'Space Grotesk', 'Lato', 'Lora', 'Poppins', 'Outfit']).map((f) => (
                    <option key={f} value={f}>{f}</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#94A3B8', marginBottom: '4px' }}>
                  Font Weight
                </label>
                <div style={{ display: 'flex', gap: '6px' }}>
                  {[500, 600, 700, 800].map((w) => (
                    <button
                      key={w}
                      type="button"
                      onClick={() => handleTypographyChange('weight', w)}
                      style={{
                        flex: 1,
                        padding: '8px 2px',
                        borderRadius: '6px',
                        fontSize: '11px',
                        cursor: 'pointer',
                        border: typography.weight === w ? '1px solid #F59E0B' : '1px solid rgba(255, 255, 255, 0.08)',
                        background: typography.weight === w ? 'rgba(245, 158, 11, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                        color: typography.weight === w ? '#FDE68A' : '#94A3B8',
                      }}
                    >
                      {w}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
