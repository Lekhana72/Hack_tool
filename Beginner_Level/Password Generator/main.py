<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Secure Password Generator</title>
  <style>
    :root{
      --bg:#0f1724;
      --card:#0b1220;
      --accent:#7c3aed;
      --muted:#94a3b8;
      --glass: rgba(255,255,255,0.04);
      --success: #10b981;
      --danger: #ef4444;
      --radius:14px;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      color-scheme: dark;
    }
    *{box-sizing:border-box}
    html,body{height:100%;margin:0;background:linear-gradient(180deg,#071028 0%, #071423 60%);color:#e6eef8}
    .wrap{min-height:100%;display:grid;place-items:center;padding:32px}
    .card{
      width:100%;max-width:820px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border:1px solid rgba(255,255,255,0.04);padding:28px;border-radius:18px;box-shadow:0 8px 30px rgba(3,7,18,0.6);
    }

    header{display:flex;align-items:center;gap:16px;margin-bottom:18px}
    .logo{width:56px;height:56px;border-radius:12px;background:linear-gradient(135deg,var(--accent),#06b6d4);display:grid;place-items:center;font-weight:700}
    h1{font-size:20px;margin:0}
    p.lead{margin:0;color:var(--muted);font-size:13px}

    .controls{display:grid;grid-template-columns:1fr 300px;gap:18px;align-items:start}

    /* left panel */
    .left{background:var(--glass);padding:16px;border-radius:12px}
    .field{display:flex;gap:12px;align-items:center}
    label{font-size:13px;color:var(--muted)}
    input[type=range]{width:100%}

    .options{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
    .opt{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,0.02);padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.02)}
    .opt input{accent-color:var(--accent)}

    .strength{height:10px;background:rgba(255,255,255,0.03);border-radius:8px;overflow:hidden;margin-top:12px}
    .strength > i{display:block;height:100%;width:0%;background:linear-gradient(90deg,#ef4444,#f59e0b,#10b981);transition:width .25s ease}

    /* right panel */
    .right{display:flex;flex-direction:column;gap:12px;padding:16px;border-radius:12px}
    .output{display:flex;gap:8px;align-items:center;padding:14px;border-radius:10px;background:linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border:1px solid rgba(255,255,255,0.02)}
    .password{flex:1;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,monospace;font-size:16px;word-break:break-all}
    button{background:var(--accent);color:white;border:none;padding:10px 12px;border-radius:10px;font-weight:600;cursor:pointer}
    button.ghost{background:transparent;border:1px solid rgba(255,255,255,0.04)}

    .meta{display:flex;gap:8px;align-items:center;justify-content:space-between;margin-top:6px}
    .small{font-size:13px;color:var(--muted)}

    footer{margin-top:14px;font-size:13px;color:var(--muted);display:flex;justify-content:space-between;gap:12px}

    @media (max-width:820px){
      .controls{grid-template-columns:1fr;}
      .logo{width:44px;height:44px}
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card" role="main">
      <header>
        <div class="logo">PW</div>
        <div>
          <h1>Secure Password Generator</h1>
          <p class="lead">Generate strong, random passwords right in your browser. Uses Web Crypto for secure randomness.</p>
        </div>
      </header>

      <div class="controls">
        <div class="left" aria-labelledby="settings">
          <div id="settings" style="display:flex;justify-content:space-between;align-items:center;">
            <label class="small">Password Settings</label>
            <div class="small">Entropy: <strong id="entropy">—</strong></div>
          </div>

          <div style="margin-top:12px">
            <div class="field">
              <label for="length">Length</label>
              <input id="length" type="range" min="4" max="64" value="16" aria-label="Password length slider">
              <div style="width:44px;text-align:right;font-weight:700;"> <span id="lenVal">16</span></div>
            </div>

            <div class="options">
              <label class="opt"><input type="checkbox" id="lower" checked> Lowercase (a-z)</label>
              <label class="opt"><input type="checkbox" id="upper" checked> Uppercase (A-Z)</label>
              <label class="opt"><input type="checkbox" id="digits" checked> Digits (0-9)</label>
              <label class="opt"><input type="checkbox" id="symbols" checked> Symbols (!@#$...)</label>
            </div>

            <div class="small" style="margin-top:12px">Options: at least one character from each selected set will be included.</div>

            <div style="margin-top:12px">
              <div class="strength" aria-hidden="true"><i id="strengthBar"></i></div>
            </div>
          </div>
        </div>

        <div class="right">
          <div class="output" role="region" aria-label="Generated password area">
            <div class="password" id="password" tabindex="0" aria-live="polite">Click Generate to create a password</div>
            <button id="copyBtn" class="ghost" title="Copy to clipboard">Copy</button>
            <button id="eyeBtn" class="ghost" title="Show/hide">Show</button>
          </div>

          <div class="meta">
            <div class="small">Generated: <strong id="genCount">0</strong></div>
            <div class="small">Last copied: <span id="copiedAt">—</span></div>
          </div>

          <div style="display:flex;gap:8px">
            <button id="generate">Generate</button>
            <button id="download" class="ghost">Download .txt</button>
            <button id="clear" class="ghost">Clear</button>
          </div>

          <div class="small" style="margin-top:6px">Tip: Don’t reuse passwords. Use a password manager for storage.</div>
        </div>
      </div>

      <footer>
        <div>Built with <strong>Web Crypto</strong> — secure random numbers</div>
        <div>Accessible · Works offline</div>
      </footer>
    </div>
  </div>

  <script>
    // Character sets
    const SETS = {
      lower: 'abcdefghijklmnopqrstuvwxyz',
      upper: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      digits: '0123456789',
      symbols: '!@#$%^&*()-_=+[]{};:,.<>/?|'
    };

    // DOM refs
    const lengthSlider = document.getElementById('length');
    const lenVal = document.getElementById('lenVal');
    const lower = document.getElementById('lower');
    const upper = document.getElementById('upper');
    const digits = document.getElementById('digits');
    const symbols = document.getElementById('symbols');
    const genBtn = document.getElementById('generate');
    const passDiv = document.getElementById('password');
    const copyBtn = document.getElementById('copyBtn');
    const eyeBtn = document.getElementById('eyeBtn');
    const strengthBar = document.getElementById('strengthBar');
    const entropyEl = document.getElementById('entropy');
    const genCount = document.getElementById('genCount');
    const downloadBtn = document.getElementById('download');
    const clearBtn = document.getElementById('clear');
    const copiedAt = document.getElementById('copiedAt');

    let visible = false;
    let count = 0;

    function updateUI(){
      lenVal.textContent = lengthSlider.value;
      updateStrength();
    }

    lengthSlider.addEventListener('input', updateUI);
    lower.addEventListener('change', updateUI);
    upper.addEventListener('change', updateUI);
    digits.addEventListener('change', updateUI);
    symbols.addEventListener('change', updateUI);

    function chosenSets(){
      const picks = [];
      if(lower.checked) picks.push('lower');
      if(upper.checked) picks.push('upper');
      if(digits.checked) picks.push('digits');
      if(symbols.checked) picks.push('symbols');
      return picks;
    }

    function getAllChars(){
      return chosenSets().map(k=>SETS[k]).join('');
    }

    // Secure random integer in [0, max)
    function secureRandomInt(max){
      if(max <= 0) return 0;
      const array = new Uint32Array(1);
      window.crypto.getRandomValues(array);
      // use modulus — acceptable for this purpose
      return array[0] % max;
    }

    function generatePassword(){
      const length = Number(lengthSlider.value);
      const sets = chosenSets();
      if(sets.length === 0){
        alert('Please select at least one character set.');
        return '';
      }
      if(length < sets.length){
        alert('Length must be at least the number of selected character sets to guarantee inclusion.');
        return '';
      }

      // Ensure at least one from each selected set
      const passwordChars = [];
      for(const key of sets){
        const s = SETS[key];
        passwordChars.push(s[secureRandomInt(s.length)]);
      }
      const all = getAllChars();
      for(let i=passwordChars.length; i<length; i++){
        passwordChars.push(all[secureRandomInt(all.length)]);
      }

      // Shuffle (Fisher-Yates) using secure randomness
      for(let i = passwordChars.length -1; i>0; i--){
        const j = secureRandomInt(i+1);
        [passwordChars[i], passwordChars[j]] = [passwordChars[j], passwordChars[i]];
      }

      return passwordChars.join('');
    }

    function estimateEntropy(length, poolSize){
      // entropy bits = length * log2(poolSize)
      const bits = length * Math.log2(poolSize || 1);
      return Math.round(bits);
    }

    function updateStrength(){
      const length = Number(lengthSlider.value);
      const pool = getAllChars().length || 1;
      const bits = estimateEntropy(length, pool);
      entropyEl.textContent = bits + ' bits';

      // Visual strength (0-100)
      const score = Math.min(100, Math.round((bits / 128) * 100));
      strengthBar.style.width = score + '%';
    }

    genBtn.addEventListener('click', ()=>{
      const pwd = generatePassword();
      if(!pwd) return;
      passDiv.textContent = visible ? pwd : '*'.repeat(pwd.length);
      passDiv.setAttribute('data-plain', pwd);
      count += 1; genCount.textContent = count;
      updateStrength();
    });

    copyBtn.addEventListener('click', async ()=>{
      const plain = passDiv.getAttribute('data-plain');
      if(!plain){
        alert('No password to copy. Generate one first.');
        return;
      }
      try{
        await navigator.clipboard.writeText(plain);
        copiedAt.textContent = new Date().toLocaleTimeString();
        copyBtn.textContent = 'Copied';
        setTimeout(()=> copyBtn.textContent = 'Copy', 1500);
      }catch(e){
        alert('Copy failed: ' + e.message);
      }
    });

    eyeBtn.addEventListener('click', ()=>{
      visible = !visible;
      const plain = passDiv.getAttribute('data-plain') || '';
      passDiv.textContent = visible ? plain || 'Click Generate to create a password' : (plain ? '*'.repeat(plain.length) : 'Click Generate to create a password');
      eyeBtn.textContent = visible ? 'Hide' : 'Show';
    });

    downloadBtn.addEventListener('click', ()=>{
      const plain = passDiv.getAttribute('data-plain');
      if(!plain){ alert('No password to download.'); return; }
      const blob = new Blob([plain], {type:'text/plain'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'password.txt';
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(url);
    });

    clearBtn.addEventListener('click', ()=>{
      passDiv.textContent = 'Click Generate to create a password';
      passDiv.removeAttribute('data-plain');
      count = 0; genCount.textContent = 0; copiedAt.textContent = '—';
      updateStrength();
    });

    // initialize UI
    updateUI();

    // accessibility: allow pressing Enter on password area to copy
    passDiv.addEventListener('keydown', (e)=>{
      if(e.key === 'Enter') copyBtn.click();
    });
  </script>
</body>
</html>
