import React, { useState, useRef } from 'react';
import { 
  Download, 
  RotateCw, 
  ZoomIn, 
  ZoomOut, 
  Maximize2, 
  Sun, 
  Moon, 
  Grid, 
  Check, 
  Sparkles,
  Layers,
  Cpu
} from 'lucide-react';

export default function LogoPreview({ 
  svg, 
  brandName, 
  onRegenerate, 
  similarityScore, 
  matchReasons, 
  isLLMPowered, 
  isLoading 
}) {
  const [bgMode, setBgMode] = useState('dark'); // 'dark' | 'light' | 'checker'
  const [zoom, setZoom] = useState(1.0);
  const [downloadSuccess, setDownloadSuccess] = useState(null); // 'svg' | 'png' | null
  const containerRef = useRef(null);

  // SVG Blob Download
  const handleExportSVG = () => {
    if (!svg) return;
    const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${brandName.toLowerCase().replace(/\s+/g, '_')}_logo.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setDownloadSuccess('svg');
    setTimeout(() => setDownloadSuccess(null), 2500);
  };

  // High-DPI PNG Rasterization Export
  const handleExportPNG = () => {
    if (!svg) return;
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(svg, 'image/svg+xml');
    const svgElement = svgDoc.documentElement;
    
    // Parse dimensions from viewBox or attributes
    const viewBox = svgElement.getAttribute('viewBox');
    let width = 800;
    let height = 600;
    if (viewBox) {
      const parts = viewBox.split(/\s+/).map(Number);
      if (parts.length === 4) {
        width = parts[2];
        height = parts[3];
      }
    }

    // High resolution multiplier for crystal clear output
    const scale = 2.5;
    const canvas = document.createElement('canvas');
    canvas.width = width * scale;
    canvas.height = height * scale;
    const ctx = canvas.getContext('2d');

    // Create an Image from SVG Data URI
    const svgString = new XMLSerializer().serializeToString(svgDoc);
    const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
    const URLObject = window.URL || window.webkitURL || window;
    const blobURL = URLObject.createObjectURL(svgBlob);

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      URLObject.revokeObjectURL(blobURL);

      // Trigger download
      canvas.toBlob((pngBlob) => {
        if (!pngBlob) return;
        const pngURL = URLObject.createObjectURL(pngBlob);
        const link = document.createElement('a');
        link.href = pngURL;
        link.download = `${brandName.toLowerCase().replace(/\s+/g, '_')}_logo.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URLObject.revokeObjectURL(pngURL);

        setDownloadSuccess('png');
        setTimeout(() => setDownloadSuccess(null), 2500);
      }, 'image/png');
    };
    img.src = blobURL;
  };

  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header Bar: Status & View Controls */}
      <div style={{
        padding: '16px 20px',
        borderBottom: '1px solid var(--border-subtle)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '10px',
      }}>
        {/* ML / AI Badges */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{
            background: isLLMPowered ? 'rgba(16, 185, 129, 0.15)' : 'rgba(59, 130, 246, 0.15)',
            border: `1px solid ${isLLMPowered ? 'rgba(16, 185, 129, 0.3)' : 'rgba(59, 130, 246, 0.3)'}`,
            borderRadius: '999px',
            padding: '3px 10px',
            display: 'flex',
            alignItems: 'center',
            gap: '5px',
            fontSize: '11px',
            color: isLLMPowered ? '#34D399' : '#60A5FA',
            fontWeight: '600',
          }}>
            <Cpu size={12} />
            {isLLMPowered ? 'NVIDIA NIM Active' : 'ML Engine'}
          </div>

          {similarityScore !== undefined && (
            <div style={{
              background: 'rgba(6, 182, 212, 0.15)',
              border: '1px solid rgba(6, 182, 212, 0.3)',
              borderRadius: '999px',
              padding: '3px 10px',
              fontSize: '11px',
              color: '#38BDF8',
              fontWeight: '600',
            }}>
              {(similarityScore * 100).toFixed(1)}% Cosine Match
            </div>
          )}
        </div>

        {/* Canvas Display Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {/* Background switcher */}
          <button
            type="button"
            className="btn-secondary"
            style={{ padding: '6px 10px' }}
            title="Dark Background"
            onClick={() => setBgMode('dark')}
          >
            <Moon size={14} color={bgMode === 'dark' ? '#38BDF8' : '#94A3B8'} />
          </button>
          <button
            type="button"
            className="btn-secondary"
            style={{ padding: '6px 10px' }}
            title="Light Background"
            onClick={() => setBgMode('light')}
          >
            <Sun size={14} color={bgMode === 'light' ? '#38BDF8' : '#94A3B8'} />
          </button>
          <button
            type="button"
            className="btn-secondary"
            style={{ padding: '6px 10px' }}
            title="Checkerboard (Transparent)"
            onClick={() => setBgMode('checker')}
          >
            <Grid size={14} color={bgMode === 'checker' ? '#38BDF8' : '#94A3B8'} />
          </button>

          {/* Zoom controls */}
          <div style={{ width: '1px', height: '18px', background: 'rgba(255, 255, 255, 0.1)', margin: '0 4px' }} />
          <button
            type="button"
            className="btn-secondary"
            style={{ padding: '6px 8px' }}
            onClick={() => setZoom(Math.max(0.6, zoom - 0.15))}
            title="Zoom Out"
          >
            <ZoomOut size={14} />
          </button>
          <span style={{ fontSize: '11px', color: '#94A3B8', minWidth: '32px', textAlign: 'center' }}>
            {Math.round(zoom * 100)}%
          </span>
          <button
            type="button"
            className="btn-secondary"
            style={{ padding: '6px 8px' }}
            onClick={() => setZoom(Math.min(1.8, zoom + 0.15))}
            title="Zoom In"
          >
            <ZoomIn size={14} />
          </button>
          <button
            type="button"
            className="btn-secondary"
            style={{ padding: '6px 8px' }}
            onClick={() => setZoom(1.0)}
            title="Reset Zoom"
          >
            <Maximize2 size={13} />
          </button>
        </div>
      </div>

      {/* Main SVG Render Canvas */}
      <div 
        ref={containerRef}
        className={bgMode === 'checker' ? 'checkerboard' : ''}
        style={{
          flex: 1,
          minHeight: '380px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '30px',
          backgroundColor: bgMode === 'dark' ? '#080C14' : bgMode === 'light' ? '#F8FAFC' : 'transparent',
          overflow: 'hidden',
          position: 'relative',
          transition: 'background-color 0.25s',
        }}
      >
        {svg ? (
          <div 
            style={{
              width: '100%',
              maxWidth: '640px',
              transform: `scale(${zoom})`,
              transformOrigin: 'center center',
              transition: 'transform 0.15s ease-out',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              filter: 'drop-shadow(0 10px 25px rgba(0, 0, 0, 0.25))',
            }}
            dangerouslySetInnerHTML={{ __html: svg }}
          />
        ) : (
          <div style={{ textAlign: 'center', color: '#64748B' }}>
            <Layers size={40} style={{ margin: '0 auto 12px', opacity: 0.4 }} />
            <p style={{ fontSize: '14px' }}>Fill in brand details to synthesize an SVG logo</p>
          </div>
        )}
      </div>

      {/* Match Reasons Footer Bar */}
      {matchReasons && matchReasons.length > 0 && (
        <div style={{
          padding: '8px 20px',
          background: 'rgba(0, 0, 0, 0.25)',
          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '11px',
          color: '#94A3B8',
          flexWrap: 'wrap',
        }}>
          <span style={{ color: '#06B6D4', fontWeight: '600' }}>AI Match Insights:</span>
          {matchReasons.map((r, i) => (
            <span key={i} style={{ background: 'rgba(255, 255, 255, 0.04)', padding: '2px 8px', borderRadius: '4px' }}>
              • {r}
            </span>
          ))}
        </div>
      )}

      {/* Action Footer: Regenerate & Export */}
      <div style={{
        padding: '16px 20px',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '10px',
        background: 'rgba(15, 23, 42, 0.4)',
      }}>
        {/* Regenerate Button */}
        <button
          type="button"
          className="btn-secondary"
          onClick={onRegenerate}
          disabled={isLoading || !svg}
          style={{ padding: '10px 16px', fontWeight: '600' }}
        >
          <RotateCw size={15} style={{ animation: isLoading ? 'spin 1s linear infinite' : 'none' }} />
          <span>Regenerate Variation</span>
        </button>

        {/* Export Buttons */}
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            type="button"
            className="btn-secondary"
            onClick={handleExportSVG}
            disabled={!svg}
            style={{
              padding: '10px 16px',
              borderColor: downloadSuccess === 'svg' ? '#10B981' : undefined,
              color: downloadSuccess === 'svg' ? '#34D399' : undefined,
            }}
          >
            {downloadSuccess === 'svg' ? <Check size={15} /> : <Download size={15} />}
            <span>Export SVG</span>
          </button>

          <button
            type="button"
            className="btn-primary"
            onClick={handleExportPNG}
            disabled={!svg}
            style={{ padding: '10px 18px' }}
          >
            {downloadSuccess === 'png' ? <Check size={15} /> : <Download size={15} />}
            <span>Export PNG (High-Res)</span>
          </button>
        </div>
      </div>
    </div>
  );
}
