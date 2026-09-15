import React, { useState } from 'react';
import { Sparkles, Wand2, Palette } from 'lucide-react';

const QUICK_PROMPTS = [
  { label: 'Modern Fintech', industry: 'Finance', desc: 'modern fintech, trustworthy, minimal, cyan accent' },
  { label: 'AI Deep Tech', industry: 'Tech', desc: 'futuristic artificial intelligence, cyber emerald, dark obsidian' },
  { label: 'Artisan Coffee', industry: 'Food', desc: 'artisan warm coffee roastery, handcrafted, cozy earthy' },
  { label: 'Clean Botanical', industry: 'Eco', desc: 'organic nature, sustainable, botanical flora, serene' },
  { label: 'Haute Fashion', industry: 'Retail', desc: 'minimalist luxury, monochrome, high fashion atelier' },
];

export default function InputForm({ onGenerate, isLoading }) {
  const [brandName, setBrandName] = useState('Apex');
  const [industry, setIndustry] = useState('Finance');
  const [styleDescription, setStyleDescription] = useState('modern fintech, trustworthy, minimal, electric cyan');
  const [preferredColor, setPreferredColor] = useState('');
  const [showColorPicker, setShowColorPicker] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!brandName.trim()) return;
    onGenerate({
      brand_name: brandName.trim(),
      industry: industry.trim(),
      style_description: styleDescription.trim(),
      preferred_color: preferredColor.trim() || undefined,
    });
  };

  const applyQuickPrompt = (p) => {
    setIndustry(p.industry);
    setStyleDescription(p.desc);
  };

  return (
    <div className="glass-card p-6" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
        <div style={{ 
          background: 'rgba(6, 182, 212, 0.15)', 
          padding: '8px', 
          borderRadius: '10px', 
          color: '#38BDF8',
          display: 'flex',
          alignItems: 'center'
        }}>
          <Wand2 size={20} />
        </div>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: '700' }}>Brand Identity Input</h2>
          <p style={{ fontSize: '12px', color: '#94A3B8' }}>AI analyzes your style & ML recommends palettes & fonts</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {/* Field 1: Brand Name */}
        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', marginBottom: '6px', color: '#E2E8F0' }}>
            1. Brand Name <span style={{ color: '#F43F5E' }}>*</span>
          </label>
          <input
            type="text"
            className="input-control"
            placeholder="e.g. Apex, Nova, Verdant"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
            required
            maxLength={40}
          />
        </div>

        {/* Field 2: Industry */}
        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', marginBottom: '6px', color: '#E2E8F0' }}>
            2. Industry Domain <span style={{ color: '#F43F5E' }}>*</span>
          </label>
          <select
            className="input-control"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            style={{ cursor: 'pointer' }}
          >
            <option value="Finance">Finance & Fintech</option>
            <option value="Tech">Technology & AI / SaaS</option>
            <option value="Health">Health & Wellness</option>
            <option value="Creative">Creative Agency & Studio</option>
            <option value="Eco">Eco, CleanTech & Nature</option>
            <option value="Food">Food, Coffee & Beverage</option>
            <option value="Retail">Retail, Fashion & Apparel</option>
            <option value="Luxury">Luxury, Real Estate & Hospitality</option>
          </select>
        </div>

        {/* Field 3: Style Description */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
            <label style={{ fontSize: '13px', fontWeight: '600', color: '#E2E8F0' }}>
              3. Style Description <span style={{ color: '#F43F5E' }}>*</span>
            </label>
            <span style={{ fontSize: '11px', color: '#64748B' }}>Natural language keywords</span>
          </div>
          <textarea
            className="input-control"
            rows={3}
            placeholder="e.g. modern, trustworthy, geometric, minimalist with cyber teal vibes"
            value={styleDescription}
            onChange={(e) => setStyleDescription(e.target.value)}
            required
          />
        </div>

        {/* Quick Inspiration Chips */}
        <div>
          <p style={{ fontSize: '11px', color: '#64748B', marginBottom: '6px' }}>Quick Inspiration Prompts:</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {QUICK_PROMPTS.map((p, idx) => (
              <button
                key={idx}
                type="button"
                className="chip"
                onClick={() => applyQuickPrompt(p)}
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>

        {/* Optional Preferred Color Accordion */}
        <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.06)', paddingTop: '12px' }}>
          <button
            type="button"
            onClick={() => setShowColorPicker(!showColorPicker)}
            style={{
              background: 'none',
              border: 'none',
              color: '#94A3B8',
              fontSize: '12px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <Palette size={14} />
            {showColorPicker ? 'Hide color preference' : '+ Add preferred color / tone bias (optional)'}
          </button>

          {showColorPicker && (
            <div style={{ marginTop: '10px', display: 'flex', gap: '10px', alignItems: 'center' }}>
              <input
                type="text"
                className="input-control"
                placeholder="e.g. Cyan, Emerald, #06B6D4, Gold, Warm"
                value={preferredColor}
                onChange={(e) => setPreferredColor(e.target.value)}
                style={{ flex: 1 }}
              />
              {preferredColor && (
                <button
                  type="button"
                  onClick={() => setPreferredColor('')}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#EF4444',
                    fontSize: '11px',
                    cursor: 'pointer',
                  }}
                >
                  Clear
                </button>
              )}
            </div>
          )}
        </div>

        {/* Action Button */}
        <button
          type="submit"
          className="btn-primary"
          disabled={isLoading || !brandName.trim()}
          style={{ width: '100%', marginTop: '8px' }}
        >
          {isLoading ? (
            <>
              <div style={{
                width: '16px',
                height: '16px',
                border: '2px solid #FFFFFF',
                borderTopColor: 'transparent',
                borderRadius: '50%',
                animation: 'spin 0.8s linear infinite',
              }} />
              <span>Synthesizing AI/ML Logo...</span>
            </>
          ) : (
            <>
              <Sparkles size={18} />
              <span>Generate SVG Logo</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
