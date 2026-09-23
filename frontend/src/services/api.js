const API_BASE = '/api';

async function request(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Accept': 'application/json',
        ...(options.headers || {})
      }
    });

    if (!res.ok) {
      let errorMsg = `Server error (${res.status})`;
      try {
        const errorData = await res.json();
        errorMsg = errorData.detail || errorData.message || errorMsg;
      } catch (e) {
        // Fallback to text
        const text = await res.text();
        if (text) errorMsg = text;
      }
      throw new Error(errorMsg);
    }

    return await res.json();
  } catch (err) {
    console.error(`API Error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  getHealth: () => request('/health'),
  getDashboard: () => request('/dashboard'),
  getTraditions: () => request('/traditions'),
  getTradition: (id) => request(`/traditions/${id}`),
  getBranch: (id) => request(`/branches/${id}`),
  getBranchComparison: (id) => request(`/branches/${id}/comparison`),
  getSources: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/sources${q ? `?${q}` : ''}`);
  },
  createSource: (data) =>
    request('/sources', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }),
  uploadSource: (formData) =>
    fetch(`${API_BASE}/sources/upload`, {
      method: 'POST',
      body: formData
    }).then(async (res) => {
      if (!res.ok) {
        let msg = `Upload failed (${res.status})`;
        try {
          const d = await res.json();
          msg = d.detail || msg;
        } catch (e) {}
        throw new Error(msg);
      }
      return res.json();
    }),
  analyzeBranch: (branchId) =>
    request(`/analyze?branch_id=${encodeURIComponent(branchId)}`, {
      method: 'POST'
    }),
  getGaps: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/gaps${q ? `?${q}` : ''}`);
  },
  getGap: (id) => request(`/gaps/${id}`),
  reconstructGap: (id) =>
    request(`/gaps/${id}/reconstruct`, {
      method: 'POST'
    }),
  verifyGap: (id, notes = '') =>
    request(`/gaps/${id}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes })
    }),
  rejectGap: (id, notes = '') =>
    request(`/gaps/${id}/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes })
    }),
  requestEvidenceGap: (id, notes = '') =>
    request(`/gaps/${id}/request-evidence`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ notes })
    }),
  getPreserved: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return request(`/knowledge${q ? `?${q}` : ''}`);
  },
  getGlossary: (q = '', domain = '') => {
    const params = new URLSearchParams();
    if (q) params.append('q', q);
    if (domain) params.append('domain', domain);
    const qs = params.toString();
    return request(`/glossary${qs ? `?${qs}` : ''}`);
  },
  getGraph: (branchId) => request(`/graph/${branchId}`),
  loadDemoData: () =>
    request('/demo/load', {
      method: 'POST'
    })
};
