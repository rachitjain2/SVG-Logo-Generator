import React, { useState, useEffect } from 'react';
import { Sparkles, Brain, Cpu, Layers, ExternalLink } from 'lucide-react';
import InputForm from './components/InputForm';
import LogoPreview from './components/LogoPreview';
import OverridePanel from './components/OverridePanel';
import AlternativesDrawer from './components/AlternativesDrawer';
import { fetchOptions, generateLogo, reRenderLogo } from './services/api';

export default function App() {
  const [options, setOptions] = useState(null);
  const [logoData, setLogoData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load options & synthesize initial logo on mount
  useEffect(() => {
    async function init() {
      try {
        const opts = await fetchOptions();
        setOptions(opts);
        
        // Synthesize initial demo logo
        handleGenerate({
          brand_name: 'Apex',
          industry: 'Finance',
          style_description: 'modern fintech, trustworthy, minimal, electric cyan',
        });
      } catch (err) {
        console.error('Initialization error:', err);
        setError(err.message);
      }
    }
    init();
  }, []);

  // Main generation handler (calls LLM + ML Recommender + SVG Generator)
  const handleGenerate = async (payload) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await generateLogo(payload);
      setLogoData(data);
    } catch (err) {
      console.error('Generation failed:', err);
      setError(err.message || 'Failed to generate logo. Please check backend connection.');
    } finally {
      setIsLoading(false);
    }
  };

  // Instant re-render handler for manual overrides
  const handleOverrideChange = async (updates) => {
    if (!logoData) return;

    const newPalette = updates.palette || logoData.selected_palette;
    const newTypography = updates.typography || logoData.selected_typography;
    const newLayout = updates.layout || logoData.layout;
    const newShape = updates.shape || logoData.shape;
    const seed = updates.seed !== undefined ? updates.seed : logoData.seed;

    try {
      const { svg } = await reRenderLogo({
        brand_name: logoData.brand_name,
        tagline: logoData.tagline,
        palette: newPalette,
        typography: newTypography,
        layout_type: newLayout,
        shape_type: newShape,
        seed: seed,
      });

      setLogoData((prev) => ({
        ...prev,
        svg: svg,
        selected_palette: newPalette,
        selected_typography: newTypography,
        layout: newLayout,
        shape: newShape,
        seed: seed,
      }));
    } catch (err) {
      console.error('Re-render failed:', err);
    }
  };

  // Regenerate variation (rotates seed and layout/shape variation)
  const handleRegenerate = () => {
    if (!logoData) return;
    const newSeed = Math.floor(Math.random() * 90000) + 1000;
    handleOverrideChange({ seed: newSeed });
  };

  // Apply alternative candidate recommendation
  const handleSelectAlternative = (alt) => {
    if (!logoData) return;
    handleOverrideChange({
      palette: alt.palette,
      typography: alt.typography,
      shape: alt.shape_affinity?.[0] || logoData.shape,
    });
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navigation Header */}
      <header style={{
        padding: '16px 28px',
        borderBottom: '1px solid var(--border-subtle)',
        background: 'rgba(11, 15, 25, 0.8)',
        backdropFilter: 'blur(12px)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        position: 'sticky',
        top: 0,
        zIndex: 50,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            background: 'linear-gradient(135deg, #0284C7 0%, #6366F1 100%)',
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#FFFFFF',
          }}>
            <Sparkles size={20} />
          </div>
          <div>
            <h1 style={{ fontSize: '18px', fontWeight: '800', letterSpacing: '-0.02em' }}>
              Aesthetic <span className="text-gradient">SVG Logo</span> Generator
            </h1>
            <p style={{ fontSize: '11px', color: '#94A3B8' }}>AI/ML Mini Project • Procedural Vector Design</p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            background: 'rgba(99, 102, 241, 0.12)',
            border: '1px solid rgba(99, 102, 241, 0.25)',
            borderRadius: '999px',
            padding: '4px 12px',
            fontSize: '12px',
            color: '#A5B4FC',
            fontWeight: '600',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}>
            <Brain size={14} />
            <span>k-NN Recommender &amp; NVIDIA NIM</span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{
        flex: 1,
        maxWidth: '1360px',
        margin: '0 auto',
        width: '100%',
        padding: '24px 20px',
      }}>
        {error && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: '12px',
            padding: '12px 16px',
            marginBottom: '20px',
            color: '#FCA5A5',
            fontSize: '13px',
          }}>
            ⚠️ {error}
          </div>
        )}

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(320px, 420px) minmax(400px, 1fr)',
          gap: '24px',
          alignItems: 'start',
        }}>
          {/* Left Column: 3-Field Input Form */}
          <div>
            <InputForm onGenerate={handleGenerate} isLoading={isLoading} />
          </div>

          {/* Right Column: Live SVG Preview & Controls */}
          <div>
            <LogoPreview
              svg={logoData?.svg}
              brandName={logoData?.brand_name || 'Logo'}
              onRegenerate={handleRegenerate}
              similarityScore={logoData?.similarity_score}
              matchReasons={logoData?.match_reasons}
              isLLMPowered={logoData?.is_llm_powered}
              isLoading={isLoading}
            />

            {/* Manual Customization Overrides */}
            {logoData && (
              <OverridePanel
                palette={logoData.selected_palette}
                typography={logoData.selected_typography}
                layout={logoData.layout}
                shape={logoData.shape}
                options={options}
                onOverrideChange={handleOverrideChange}
              />
            )}

            {/* Alternative ML Candidates Drawer */}
            {logoData?.alternatives && (
              <AlternativesDrawer
                alternatives={logoData.alternatives}
                onSelectAlternative={handleSelectAlternative}
              />
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer style={{
        padding: '16px 28px',
        borderTop: '1px solid var(--border-subtle)',
        fontSize: '12px',
        color: '#64748B',
        textAlign: 'center',
        background: 'rgba(11, 15, 25, 0.6)',
      }}>
        AI/ML Mini Project: SVG Logo Generator • Powered by Scikit-Learn k-NN Metric Retrieval, NVIDIA NIM &amp; Procedural SVG Engine
      </footer>
    </div>
  );
}
