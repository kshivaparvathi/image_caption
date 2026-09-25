/**
 * VisionCaption AI - Intelligent Voice Narration Player
 * Supports server-streamed audio (gTTS) & client Web Speech API with
 * visual wave animation, section highlighting, and playback controls.
 */

class VoicePlayer {
  constructor() {
    this.audioElement = new Audio();
    this.currentText = '';
    this.currentUrl = '';
    this.currentSection = null;
    this.currentLang = 'en';
    this.rate = 1.0;
    this.engine = 'server'; // 'server' (gTTS) or 'browser' (Web Speech)
    this.isPlaying = false;
    this.isPaused = false;
    
    // Canvas visualizer
    this.canvas = null;
    this.ctx = null;
    this.animFrameId = null;
    this.wavePhase = 0;

    this._initAudioListeners();
  }

  initVisualizer(canvasElement) {
    this.canvas = canvasElement;
    if (this.canvas) {
      this.ctx = this.canvas.getContext('2d');
      this.renderVisualizer();
    }
  }

  _initAudioListeners() {
    this.audioElement.addEventListener('play', () => {
      this.isPlaying = true;
      this.isPaused = false;
      this._updateUIState();
      this._highlightSection(this.currentSection);
      this._startVisualizerLoop();
    });

    this.audioElement.addEventListener('pause', () => {
      if (!this.audioElement.ended) {
        this.isPaused = true;
        this.isPlaying = false;
        this._updateUIState();
      }
    });

    this.audioElement.addEventListener('ended', () => {
      this.isPlaying = false;
      this.isPaused = false;
      this._updateUIState();
      this._unhighlightAll();
      this._stopVisualizerLoop();
    });

    this.audioElement.addEventListener('timeupdate', () => {
      this._updateProgress();
    });

    this.audioElement.addEventListener('error', (e) => {
      console.warn('Server audio playback failed, falling back to Web Speech API...', e);
      if (this.currentText) {
        this.engine = 'browser';
        this.play(this.currentText, this.currentSection, this.currentLang, true);
      }
    });
  }

  setRate(newRate) {
    this.rate = parseFloat(newRate);
    this.audioElement.playbackRate = this.rate;
    if (window.speechSynthesis && window.speechSynthesis.speaking) {
      // Re-trigger speech with new rate if browser engine active
    }
  }

  play(content, sectionId = 'full', langCode = 'en', isRawText = false) {
    this.stop();

    this.currentSection = sectionId;
    this.currentLang = langCode;

    // Check if content is audio URL or raw text
    const isUrl = typeof content === 'string' && (content.startsWith('/') || content.startsWith('http'));

    if (this.engine === 'server' && isUrl) {
      this.currentUrl = content;
      this.audioElement.src = content;
      this.audioElement.playbackRate = this.rate;
      this.audioElement.play().catch(err => {
        console.error('Audio play error:', err);
      });
    } else {
      // Use Web Speech API or generated URL
      const textToSpeak = isUrl ? decodeURIComponent(content.split('text=')[1]?.split('&')[0] || '') : content;
      this.currentText = textToSpeak;

      if (this.engine === 'browser' || !isUrl) {
        this._playWebSpeech(textToSpeak, langCode);
      } else {
        const encoded = encodeURIComponent(textToSpeak);
        this.currentUrl = `/api/tts?text=${encoded}&lang=${langCode}`;
        this.audioElement.src = this.currentUrl;
        this.audioElement.playbackRate = this.rate;
        this.audioElement.play().catch(err => console.error(err));
      }
    }

    this._highlightSection(sectionId);
    this._setNowPlayingLabel(sectionId);
  }

  _playWebSpeech(text, langCode) {
    if (!('speechSynthesis' in window)) {
      alert('Text to speech is not supported in this browser.');
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = this.rate;

    // Try finding matching voice
    const voices = window.speechSynthesis.getVoices();
    const cleanLang = langCode.toLowerCase().split('-')[0];
    const matchingVoice = voices.find(v => v.lang.toLowerCase().startsWith(cleanLang));
    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }
    utterance.lang = langCode;

    utterance.onstart = () => {
      this.isPlaying = true;
      this.isPaused = false;
      this._updateUIState();
      this._startVisualizerLoop();
    };

    utterance.onend = () => {
      this.isPlaying = false;
      this.isPaused = false;
      this._updateUIState();
      this._unhighlightAll();
      this._stopVisualizerLoop();
    };

    utterance.onerror = () => {
      this.isPlaying = false;
      this._updateUIState();
      this._stopVisualizerLoop();
    };

    window.speechSynthesis.speak(utterance);
  }

  pause() {
    if (this.engine === 'server') {
      this.audioElement.pause();
    } else if (window.speechSynthesis) {
      window.speechSynthesis.pause();
    }
    this.isPaused = true;
    this.isPlaying = false;
    this._updateUIState();
    this._stopVisualizerLoop();
  }

  resume() {
    if (this.engine === 'server') {
      this.audioElement.play();
    } else if (window.speechSynthesis) {
      window.speechSynthesis.resume();
    }
    this.isPlaying = true;
    this.isPaused = false;
    this._updateUIState();
    this._startVisualizerLoop();
  }

  stop() {
    this.audioElement.pause();
    this.audioElement.currentTime = 0;
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    this.isPlaying = false;
    this.isPaused = false;
    this._updateUIState();
    this._unhighlightAll();
    this._stopVisualizerLoop();
    this._setNowPlayingLabel(null);
  }

  replay() {
    if (this.currentUrl || this.currentText) {
      this.audioElement.currentTime = 0;
      if (this.engine === 'server' && this.currentUrl) {
        this.audioElement.play();
      } else {
        this.play(this.currentText, this.currentSection, this.currentLang);
      }
    }
  }

  seek(percent) {
    if (this.audioElement.duration) {
      this.audioElement.currentTime = (percent / 100) * this.audioElement.duration;
    }
  }

  _highlightSection(sectionId) {
    this._unhighlightAll();
    if (!sectionId) return;

    const el = document.getElementById(`card-${sectionId}`);
    if (el) {
      el.classList.add('playing-section-highlight');
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  _unhighlightAll() {
    document.querySelectorAll('.playing-section-highlight').forEach(el => {
      el.classList.remove('playing-section-highlight');
    });
  }

  _setNowPlayingLabel(sectionId) {
    const label = document.getElementById('now-speaking-indicator');
    if (!label) return;

    if (!sectionId) {
      label.textContent = 'Voice Ready • Click any section to listen';
      return;
    }

    const titles = {
      'full': 'Full Comprehensive Narration',
      'caption': 'Short Caption',
      'description': 'Detailed Scene Description',
      'scene': 'Scene & Environment Context',
      'elements': 'Important Visible Elements',
      'actions': 'Activities & Actions',
      'people': 'People & Demographic Visual Info',
      'insights': 'Visual Insights & Composition',
      'qa': 'Interactive Follow-up Answer'
    };

    label.textContent = `🎙️ Now Narrating: ${titles[sectionId] || sectionId}`;
  }

  _updateUIState() {
    const playBtn = document.getElementById('btn-voice-play');
    const pauseBtn = document.getElementById('btn-voice-pause');
    const resumeBtn = document.getElementById('btn-voice-resume');
    
    if (this.isPlaying) {
      if (playBtn) playBtn.classList.add('hidden');
      if (pauseBtn) pauseBtn.classList.remove('hidden');
      if (resumeBtn) resumeBtn.classList.add('hidden');
    } else if (this.isPaused) {
      if (playBtn) playBtn.classList.add('hidden');
      if (pauseBtn) pauseBtn.classList.add('hidden');
      if (resumeBtn) resumeBtn.classList.remove('hidden');
    } else {
      if (playBtn) playBtn.classList.remove('hidden');
      if (pauseBtn) pauseBtn.classList.add('hidden');
      if (resumeBtn) resumeBtn.classList.add('hidden');
    }
  }

  _updateProgress() {
    const progressBar = document.getElementById('audio-progress-bar');
    const timeDisplay = document.getElementById('audio-time-display');

    if (this.audioElement.duration) {
      const cur = this.audioElement.currentTime;
      const dur = this.audioElement.duration;
      const pct = (cur / dur) * 100;
      if (progressBar) progressBar.style.width = `${pct}%`;

      if (timeDisplay) {
        timeDisplay.textContent = `${this._formatTime(cur)} / ${this._formatTime(dur)}`;
      }
    }
  }

  _formatTime(sec) {
    if (!sec || isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  // Wave Visualizer Animation
  _startVisualizerLoop() {
    if (!this.canvas) return;
    const loop = () => {
      this.renderVisualizer();
      this.animFrameId = requestAnimationFrame(loop);
    };
    cancelAnimationFrame(this.animFrameId);
    this.animFrameId = requestAnimationFrame(loop);
  }

  _stopVisualizerLoop() {
    cancelAnimationFrame(this.animFrameId);
    this.renderVisualizer(true);
  }

  renderVisualizer(isIdle = false) {
    if (!this.canvas || !this.ctx) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    const ctx = this.ctx;

    ctx.clearRect(0, 0, w, h);

    const bars = 24;
    const barWidth = 4;
    const spacing = (w - (bars * barWidth)) / (bars - 1);

    this.wavePhase += 0.08;

    for (let i = 0; i < bars; i++) {
      let barHeight;
      if (isIdle || !this.isPlaying) {
        barHeight = 4;
      } else {
        const wave = Math.sin(this.wavePhase + i * 0.45) * 0.5 + 0.5;
        const subwave = Math.cos(this.wavePhase * 0.8 + i * 0.3) * 0.3 + 0.3;
        barHeight = Math.max(4, (wave + subwave) * (h * 0.75));
      }

      const x = i * (barWidth + spacing);
      const y = (h - barHeight) / 2;

      // Gradient color for bars
      const grad = ctx.createLinearGradient(0, y, 0, y + barHeight);
      grad.addColorStop(0, '#3b82f6');
      grad.addColorStop(1, '#8b5cf6');

      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect(x, y, barWidth, barHeight, 2);
      ctx.fill();
    }
  }
}

window.voicePlayer = new VoicePlayer();
