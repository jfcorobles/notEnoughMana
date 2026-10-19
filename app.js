/**
 * NOT ENOUGH MANA - Companion App Controller
 * Lightweight PWA for Health and Mana tracking
 */

(() => {
  'use strict';

  // --- GAME STATE ---
  const MAX_HP = 10;
  const MIN_HP = 0;
  const MIN_MP = 0;

  let state = {
    hp: 10,
    mp: 0,
    soundEnabled: true,
    history: []
  };

  // --- AUDIO SYNTHESIZER (Web Audio API) ---
  let audioCtx = null;

  function initAudio() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        audioCtx = new AudioContext();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }

  const soundFX = {
    // Punchy damage hit
    damage() {
      if (!state.soundEnabled || !audioCtx) return;
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, now);
      osc.frequency.exponentialRampToValueAtTime(40, now + 0.18);

      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.2);
    },

    // Gentle upward heal chime
    heal() {
      if (!state.soundEnabled || !audioCtx) return;
      const now = audioCtx.currentTime;
      const notes = [440, 554.37, 659.25]; // A4, C#5, E5
      notes.forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const start = now + idx * 0.06;

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, start);

        gain.gain.setValueAtTime(0.2, start);
        gain.gain.exponentialRampToValueAtTime(0.001, start + 0.25);

        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(start);
        osc.stop(start + 0.25);
      });
    },

    // Bubbly potion gulp + energetic chime
    potion() {
      if (!state.soundEnabled || !audioCtx) return;
      const now = audioCtx.currentTime;

      // 1. Water bubbles / gulp
      for (let i = 0; i < 4; i++) {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const t = now + i * 0.05;
        osc.type = 'sine';
        osc.frequency.setValueAtTime(320 + Math.random() * 200, t);
        osc.frequency.exponentialRampToValueAtTime(700 + Math.random() * 200, t + 0.06);

        gain.gain.setValueAtTime(0.18, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.07);

        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(t);
        osc.stop(t + 0.07);
      }

      // 2. Triumphant mana chime
      const chimeNotes = [587.33, 739.99, 880]; // D5, F#5, A5
      chimeNotes.forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const start = now + 0.18 + idx * 0.07;

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, start);

        gain.gain.setValueAtTime(0.25, start);
        gain.gain.exponentialRampToValueAtTime(0.001, start + 0.35);

        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(start);
        osc.stop(start + 0.35);
      });
    },

    // Crisp mana point gain
    manaGain() {
      if (!state.soundEnabled || !audioCtx) return;
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(650, now);
      osc.frequency.exponentialRampToValueAtTime(1100, now + 0.12);

      gain.gain.setValueAtTime(0.2, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.16);
    },

    // Arcane mana point spend
    manaSpend() {
      if (!state.soundEnabled || !audioCtx) return;
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(520, now);
      osc.frequency.exponentialRampToValueAtTime(260, now + 0.14);

      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.16);
    },

    // Defeat funeral bell
    defeat() {
      if (!state.soundEnabled || !audioCtx) return;
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(110, now);
      osc.frequency.exponentialRampToValueAtTime(45, now + 0.8);

      gain.gain.setValueAtTime(0.4, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.9);

      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.9);
    }
  };

  // --- HAPTIC VIBRATION ---
  function triggerHaptic(pattern = 25) {
    if ('vibrate' in navigator) {
      try {
        navigator.vibrate(pattern);
      } catch (e) {
        // Silently catch browsers that block vibration
      }
    }
  }

  // --- WAKE LOCK API ---
  let wakeLockSentinel = null;
  async function toggleWakeLock() {
    if (!('wakeLock' in navigator)) {
      alert('Tu navegador no soporta la función de mantener pantalla activa.');
      return;
    }

    try {
      if (wakeLockSentinel !== null) {
        await wakeLockSentinel.release();
        wakeLockSentinel = null;
        updateWakeLockUI(false);
      } else {
        wakeLockSentinel = await navigator.wakeLock.request('screen');
        updateWakeLockUI(true);
        wakeLockSentinel.addEventListener('release', () => {
          wakeLockSentinel = null;
          updateWakeLockUI(false);
        });
      }
    } catch (err) {
      console.warn('WakeLock error:', err);
      updateWakeLockUI(false);
    }
  }

  function updateWakeLockUI(isActive) {
    const btn = document.getElementById('wakeLockBtn');
    if (!btn) return;
    if (isActive) {
      btn.classList.add('active');
      btn.title = 'Pantalla siempre activa: ACTIVADA';
    } else {
      btn.classList.remove('active');
      btn.title = 'Mantener pantalla activa (evita que se apague)';
    }
  }

  // --- DOM ELEMENTS ---
  const hpDisplay = document.getElementById('hpDisplay');
  const mpDisplay = document.getElementById('mpDisplay');
  const manaStatusLabel = document.getElementById('manaStatusLabel');
  const heartShape = document.getElementById('heartShape');
  const dropletShape = document.getElementById('dropletShape');
  const hpPipsContainer = document.getElementById('hpPipsContainer');
  const hpEffectsOverlay = document.getElementById('hpEffectsOverlay');
  const mpEffectsOverlay = document.getElementById('mpEffectsOverlay');

  const hpMinusBtn = document.getElementById('hpMinusBtn');
  const hpPlusBtn = document.getElementById('hpPlusBtn');
  const potionBtn = document.getElementById('potionBtn');
  const mpMinusBtn = document.getElementById('mpMinusBtn');
  const mpPlusBtn = document.getElementById('mpPlusBtn');

  const undoBtn = document.getElementById('undoBtn');
  const soundToggleBtn = document.getElementById('soundToggleBtn');
  const wakeLockBtn = document.getElementById('wakeLockBtn');
  const resetModalBtn = document.getElementById('resetModalBtn');
  const rulesBtn = document.getElementById('rulesBtn');

  // Modals
  const resetModal = document.getElementById('resetModal');
  const cancelResetBtn = document.getElementById('cancelResetBtn');
  const confirmResetBtn = document.getElementById('confirmResetBtn');

  const rulesModal = document.getElementById('rulesModal');
  const closeRulesBtn = document.getElementById('closeRulesBtn');
  const gotItRulesBtn = document.getElementById('gotItRulesBtn');

  const defeatOverlay = document.getElementById('defeatOverlay');
  const reviveBtn = document.getElementById('reviveBtn');
  const defeatNewGameBtn = document.getElementById('defeatNewGameBtn');

  // --- LOCAL STORAGE PERSISTENCE ---
  const STORAGE_KEY = 'nem_companion_state';

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        hp: state.hp,
        mp: state.mp,
        soundEnabled: state.soundEnabled
      }));
    } catch (e) {
      console.warn('Could not save to localStorage', e);
    }
  }

  function loadState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (typeof parsed.hp === 'number') state.hp = Math.max(MIN_HP, Math.min(MAX_HP, parsed.hp));
        if (typeof parsed.mp === 'number') state.mp = Math.max(MIN_MP, parsed.mp);
        if (typeof parsed.soundEnabled === 'boolean') state.soundEnabled = parsed.soundEnabled;
      }
    } catch (e) {
      console.warn('Could not load from localStorage', e);
    }
  }

  // --- HISTORY & UNDO ---
  function recordHistory() {
    state.history.push({ hp: state.hp, mp: state.mp });
    if (state.history.length > 25) state.history.shift();
    updateUndoButton();
  }

  function undoLastAction() {
    if (state.history.length === 0) return;
    initAudio();
    const prev = state.history.pop();
    state.hp = prev.hp;
    state.mp = prev.mp;
    saveState();
    render();
    triggerHaptic(20);
    soundFX.manaSpend();
    updateUndoButton();
  }

  function updateUndoButton() {
    if (undoBtn) {
      undoBtn.disabled = state.history.length === 0;
    }
  }

  // --- FLOATING TEXT ANIMATIONS ---
  function createFloatingText(container, text, type) {
    if (!container) return;
    const el = document.createElement('div');
    el.className = `float-effect float-${type}`;
    el.textContent = text;
    container.appendChild(el);
    setTimeout(() => {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 850);
  }

  // --- FORMAT NUMBERS (DOTTED RETICLE ZERO) ---
  function formatDisplayNumber(num) {
    const str = String(num);
    return str.split('').map(char => {
      if (char === '0') {
        return '<span class="digit-zero">0<span class="zero-dot" aria-hidden="true"></span></span>';
      }
      return `<span class="digit-char">${char}</span>`;
    }).join('');
  }

  // --- RENDER LOGIC ---
  function render() {
    // 1. Update HP Value
    if (hpDisplay) {
      hpDisplay.innerHTML = formatDisplayNumber(state.hp);
    }

    // 2. Update HP Pips
    const pips = hpPipsContainer ? hpPipsContainer.querySelectorAll('.hp-pip') : [];
    pips.forEach((pip, index) => {
      if (index < state.hp) {
        pip.classList.add('active');
      } else {
        pip.classList.remove('active');
      }
    });

    // 3. Heart Critical animation
    if (heartShape) {
      if (state.hp > 0 && state.hp <= 3) {
        heartShape.classList.add('heart-critical');
      } else {
        heartShape.classList.remove('heart-critical');
      }
    }

    // 4. Update MP Value
    if (mpDisplay) {
      mpDisplay.innerHTML = formatDisplayNumber(state.mp);
    }

    // 5. Dynamic Mana Status Subtitle
    if (manaStatusLabel) {
      if (state.mp === 0) {
        manaStatusLabel.textContent = 'Pozo Vacío (0 MP)';
      } else if (state.mp <= 2) {
        manaStatusLabel.textContent = `Gotas Mágicas (${state.mp} MP)`;
      } else if (state.mp <= 5) {
        manaStatusLabel.textContent = `Poción Cargada (${state.mp} MP)`;
      } else if (state.mp <= 8) {
        manaStatusLabel.textContent = `Torrente de Maná (${state.mp} MP)`;
      } else {
        manaStatusLabel.textContent = `¡Sobrecarga Arcana! (${state.mp} MP)`;
      }
    }

    // 6. Defeat Check
    if (state.hp <= 0) {
      defeatOverlay.classList.add('open');
      defeatOverlay.setAttribute('aria-hidden', 'false');
    } else {
      defeatOverlay.classList.remove('open');
      defeatOverlay.setAttribute('aria-hidden', 'true');
    }

    // 7. Update Sound UI
    updateSoundUI();
  }

  function updateSoundUI() {
    const onIcon = soundToggleBtn.querySelector('.sound-on-icon');
    const offIcon = soundToggleBtn.querySelector('.sound-off-icon');
    if (state.soundEnabled) {
      if (onIcon) onIcon.style.display = 'block';
      if (offIcon) offIcon.style.display = 'none';
      soundToggleBtn.classList.remove('active');
      soundToggleBtn.title = 'Sonido activado (clic para silenciar)';
    } else {
      if (onIcon) onIcon.style.display = 'none';
      if (offIcon) offIcon.style.display = 'block';
      soundToggleBtn.classList.add('active');
      soundToggleBtn.title = 'Sonido silenciado (clic para activar)';
    }
  }

  // --- GAME ACTIONS ---
  function changeHp(delta) {
    initAudio();
    const newHp = Math.max(MIN_HP, Math.min(MAX_HP, state.hp + delta));
    if (newHp === state.hp) return;

    recordHistory();
    state.hp = newHp;
    saveState();

    if (delta < 0) {
      soundFX.damage();
      triggerHaptic([35, 20, 35]);
      if (heartShape) {
        heartShape.classList.remove('shake-anim');
        void heartShape.offsetWidth; // trigger reflow
        heartShape.classList.add('shake-anim');
      }
      createFloatingText(hpEffectsOverlay, `${delta}`, 'damage');

      if (state.hp === 0) {
        setTimeout(() => soundFX.defeat(), 250);
      }
    } else {
      soundFX.heal();
      triggerHaptic(30);
      if (heartShape) {
        heartShape.classList.remove('pop-anim');
        void heartShape.offsetWidth;
        heartShape.classList.add('pop-anim');
      }
      createFloatingText(hpEffectsOverlay, `+${delta}`, 'heal');
    }

    render();
  }

  function changeMp(delta, isPotion = false) {
    initAudio();
    const newMp = Math.max(MIN_MP, state.mp + delta);
    if (newMp === state.mp && delta <= 0) return;

    recordHistory();
    state.mp = newMp;
    saveState();

    if (isPotion) {
      soundFX.potion();
      triggerHaptic([50, 40, 70]);
      if (dropletShape) {
        dropletShape.classList.remove('pop-anim');
        void dropletShape.offsetWidth;
        dropletShape.classList.add('pop-anim');
      }
      createFloatingText(mpEffectsOverlay, '+3 MP', 'mana');
    } else if (delta > 0) {
      soundFX.manaGain();
      triggerHaptic(25);
      if (dropletShape) {
        dropletShape.classList.remove('pop-anim');
        void dropletShape.offsetWidth;
        dropletShape.classList.add('pop-anim');
      }
      createFloatingText(mpEffectsOverlay, `+${delta} MP`, 'mana');
    } else {
      soundFX.manaSpend();
      triggerHaptic(20);
      createFloatingText(mpEffectsOverlay, `${delta} MP`, 'damage');
    }

    render();
  }

  function resetGame() {
    initAudio();
    recordHistory();
    state.hp = 10;
    state.mp = 0;
    saveState();
    render();
    soundFX.heal();
    triggerHaptic(50);
  }

  // --- EVENT LISTENERS ---
  function setupEventListeners() {
    // HP Buttons
    hpMinusBtn.addEventListener('click', () => changeHp(-1));
    hpPlusBtn.addEventListener('click', () => changeHp(1));

    // MP Buttons
    potionBtn.addEventListener('click', () => changeMp(3, true));
    mpMinusBtn.addEventListener('click', () => changeMp(-1, false));
    mpPlusBtn.addEventListener('click', () => changeMp(1, false));

    // Top Utility Controls
    undoBtn.addEventListener('click', undoLastAction);
    
    wakeLockBtn.addEventListener('click', toggleWakeLock);

    soundToggleBtn.addEventListener('click', () => {
      initAudio();
      state.soundEnabled = !state.soundEnabled;
      saveState();
      updateSoundUI();
      triggerHaptic(15);
      if (state.soundEnabled) soundFX.manaGain();
    });

    // Reset Modal
    resetModalBtn.addEventListener('click', () => {
      initAudio();
      resetModal.classList.add('open');
      resetModal.setAttribute('aria-hidden', 'false');
    });

    cancelResetBtn.addEventListener('click', () => {
      resetModal.classList.remove('open');
      resetModal.setAttribute('aria-hidden', 'true');
    });

    confirmResetBtn.addEventListener('click', () => {
      resetModal.classList.remove('open');
      resetModal.setAttribute('aria-hidden', 'true');
      resetGame();
    });

    // Rules Modal
    rulesBtn.addEventListener('click', () => {
      initAudio();
      rulesModal.classList.add('open');
      rulesModal.setAttribute('aria-hidden', 'false');
    });

    closeRulesBtn.addEventListener('click', () => {
      rulesModal.classList.remove('open');
      rulesModal.setAttribute('aria-hidden', 'true');
    });

    gotItRulesBtn.addEventListener('click', () => {
      rulesModal.classList.remove('open');
      rulesModal.setAttribute('aria-hidden', 'true');
    });

    // Defeat Actions
    reviveBtn.addEventListener('click', () => {
      defeatOverlay.classList.remove('open');
      defeatOverlay.setAttribute('aria-hidden', 'true');
      changeHp(1); // Revive with 1 HP
    });

    defeatNewGameBtn.addEventListener('click', () => {
      defeatOverlay.classList.remove('open');
      defeatOverlay.setAttribute('aria-hidden', 'true');
      resetGame();
    });

    // Close modals on backdrop click
    [resetModal, rulesModal].forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.classList.remove('open');
          modal.setAttribute('aria-hidden', 'true');
        }
      });
    });

    // Keyboard shortcuts for PC desktop users:
    // Left/Right or -/+ for HP, Up/Down for Mana, Space or P for Potion, Z for Undo
    window.addEventListener('keydown', (e) => {
      // Don't trigger if modal is open
      if (resetModal.classList.contains('open') || rulesModal.classList.contains('open')) return;

      if (e.key === 'q' || e.key === 'Q' || e.key === '1') {
        changeHp(-1);
      } else if (e.key === 'w' || e.key === 'W' || e.key === '2') {
        changeHp(1);
      } else if (e.key === ' ' || e.key === 'p' || e.key === 'P') {
        e.preventDefault();
        changeMp(3, true);
      } else if (e.key === 'a' || e.key === 'A') {
        changeMp(-1, false);
      } else if (e.key === 's' || e.key === 'S') {
        changeMp(1, false);
      } else if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
        e.preventDefault();
        undoLastAction();
      }
    });

    // Page visibility change: re-acquire wake lock if active
    document.addEventListener('visibilitychange', async () => {
      if (wakeLockSentinel !== null && document.visibilityState === 'visible') {
        try {
          wakeLockSentinel = await navigator.wakeLock.request('screen');
        } catch (e) {
          console.warn('Re-locking wake screen failed', e);
        }
      }
    });
  }

  // --- SERVICE WORKER REGISTRATION (PWA) ---
  function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
          .then((reg) => console.log('ServiceWorker registered:', reg.scope))
          .catch((err) => console.log('ServiceWorker registration failed:', err));
      });
    }
  }

  // --- INIT ---
  function init() {
    loadState();
    render();
    setupEventListeners();
    registerServiceWorker();
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
