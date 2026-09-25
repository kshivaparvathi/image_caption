/**
 * Image Caption AI - API Client Module
 * Provides seamless async communication with the backend service.
 */

const Api = {
  baseUrl: '',

  async fetchPlatforms() {
    const res = await fetch(`${this.baseUrl}/api/platforms`);
    if (!res.ok) throw new Error('Failed to load platforms.');
    return await res.json();
  },

  async fetchLanguages() {
    const res = await fetch(`${this.baseUrl}/api/languages`);
    if (!res.ok) throw new Error('Failed to load languages.');
    return await res.json();
  },

  async fetchSamples() {
    const res = await fetch(`${this.baseUrl}/api/samples`);
    if (!res.ok) throw new Error('Failed to load sample benchmark images.');
    return await res.json();
  },

  async generateCaption({ file, sampleId, platform, language, instruction, variation }) {
    const formData = new FormData();
    if (file) {
      formData.append('file', file);
    }
    if (sampleId) {
      formData.append('sample_id', sampleId);
    }
    formData.append('platform', platform || 'caption');
    formData.append('language', language || 'en');
    if (instruction && instruction.trim()) {
      formData.append('instruction', instruction.trim());
    }
    formData.append('variation', variation || 0);

    const res = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      let errorMsg = 'Failed to generate caption.';
      try {
        const errData = await res.json();
        errorMsg = errData.detail || errorMsg;
      } catch (e) {}
      throw new Error(errorMsg);
    }

    return await res.json();
  },

  async checkHealth() {
    const res = await fetch(`${this.baseUrl}/api/health`);
    return await res.json();
  }
};
