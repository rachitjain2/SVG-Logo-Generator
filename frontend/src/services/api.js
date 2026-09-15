/**
 * API client communicating with FastAPI backend.
 */

const BASE_URL = '/api';

export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchOptions() {
  const res = await fetch(`${BASE_URL}/options`);
  if (!res.ok) throw new Error(`Failed to load options: ${res.statusText}`);
  return res.json();
}

export async function generateLogo(payload) {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Generation failed: ${res.statusText}`);
  }
  return res.json();
}

export async function reRenderLogo(payload) {
  const res = await fetch(`${BASE_URL}/re-render`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || `Re-render failed: ${res.statusText}`);
  }
  return res.json();
}
