/**
 * Image Caption AI - Main Application Controller
 * Handles routing, drag-and-drop uploads, voice recognition,
 * multilingual text-to-speech with Play/Pause/Resume/Stop,
 * platform switching, inline editing, and caption regeneration.
 */

const App = {
  // Application State
  state: {
    currentRoute: '/',
    currentPlatform: 'instagram',
    selectedLanguage: 'en',
    selectedFile: null,
    selectedSampleId: null,
    previewUrl: null,
    instruction: '',
    variationCount: 0,
    isProcessing: false,
    isRecordingVoice: false,
    recognitionInstance: null,
    speechSynthesisUtterance: null,
    audioElement: null,
    speechState: 'stopped', // 'stopped' | 'playing' | 'paused'
    lastResult: null,
    isEditing: false
  },

  platforms: {
    instagram: {
      id: 'instagram',
      name: 'Instagram Caption',
      title: 'Instagram Caption Generator',
      slug: 'instagram',
      icon: 'instagram',
      badge: 'Social & Reels',
      tagline: 'Aesthetic, engaging captions with catchy hooks, storytelling, and viral hashtags.',
      placeholder: 'e.g. Make it aesthetic, add travel hashtags, sound funny, or keep it short'
    },
    twitter: {
      id: 'twitter',
      name: 'X / Twitter Post',
      title: 'X / Twitter Post Generator',
      slug: 'twitter',
      icon: 'twitter',
      badge: 'Short-Form',
      tagline: 'Concise, punchy posts optimized for high engagement under 280 characters.',
      placeholder: 'e.g. Make it witty, add tech hashtags, punchy one-liner, or sound bold'
    },
    linkedin: {
      id: 'linkedin',
      name: 'LinkedIn Post',
      title: 'LinkedIn Post Generator',
      slug: 'linkedin',
      icon: 'linkedin',
      badge: 'Professional',
      tagline: 'Thoughtful, career-oriented commentary with leadership takeaways and professional framing.',
      placeholder: 'e.g. Focus on leadership, productivity takeaways, career advice, or teamwork'
    },
    facebook: {
      id: 'facebook',
      name: 'Facebook Caption',
      title: 'Facebook Caption Generator',
      slug: 'facebook',
      icon: 'facebook',
      badge: 'Community',
      tagline: 'Warm, relatable social captions designed to spark friendly conversations and comments.',
      placeholder: 'e.g. Make it warm and family-friendly, add a fun question, or sound nostalgic'
    },
    whatsapp: {
      id: 'whatsapp',
      name: 'WhatsApp Status',
      title: 'WhatsApp Status Generator',
      slug: 'whatsapp',
      icon: 'whatsapp',
      badge: 'Status Story',
      tagline: 'Short, expressive status lines and mood quotes perfect for 24-hour stories.',
      placeholder: 'e.g. Keep it deep, make it funny, minimalist mood quote, or weekend vibe'
    },
    caption: {
      id: 'caption',
      name: 'General Image Caption',
      title: 'General Image Caption Generator',
      slug: 'caption',
      icon: 'caption',
      badge: 'Descriptive',
      tagline: 'Natural, rich visual descriptions capturing subjects, context, composition, and mood.',
      placeholder: 'e.g. Keep it short, make it descriptive, focus on lighting, or poetic tone'
    }
  },

  // ----------------- INITIALIZATION -----------------
  async init() {
    this.bindEvents();
    await this.loadLanguages();
    this.handleRoute(window.location.pathname, false);

    window.addEventListener('popstate', () => {
      this.handleRoute(window.location.pathname, false);
    });
  },

  bindEvents() {
    // Dropzone drag & drop
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');

    if (dropzone && fileInput) {
      ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzone.classList.add('border-indigo-500', 'bg-indigo-500/10');
        });
      });

      ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzone.classList.remove('border-indigo-500', 'bg-indigo-500/10');
        });
      });

      dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt.files && dt.files.length > 0) {
          this.handleFileSelected(dt.files[0]);
        }
      });

      fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
          this.handleFileSelected(e.target.files[0]);
        }
      });
    }

    // Language selection change
    const langSelect = document.getElementById('lang-select');
    if (langSelect) {
      langSelect.addEventListener('change', (e) => {
        this.state.selectedLanguage = e.target.value;
      });
    }

    // Editable caption textarea sync
    const captionEditor = document.getElementById('caption-editor');
    if (captionEditor) {
      captionEditor.addEventListener('input', () => {
        this.updateCharCount();
      });
    }
  },

  // ----------------- ROUTING -----------------
  navigate(path, push = true) {
    if (push) {
      window.history.pushState(null, '', path);
    }
    this.handleRoute(path);
  },

  handleRoute(pathname) {
    const cleanPath = pathname.replace(/^\/+|\/+$/g, '');
    const homeView = document.getElementById('home-view');
    const generatorView = document.getElementById('generator-view');

    // Route matching
    if (!cleanPath || cleanPath === 'home') {
      this.state.currentRoute = '/';
      if (homeView) homeView.classList.remove('hidden');
      if (generatorView) generatorView.classList.add('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (this.platforms[cleanPath]) {
      this.state.currentRoute = `/${cleanPath}`;
      this.setPlatform(cleanPath);
      if (homeView) homeView.classList.add('hidden');
      if (generatorView) generatorView.classList.remove('hidden');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      // Fallback to Home
      this.navigate('/', false);
    }
  },

  scrollToSection(sectionId) {
    if (this.state.currentRoute !== '/') {
      this.navigate('/');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }
  },

  setPlatform(platformKey) {
    const platform = this.platforms[platformKey] || this.platforms.caption;
    this.state.currentPlatform = platform.id;

    // Update Header
    const titleEl = document.getElementById('platform-title');
    const badgeEl = document.getElementById('platform-badge');
    const taglineEl = document.getElementById('platform-tagline');
    const iconContainer = document.getElementById('platform-icon-container');
    const instructionInput = document.getElementById('instruction-input');

    if (titleEl) titleEl.textContent = platform.title;
    if (badgeEl) badgeEl.textContent = platform.badge;
    if (taglineEl) taglineEl.textContent = platform.tagline;
    if (instructionInput) instructionInput.placeholder = platform.placeholder;

    if (iconContainer) {
      iconContainer.innerHTML = this.getPlatformIconSvg(platform.id, 'w-6 h-6');
    }

    // Update active nav pills if any
    document.querySelectorAll('.platform-pill').forEach(btn => {
      const p = btn.getAttribute('data-platform');
      if (p === platform.id) {
        btn.classList.add('bg-indigo-600', 'text-white', 'border-indigo-500');
        btn.classList.remove('bg-gray-800/80', 'text-gray-300', 'border-gray-700');
      } else {
        btn.classList.remove('bg-indigo-600', 'text-white', 'border-indigo-500');
        btn.classList.add('bg-gray-800/80', 'text-gray-300', 'border-gray-700');
      }
    });
  },

  // ----------------- LANGUAGES -----------------
  async loadLanguages() {
    try {
      const data = await Api.fetchLanguages();
      const select = document.getElementById('lang-select');
      if (!select) return;

      select.innerHTML = '';

      // Required prioritized languages group
      const coreGroup = document.createElement('optgroup');
      coreGroup.label = 'Featured & Indian Languages';

      const otherGroup = document.createElement('optgroup');
      otherGroup.label = 'Other Global Languages';

      const coreCodes = ['en', 'te', 'hi', 'ta', 'kn', 'ml', 'bn', 'mr'];

      data.languages.forEach(l => {
        const opt = document.createElement('option');
        opt.value = l.code;
        opt.textContent = `${l.flag} ${l.name} (${l.native_name})`;
        if (coreCodes.includes(l.code)) {
          coreGroup.appendChild(opt);
        } else {
          otherGroup.appendChild(opt);
        }
      });

      select.appendChild(coreGroup);
      select.appendChild(otherGroup);
      select.value = this.state.selectedLanguage;
    } catch (e) {
      console.warn('Could not load language registry:', e);
    }
  },

  // ----------------- FILE & SAMPLE HANDLING -----------------
  handleFileSelected(file) {
    const allowed = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    const maxBytes = 15 * 1024 * 1024; // 15MB

    if (!allowed.includes(file.type.toLowerCase())) {
      this.showError('Unsupported format. Please upload JPG, PNG, or WEBP images.');
      return;
    }

    if (file.size > maxBytes) {
      this.showError('File exceeds 15MB maximum size. Please upload a smaller image.');
      return;
    }

    this.clearError();
    this.hideResult();
    this.state.lastResult = null;
    this.state.selectedFile = file;
    this.state.selectedSampleId = null;

    const reader = new FileReader();
    reader.onload = (e) => {
      this.state.previewUrl = e.target.result;
      this.renderImagePreview();
    };
    reader.readAsDataURL(file);
  },

  loadSample(sampleId, imageUrl) {
    this.clearError();
    this.hideResult();
    this.state.lastResult = null;
    this.state.selectedFile = null;
    this.state.selectedSampleId = sampleId;
    this.state.previewUrl = imageUrl;
    this.renderImagePreview();
  },

  renderImagePreview() {
    const dropzoneContainer = document.getElementById('dropzone-container');
    const previewContainer = document.getElementById('preview-container');
    const previewImg = document.getElementById('preview-img');

    if (this.state.previewUrl) {
      if (dropzoneContainer) dropzoneContainer.classList.add('hidden');
      if (previewContainer) previewContainer.classList.remove('hidden');
      if (previewImg) previewImg.src = this.state.previewUrl;
    } else {
      if (dropzoneContainer) dropzoneContainer.classList.remove('hidden');
      if (previewContainer) previewContainer.classList.add('hidden');
      if (previewImg) previewImg.src = '';
    }
  },

  removeImage() {
    this.state.selectedFile = null;
    this.state.selectedSampleId = null;
    this.state.previewUrl = null;
    const fileInput = document.getElementById('file-input');
    if (fileInput) fileInput.value = '';
    this.renderImagePreview();
    this.hideResult();
  },

  // ----------------- USER INSTRUCTIONS & VOICE -----------------
  applyChip(text) {
    const input = document.getElementById('instruction-input');
    if (input) {
      input.value = text;
      this.state.instruction = text;
      input.focus();
    }
  },

  toggleVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const micBtn = document.getElementById('btn-mic');
    const input = document.getElementById('instruction-input');

    if (!SpeechRecognition) {
      this.showError('Speech recognition is not supported in this browser. Please type your instruction directly.');
      return;
    }

    if (this.state.isRecordingVoice) {
      // Stop recording
      if (this.state.recognitionInstance) {
        this.state.recognitionInstance.stop();
      }
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      this.state.recognitionInstance = recognition;
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = this.state.selectedLanguage === 'en' ? 'en-US' : this.state.selectedLanguage;

      recognition.onstart = () => {
        this.state.isRecordingVoice = true;
        if (micBtn) {
          micBtn.classList.add('mic-recording');
          micBtn.title = 'Listening... Click to stop';
        }
        if (input) input.placeholder = 'Listening... Speak your instruction now...';
      };

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        if (input) {
          input.value = transcript;
          this.state.instruction = transcript;
        }
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition error:', event.error);
        if (event.error === 'not-allowed') {
          this.showError('Microphone access was denied. Please allow microphone permissions in your browser settings.');
        } else if (event.error !== 'no-speech') {
          this.showError(`Voice input error: ${event.error}`);
        }
        this.stopVoiceRecognition();
      };

      recognition.onend = () => {
        this.stopVoiceRecognition();
      };

      recognition.start();
    } catch (e) {
      console.error('Failed to start speech recognition:', e);
      this.showError('Unable to activate microphone. Please type your instruction.');
      this.stopVoiceRecognition();
    }
  },

  stopVoiceRecognition() {
    this.state.isRecordingVoice = false;
    const micBtn = document.getElementById('btn-mic');
    const input = document.getElementById('instruction-input');
    const platform = this.platforms[this.state.currentPlatform] || this.platforms.caption;

    if (micBtn) {
      micBtn.classList.remove('mic-recording');
      micBtn.title = 'Speak instruction with voice';
    }
    if (input) {
      input.placeholder = platform.placeholder;
      input.focus();
    }
  },

  // ----------------- CAPTION GENERATION -----------------
  async generateCaption(isRegeneration = false) {
    if (!this.state.selectedFile && !this.state.selectedSampleId) {
      this.showError('Please upload an image or select a sample image before generating.');
      return;
    }

    this.clearError();
    this.stopSpeech();

    if (isRegeneration) {
      this.state.variationCount += 1;
    } else {
      this.state.variationCount = 0;
    }

    const instructionInput = document.getElementById('instruction-input');
    const instruction = instructionInput ? instructionInput.value.trim() : '';

    this.showProcessing(true);

    try {
      const result = await Api.generateCaption({
        file: this.state.selectedFile,
        sampleId: this.state.selectedSampleId,
        platform: this.state.currentPlatform,
        language: this.state.selectedLanguage,
        instruction: instruction,
        variation: this.state.variationCount
      });

      this.state.lastResult = result;
      this.renderResult(result);
      this.showProcessing(false);

      // Smooth scroll to result
      const resultCard = document.getElementById('result-section');
      if (resultCard) {
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    } catch (err) {
      this.showProcessing(false);
      this.showError(err.message || 'AI caption generation encountered an error. Please try again.');
    }
  },

  regenerateCaption() {
    const regenBtn = document.getElementById('btn-regenerate');
    if (regenBtn) {
      const icon = regenBtn.querySelector('.regen-icon');
      if (icon) icon.classList.add('animate-spin');
    }
    this.generateCaption(true).finally(() => {
      if (regenBtn) {
        const icon = regenBtn.querySelector('.regen-icon');
        if (icon) icon.classList.remove('animate-spin');
      }
    });
  },

  showProcessing(show) {
    this.state.isProcessing = show;
    const generateBtn = document.getElementById('btn-generate');
    const processingSection = document.getElementById('processing-state');
    const resultSection = document.getElementById('result-section');

    if (generateBtn) {
      generateBtn.disabled = show;
      generateBtn.classList.toggle('opacity-60', show);
    }

    if (processingSection) {
      processingSection.classList.toggle('hidden', !show);
    }

    if (show && resultSection) {
      resultSection.classList.add('hidden');
    }
  },

  // ----------------- RESULT RENDERING -----------------
  renderResult(res) {
    const resultSection = document.getElementById('result-section');
    const captionEditor = document.getElementById('caption-editor');
    const platformBadge = document.getElementById('res-platform-badge');
    const langBadge = document.getElementById('res-lang-badge');
    const resultImg = document.getElementById('res-img');

    // Visual breakdown
    const sceneTag = document.getElementById('vis-scene');
    const objectsTag = document.getElementById('vis-objects');
    const activityTag = document.getElementById('vis-activity');
    const moodTag = document.getElementById('vis-mood');

    if (resultImg && this.state.previewUrl) {
      resultImg.src = this.state.previewUrl;
    }

    if (captionEditor) {
      captionEditor.value = res.caption;
      this.updateCharCount();
    }

    if (platformBadge) {
      platformBadge.innerHTML = `${this.getPlatformIconSvg(res.platform.id, 'w-3.5 h-3.5 inline mr-1')} ${res.platform.name}`;
    }

    if (langBadge) {
      langBadge.textContent = `${res.language.flag} ${res.language.name} (${res.language.native_name})`;
    }

    // Render 4 Alternative Captions
    const altContainer = document.getElementById('alternatives-container');
    const altList = document.getElementById('alternatives-list');
    if (altContainer && altList) {
      if (res.alternatives && res.alternatives.length > 0) {
        altList.innerHTML = res.alternatives.map((alt, idx) => `
          <div class="p-3.5 rounded-xl bg-gray-950/70 border border-gray-800/90 hover:border-gray-700/80 transition flex flex-col sm:flex-row sm:items-start justify-between gap-3 group">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1.5">
                <span class="text-xs font-bold text-indigo-400">${alt.label}</span>
                <span class="text-[10px] px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-medium">${alt.badge}</span>
              </div>
              <p class="text-sm text-gray-200 leading-relaxed">${alt.caption}</p>
            </div>
            <div class="flex items-center gap-1.5 self-end sm:self-center shrink-0">
              <button onclick="App.useAlternative(${idx})" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-indigo-600/30 hover:bg-indigo-600 text-indigo-200 hover:text-white border border-indigo-500/30 transition flex items-center gap-1" title="Use this caption as the main caption">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <span>Use as Main</span>
              </button>
              <button onclick="App.copyAlternative(${idx}, this)" class="p-1.5 rounded-lg text-gray-400 hover:text-white bg-gray-900 hover:bg-gray-800 border border-gray-800 transition" title="Copy alternative">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
              </button>
              <button onclick="App.playAlternativeSpeech(${idx})" class="p-1.5 rounded-lg text-gray-400 hover:text-white bg-gray-900 hover:bg-gray-800 border border-gray-800 transition" title="Listen to this caption">
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
              </button>
            </div>
          </div>
        `).join('');
        altContainer.classList.remove('hidden');
      } else {
        altContainer.classList.add('hidden');
        altList.innerHTML = '';
      }
    }

    // Render separate verified hashtags
    const hashtagsContainer = document.getElementById('hashtags-container');
    const hashtagsDisplay = document.getElementById('hashtags-display');
    if (hashtagsContainer && hashtagsDisplay) {
      if (res.hashtags && res.hashtags.length > 0) {
        hashtagsDisplay.innerHTML = res.hashtags.map(t => `
          <span class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 select-all cursor-pointer hover:bg-indigo-500/20 transition">
            ${t}
          </span>
        `).join('');
        hashtagsContainer.classList.remove('hidden');
      } else {
        hashtagsContainer.classList.add('hidden');
        hashtagsDisplay.innerHTML = '';
      }
    }

    if (resultSection) {
      resultSection.classList.remove('hidden');
    }
  },

  hideResult() {
    const resultSection = document.getElementById('result-section');
    if (resultSection) resultSection.classList.add('hidden');
    this.stopSpeech();
  },

  updateCharCount() {
    const editor = document.getElementById('caption-editor');
    const charCount = document.getElementById('char-count');
    const wordCount = document.getElementById('word-count');
    if (!editor) return;

    const text = editor.value;
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;

    if (charCount) charCount.textContent = `${chars} chars`;
    if (wordCount) wordCount.textContent = `${words} words`;
  },

  // ----------------- ACTIONS: COPY & EDIT -----------------
  copyCaption() {
    const editor = document.getElementById('caption-editor');
    const copyBtn = document.getElementById('btn-copy');
    if (!editor) return;

    const text = editor.value;
    navigator.clipboard.writeText(text).then(() => {
      if (copyBtn) {
        const originalHtml = copyBtn.innerHTML;
        copyBtn.innerHTML = `
          <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <span class="text-emerald-400 font-medium">Copied!</span>
        `;
        setTimeout(() => {
          copyBtn.innerHTML = originalHtml;
        }, 2000);
      }
    }).catch(() => {
      this.showError('Unable to access clipboard. Please copy manually.');
    });
  },

  copyHashtags() {
    if (!this.state.lastResult || !this.state.lastResult.hashtags) return;
    const tagsText = this.state.lastResult.hashtags.join(' ');
    const btn = document.getElementById('btn-copy-hashtags');
    navigator.clipboard.writeText(tagsText).then(() => {
      if (btn) {
        const orig = btn.innerHTML;
        btn.innerHTML = `<span class="text-emerald-400">Copied!</span>`;
        setTimeout(() => { btn.innerHTML = orig; }, 2000);
      }
    });
  },

  useAlternative(index) {
    if (!this.state.lastResult || !this.state.lastResult.alternatives) return;
    const alt = this.state.lastResult.alternatives[index];
    if (!alt) return;

    const editor = document.getElementById('caption-editor');
    if (editor) {
      editor.value = alt.caption;
      this.updateCharCount();
      editor.classList.add('ring-2', 'ring-indigo-500', 'bg-indigo-950/20');
      setTimeout(() => {
        editor.classList.remove('ring-2', 'ring-indigo-500', 'bg-indigo-950/20');
      }, 1000);
      editor.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  },

  copyAlternative(index, btnEl) {
    if (!this.state.lastResult || !this.state.lastResult.alternatives) return;
    const alt = this.state.lastResult.alternatives[index];
    if (!alt) return;

    navigator.clipboard.writeText(alt.caption).then(() => {
      if (btnEl) {
        const origHtml = btnEl.innerHTML;
        btnEl.innerHTML = `<svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`;
        setTimeout(() => { btnEl.innerHTML = origHtml; }, 2000);
      }
    });
  },

  playAlternativeSpeech(index) {
    if (!this.state.lastResult || !this.state.lastResult.alternatives) return;
    const alt = this.state.lastResult.alternatives[index];
    if (!alt) return;

    this.stopSpeech();
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(alt.caption);
      const langCode = (this.state.lastResult.language && this.state.lastResult.language.bcp47) || 'en-US';
      utterance.lang = langCode;
      window.speechSynthesis.speak(utterance);
    }
  },

  toggleEditCaption() {
    const editor = document.getElementById('caption-editor');
    const editBtn = document.getElementById('btn-edit');
    if (!editor) return;

    this.state.isEditing = !this.state.isEditing;
    if (this.state.isEditing) {
      editor.removeAttribute('readonly');
      editor.classList.add('ring-2', 'ring-indigo-500/80', 'bg-gray-900/90');
      editor.focus();
      if (editBtn) editBtn.classList.add('bg-indigo-600/30', 'text-indigo-300');
    } else {
      editor.setAttribute('readonly', 'true');
      editor.classList.remove('ring-2', 'ring-indigo-500/80', 'bg-gray-900/90');
      if (editBtn) editBtn.classList.remove('bg-indigo-600/30', 'text-indigo-300');
    }
  },

  // ----------------- TEXT-TO-SPEECH (PLAY / PAUSE / RESUME / STOP) -----------------
  playSpeech() {
    const editor = document.getElementById('caption-editor');
    if (!editor || !editor.value.trim()) return;

    const text = editor.value.trim();

    // If currently paused, resume playback
    if (this.state.speechState === 'paused') {
      this.resumeSpeech();
      return;
    }

    this.stopSpeech();

    // Check Web Speech API availability
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      this.state.speechSynthesisUtterance = utterance;

      // Match voice for selected language
      const voices = window.speechSynthesis.getVoices();
      const targetLang = this.state.selectedLanguage;
      
      // Preferred language codes map
      const langBcp47Map = {
        'en': 'en-US',
        'te': 'te-IN',
        'hi': 'hi-IN',
        'ta': 'ta-IN',
        'kn': 'kn-IN',
        'ml': 'ml-IN',
        'bn': 'bn-IN',
        'mr': 'mr-IN',
        'es': 'es-ES',
        'fr': 'fr-FR',
        'de': 'de-DE'
      };
      const bcp = langBcp47Map[targetLang] || targetLang;

      const matchingVoice = voices.find(v => v.lang === bcp || v.lang.startsWith(targetLang));
      if (matchingVoice) {
        utterance.voice = matchingVoice;
      }
      utterance.lang = bcp;
      utterance.rate = 1.0;

      utterance.onstart = () => {
        this.setSpeechState('playing');
      };

      utterance.onend = () => {
        this.setSpeechState('stopped');
      };

      utterance.onerror = (e) => {
        console.warn('Speech synthesis error, attempting audio fallback:', e);
        this.playBackendAudioFallback(text, targetLang);
      };

      window.speechSynthesis.speak(utterance);
      this.setSpeechState('playing');

    } else {
      // Fallback to backend TTS endpoint
      this.playBackendAudioFallback(text, this.state.selectedLanguage);
    }
  },

  pauseSpeech() {
    if (this.state.audioElement) {
      this.state.audioElement.pause();
      this.setSpeechState('paused');
      return;
    }

    if ('speechSynthesis' in window && window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      this.setSpeechState('paused');
    }
  },

  resumeSpeech() {
    if (this.state.audioElement) {
      this.state.audioElement.play();
      this.setSpeechState('playing');
      return;
    }

    if ('speechSynthesis' in window && window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      this.setSpeechState('playing');
    } else {
      this.playSpeech();
    }
  },

  stopSpeech() {
    if (this.state.audioElement) {
      this.state.audioElement.pause();
      this.state.audioElement.currentTime = 0;
      this.state.audioElement = null;
    }

    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }

    this.setSpeechState('stopped');
  },

  playBackendAudioFallback(text, lang) {
    try {
      this.stopSpeech();
      const audioUrl = `/api/tts?text=${encodeURIComponent(text)}&lang=${encodeURIComponent(lang)}`;
      const audio = new Audio(audioUrl);
      this.state.audioElement = audio;

      audio.onplay = () => this.setSpeechState('playing');
      audio.onpause = () => this.setSpeechState('paused');
      audio.onended = () => this.setSpeechState('stopped');
      audio.onerror = () => {
        this.setSpeechState('stopped');
        this.showError('Text-to-speech audio could not be played.');
      };

      audio.play();
    } catch (e) {
      this.setSpeechState('stopped');
      this.showError('Text-to-speech not supported.');
    }
  },

  setSpeechState(state) {
    this.state.speechState = state;
    const btnPlay = document.getElementById('btn-tts-play');
    const btnPause = document.getElementById('btn-tts-pause');
    const btnResume = document.getElementById('btn-tts-resume');
    const btnStop = document.getElementById('btn-tts-stop');
    const waveBars = document.querySelectorAll('.audio-bar');

    // Controls display toggling
    if (state === 'playing') {
      if (btnPlay) btnPlay.classList.add('hidden');
      if (btnPause) btnPause.classList.remove('hidden');
      if (btnResume) btnResume.classList.add('hidden');
      if (btnStop) btnStop.classList.remove('hidden');
      waveBars.forEach(b => b.classList.add('audio-bar-animating'));
    } else if (state === 'paused') {
      if (btnPlay) btnPlay.classList.add('hidden');
      if (btnPause) btnPause.classList.add('hidden');
      if (btnResume) btnResume.classList.remove('hidden');
      if (btnStop) btnStop.classList.remove('hidden');
      waveBars.forEach(b => b.classList.remove('audio-bar-animating'));
    } else {
      // Stopped
      if (btnPlay) btnPlay.classList.remove('hidden');
      if (btnPause) btnPause.classList.add('hidden');
      if (btnResume) btnResume.classList.add('hidden');
      if (btnStop) btnStop.classList.add('hidden');
      waveBars.forEach(b => b.classList.remove('audio-bar-animating'));
    }
  },

  // ----------------- ERRORS & ALERTS -----------------
  showError(msg) {
    const box = document.getElementById('error-box');
    const text = document.getElementById('error-message');
    if (box && text) {
      text.textContent = msg;
      box.classList.remove('hidden');
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  },

  clearError() {
    const box = document.getElementById('error-box');
    if (box) box.classList.add('hidden');
  },

  // ----------------- THEME TOGGLE -----------------
  toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) {
      themeBtn.textContent = next === 'dark' ? '☀️ Light' : '🌙 Dark';
    }
  },

  // ----------------- ICON HELPERS -----------------
  getPlatformIconSvg(id, classes = 'w-5 h-5') {
    switch (id) {
      case 'instagram':
        return `<svg class="${classes}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>`;
      case 'twitter':
        return `<svg class="${classes}" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>`;
      case 'linkedin':
        return `<svg class="${classes}" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>`;
      case 'facebook':
        return `<svg class="${classes}" viewBox="0 0 24 24" fill="currentColor"><path d="M22.675 0h-21.35c-.732 0-1.325.593-1.325 1.325v21.351c0 .731.593 1.324 1.325 1.324h11.495v-9.294h-3.128v-3.622h3.128v-2.671c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12v9.293h6.116c.73 0 1.323-.593 1.323-1.325v-21.35c0-.732-.593-1.325-1.325-1.325z"/></svg>`;
      case 'whatsapp':
        return `<svg class="${classes}" viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>`;
      default:
        return `<svg class="${classes}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`;
    }
  }
};

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
