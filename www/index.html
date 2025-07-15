<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Password Manager Dashboard</title>
  <style>
    /* Base Styles */
    * {
      box-sizing: border-box;
    }
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #121212;
      color: #e0e0e0;
      transition: background-color 0.3s ease, color 0.3s ease;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: #1f1f1f;
      padding: 10px 20px;
      height: 60px;
      transition: background-color 0.3s ease;
    }
    .menu {
      list-style: none;
      margin: 0;
      padding: 0;
      display: flex;
    }
    .menu li {
      margin-right: 20px;
      cursor: pointer;
      padding: 5px;
      transition: color 0.3s ease;
    }
    .menu li:hover {
      text-decoration: underline;
    }
    
    /* Theme Toggle (iOS–style switch with icons) */
    .theme-toggle {
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    .theme-icon {
      width: 24px;
      height: 24px;
      vertical-align: middle;
    }
    .switch {
      position: relative;
      display: inline-block;
      width: 50px;
      height: 24px;
      margin-left: 10px;
    }
    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      transition: 0.2s ease;
      border-radius: 24px;
    }
    .slider:before {
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: 0.2s ease;
      border-radius: 50%;
    }
    input:checked + .slider {
      background-color: #66bb6a;
    }
    input:checked + .slider:before {
      transform: translateX(26px);
    }
    
    /* Container Styles */
    .container {
      padding: 20px;
      min-height: calc(100vh - 60px);
      transition: padding 0.3s ease;
    }
    .sections {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 20px;
      transition: all 0.3s ease;
    }
    .section {
      background-color: #1f1f1f;
      padding: 20px;
      border-radius: 8px;
      transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }
    .section h2 {
      margin-top: 0;
      transition: color 0.3s ease;
    }
    
    /* Dashboard Metric Subsections */
    .metrics {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-top: 10px;
    }
    .metric {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 10px;
      min-height: 90px; /* Ensure uniform height */
      transition: transform 0.3s ease;
    }
    .metric:hover {
      transform: scale(1.05);
    }
    .metric-label {
      font-size: 0.9em;
      margin-bottom: 5px;
      opacity: 0.8;
    }
    .metric-value {
      font-size: 3.5em;
      font-weight: bold;
      line-height: 1;
      margin: 0;
    }
    
    /* New Progress Bar Elements for Storage & Files Data */
    .progress-bar {
      margin-top: 15px;
    }
    .progress-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.85em;
      margin-bottom: 4px;
    }
    .progress-track {
      height: 8px;
      background-color: #444;
      border-radius: 4px;
      position: relative;
    }
    /* Default storage progress fill uses green */
    .progress-fill.storage {
      height: 100%;
      background-color: #66bb6a;
      border-radius: 4px;
      transition: width 0.3s ease;
    }
    /* Files shared progress fill uses blue (#037bfc) */
    .progress-fill.files {
      height: 100%;
      background-color: #037bfc;
      border-radius: 4px;
      transition: width 0.3s ease;
    }
    .progress-value {
      font-size: 0.9em;
      text-align: right;
      margin-top: 4px;
    }
    
    /* Light theme overrides with stronger colors */
    .light-theme body {
      background-color: #f0f0f0;
      color: #333;
    }
    .light-theme header {
      background-color: #e0e0e0;
    }
    .light-theme .section {
      color: #333;
      box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    }
    /* Strong accent colors for dashboard sections in light mode */
    .light-theme .section:nth-child(1) { background-color: #ffcccc; }
    .light-theme .section:nth-child(2) { background-color: #ccffcc; }
    .light-theme .section:nth-child(3) { background-color: #ccccff; }
    .light-theme .section:nth-child(4) { background-color: #ffffcc; }
    
    /* Form Elements */
    input[type="number"],
    input[type="range"] {
      width: 100%;
      padding: 8px;
      margin: 5px 0;
      border: 1px solid #333;
      border-radius: 4px;
      background-color: #333;
      color: #e0e0e0;
      transition: background-color 0.3s ease, color 0.3s ease;
    }
    .light-theme input[type="number"],
    .light-theme input[type="range"] {
      background-color: #fff;
      color: #333;
      border: 1px solid #ccc;
    }
    label {
      margin: 10px 0 5px;
      display: block;
    }
    #generatedPassword {
      margin-top: 10px;
      padding: 10px;
      background-color: #333;
      border-radius: 4px;
      word-break: break-all;
      font-weight: bold;
      transition: background-color 0.3s ease;
    }
    .light-theme #generatedPassword {
      background-color: #fff;
      border: 1px solid #ccc;
    }
    
    /* Slider tooltip positioned BELOW the slider */
    .range-container {
      position: relative;
      margin: 20px 0;
    }
    .range-tooltip {
      position: absolute;
      top: 30px;
      background: #333;
      color: #fff;
      padding: 3px 6px;
      border-radius: 4px;
      font-size: 12px;
      white-space: nowrap;
      transform: translateX(-50%);
      pointer-events: none;
      transition: background 0.3s ease, color 0.3s ease;
    }
    .light-theme .range-tooltip {
      background: #ccc;
      color: #333;
    }
    
    /* Settings View Styling */
    .settings-wrapper {
      display: flex;
      gap: 20px;
      transition: all 0.3s ease;
      height: calc(100vh - 60px);
    }
    .settings-menu {
      width: 300px;  /* Increased menu width */
      background: #1f1f1f;
      border-radius: 8px;
      padding: 10px;
      transition: background 0.3s ease;
      height: 100%;
    }
    .settings-menu ul {
      list-style: none;
      margin: 0;
      padding: 0;
    }
    .settings-menu li {
      margin-bottom: 10px;
      cursor: pointer;
      padding: 10px;
      border-radius: 4px;
      background: #333;
      transition: background 0.3s ease;
    }
    .settings-menu li:hover {
      background: #444;  /* Subtle lighter hover */
    }
    .settings-menu li.active {
      background: #444;  /* Slightly darker when active */
    }
    .settings-content {
      flex: 1;
      background: #1f1f1f;
      border-radius: 8px;
      padding: 20px;
      transition: background 0.3s ease, color 0.3s ease;
      height: 100%;
      overflow-y: auto;
    }
    .settings-content h3 {
      margin-top: 0;
    }
    .settings-section {
      margin-bottom: 20px;
    }
    .settings-section button, .settings-section input[type="button"] {
      padding: 8px 12px;
      margin-right: 10px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.3s ease, color 0.3s ease;
    }
    .settings-section button:hover, .settings-section input[type="button"]:hover {
      background: #66bb6a;
      color: #fff;
    }
    /* Settings overrides for light mode */
    .light-theme .settings-menu {
      background: #e0e0e0;
    }
    .light-theme .settings-menu li {
      background: #ccc;
      color: #333;
    }
    .light-theme .settings-content {
      background: #e0e0e0;
      color: #333;
    }
    
    /* View transitions (fade in/out) */
    .view {
      transition: opacity 0.3s ease-in-out;
    }
  </style>
</head>
<body>
  <header>
    <!-- Top Menu -->
    <ul class="menu">
      <li onclick="showView('dashboard')">Dashboard</li>
      <li onclick="alert('Logins view not implemented yet')">Logins</li>
      <li onclick="alert('Files view not implemented yet')">Files</li>
      <li onclick="showView('settings')">Settings</li>
    </ul>
    <!-- iOS‑style Theme Toggle with Sun/Moon Icons -->
    <div class="theme-toggle" onclick="toggleTheme()">
      <span id="themeIcon" class="theme-icon">
        <!-- Default to Moon icon (for dark mode) -->
        <svg viewBox="0 0 24 24" fill="#e0e0e0" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 12.79A9 9 0 0 1 11.21 3 7 7 0 1 0 21 12.79z"/>
        </svg>
      </span>
      <label class="switch">
        <input type="checkbox" id="themeSwitch" onchange="toggleTheme()">
        <span class="slider"></span>
      </label>
    </div>
  </header>
  
  <div class="container">
    <!-- Dashboard View -->
    <div id="dashboardView" class="view" style="opacity:1; display:block;">
      <div class="sections">
        <!-- Section 1: Password Data -->
        <div class="section">
          <h2>Password Data</h2>
          <div class="metrics">
            <div class="metric">
              <div class="metric-label">Reused Passwords</div>
              <div class="metric-value" id="reusedPasswords">12</div>
            </div>
            <div class="metric">
              <div class="metric-label">Exposed Passwords</div>
              <div class="metric-value" id="exposedPasswords">5</div>
            </div>
            <div class="metric">
              <div class="metric-label">Total Passwords</div>
              <div class="metric-value" id="totalPasswords">150</div>
            </div>
            <div class="metric">
              <div class="metric-label">Weak Passwords</div>
              <div class="metric-value" id="weakPasswords">20</div>
            </div>
          </div>
        </div>
  
        <!-- Section 2: Storage & Files Data -->
        <div class="section">
          <h2>Storage &amp; Files Data</h2>
          <div class="metrics">
            <div class="metric">
              <div class="metric-label">Total Files</div>
              <div class="metric-value" id="totalFiles">50</div>
            </div>
            <div class="metric">
              <div class="metric-label">Used Storage</div>
              <div class="metric-value" id="usedStorage">1.5GB</div>
            </div>
            <div class="metric">
              <div class="metric-label">Remaining Storage</div>
              <div class="metric-value" id="remainingStorage">8.5GB</div>
            </div>
            <div class="metric">
              <div class="metric-label">Files Shared</div>
              <div class="metric-value" id="filesShared">10</div>
            </div>
          </div>
          <!-- New Storage Progress Bar -->
          <div class="progress-bar">
            <div class="progress-label">
              <span class="left-label">0GB</span>
              <span class="right-label">10GB</span>
            </div>
            <div class="progress-track">
              <!-- 1.5GB used of 10GB ~ 15% width -->
              <div class="progress-fill storage" style="width: 15%;"></div>
            </div>
            <div class="progress-value">1.5GB used</div>
          </div>
          <!-- New Files Progress Bar -->
          <div class="progress-bar">
            <div class="progress-label">
              <span class="left-label">0</span>
              <span class="right-label">50</span>
            </div>
            <div class="progress-track">
              <!-- 10 shared of 50 total = 20% width -->
              <div class="progress-fill files" style="width: 20%;"></div>
            </div>
            <div class="progress-value">10 files shared</div>
          </div>
        </div>
  
        <!-- Section 3: Password Generator -->
        <div class="section">
          <h2>Password Generator</h2>
          <!-- Length Slider -->
          <label for="lengthInput">Length</label>
          <div class="range-container">
            <input type="range" id="lengthInput" value="12" min="1" max="20">
            <div class="range-tooltip" id="lengthTooltip">12</div>
          </div>
          
          <!-- Toggle Switches -->
          <div>
            <label for="includeLower">Include Lowercase</label>
            <label class="switch">
              <input type="checkbox" id="includeLower" checked>
              <span class="slider"></span>
            </label>
          </div>
          <div>
            <label for="includeUpper">Include Uppercase</label>
            <label class="switch">
              <input type="checkbox" id="includeUpper" checked>
              <span class="slider"></span>
            </label>
          </div>
          <div>
            <label for="includeNumbers">Include Numbers</label>
            <label class="switch">
              <input type="checkbox" id="includeNumbers" checked>
              <span class="slider"></span>
            </label>
          </div>
          <div>
            <label for="includeSymbols">Include Symbols</label>
            <label class="switch">
              <input type="checkbox" id="includeSymbols">
              <span class="slider"></span>
            </label>
          </div>
          <div id="generatedPassword">Your generated password will appear here.</div>
        </div>
  
        <!-- Section 4: Empty for Now -->
        <div class="section">
          <h2>Empty Section</h2>
          <p>Content coming soon...</p>
        </div>
      </div>
    </div>
    
    <!-- Settings View -->
    <div id="settingsView" class="view" style="opacity:0; display:none;">
      <div class="settings-wrapper">
        <!-- Vertical Settings Menu -->
        <div class="settings-menu">
          <ul>
            <li id="menuAccount" class="active" onclick="showSettingsTab('account')">Account</li>
            <li id="menuSecurity" onclick="showSettingsTab('security')">Security</li>
            <li id="menuStorage" onclick="showSettingsTab('storage')">Storage</li>
          </ul>
        </div>
        <!-- Settings Content Area -->
        <div class="settings-content">
          <!-- Account Tab -->
          <div id="tabAccount" class="settings-section">
            <h3>Account</h3>
            <p><strong>Email:</strong> user@example.com</p>
            <p><strong>Name:</strong> John Doe</p>
            <p><strong>Days Since Password Change:</strong> 45 days</p>
            <button onclick="alert('Signing out...')">Sign Out</button>
          </div>
          <!-- Security Tab -->
          <div id="tabSecurity" class="settings-section" style="display:none">
            <h3>Security</h3>
            <button onclick="alert('Change Password clicked')">Change Password</button>
            <div style="margin:10px 0">
              <label for="toggle2FA">Enable 2FA</label>
              <label class="switch">
                <input type="checkbox" id="toggle2FA">
                <span class="slider"></span>
              </label>
            </div>
            <button onclick="alert('Add Hardware Keys clicked')">Add Hardware Keys</button>
            <button onclick="alert('Change PIN Code clicked')">Change PIN Code</button>
          </div>
          <!-- Storage Tab -->
          <div id="tabStorage" class="settings-section" style="display:none">
            <h3>Storage</h3>
            <p>
              <strong>OneDrive:</strong>
              <button onclick="alert('Connect OneDrive')">Connect</button>
            </p>
            <p>
              <strong>Google Drive:</strong>
              Connected 
              <button onclick="alert('Disconnect Google Drive')">Disconnect</button>
            </p>
            <p>
              <strong>Megagz:</strong>
              <button onclick="alert('Connect Megagz')">Connect</button>
            </p>
            <p>
              <strong>Dropbox:</strong>
              <button onclick="alert('Connect Dropbox')">Connect</button>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <script>
    // Smooth view switching using fade transitions.
    function showView(view) {
      const dashView = document.getElementById('dashboardView');
      const setView = document.getElementById('settingsView');
      if (view === 'dashboard') {
        setView.style.opacity = 0;
        setTimeout(() => {
          setView.style.display = 'none';
          dashView.style.display = 'block';
          setTimeout(() => { dashView.style.opacity = 1; }, 20);
        }, 300);
      } else if (view === 'settings') {
        dashView.style.opacity = 0;
        setTimeout(() => {
          dashView.style.display = 'none';
          setView.style.display = 'block';
          setTimeout(() => {
            setView.style.opacity = 1;
            showSettingsTab('account');
          }, 20);
        }, 300);
      }
    }
    
    // Settings tab switcher.
    function showSettingsTab(tab) {
      document.getElementById('tabAccount').style.display = 'none';
      document.getElementById('tabSecurity').style.display = 'none';
      document.getElementById('tabStorage').style.display = 'none';
      
      document.getElementById('menuAccount').classList.remove('active');
      document.getElementById('menuSecurity').classList.remove('active');
      document.getElementById('menuStorage').classList.remove('active');
      
      if (tab === 'account'){
        document.getElementById('tabAccount').style.display = 'block';
        document.getElementById('menuAccount').classList.add('active');
      } else if (tab === 'security'){
        document.getElementById('tabSecurity').style.display = 'block';
        document.getElementById('menuSecurity').classList.add('active');
      } else if (tab === 'storage'){
        document.getElementById('tabStorage').style.display = 'block';
        document.getElementById('menuStorage').classList.add('active');
      }
    }
    
    // Theme toggle functionality.
    function toggleTheme() {
      const themeSwitch = document.getElementById('themeSwitch');
      const themeIcon = document.getElementById('themeIcon');
      if (themeSwitch.checked) {
        document.documentElement.classList.add('light-theme');
        // Fixed Sun icon with proper namespace and updated path data.
        themeIcon.innerHTML = `
          <svg viewBox="0 0 24 24" fill="#333" xmlns="http://www.w3.org/2000/svg">
            <path d="M6.76 4.84l-1.8-1.79-1.42 1.41 1.79 1.8 1.43-1.42zM17.24 4.84l1.8-1.79 1.42 1.41-1.79 1.8-1.43-1.42zM12 2h-1v3h1V2zM5 11H2v-1h3v1zm14 0h3v-1h-3v1zm-2.1 4.9l1.79 1.79-1.42 1.41-1.79-1.79 1.42-1.41zM6.32 16.32l1.42 1.41L6.95 19.5l-1.79-1.8 1.16-1.38zM12 19h1v3h-1v-3zM12 7a5 5 0 100 10 5 5 0 000-10z"/>
          </svg>`;
      } else {
        document.documentElement.classList.remove('light-theme');
        themeIcon.innerHTML = `
          <svg viewBox="0 0 24 24" fill="#e0e0e0" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 12.79A9 9 0 0 1 11.21 3 7 7 0 1 0 21 12.79z"/>
          </svg>`;
      }
    }
    
    // Password generator functionality.
    function generatePassword() {
      const length = parseInt(document.getElementById('lengthInput').value, 10);
      const includeLower = document.getElementById('includeLower').checked;
      const includeUpper = document.getElementById('includeUpper').checked;
      const includeNumbers = document.getElementById('includeNumbers').checked;
      const includeSymbols = document.getElementById('includeSymbols').checked;
      
      const lowerChars = 'abcdefghijklmnopqrstuvwxyz';
      const upperChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      const numbers = '0123456789';
      const symbols = '!@#$%^&*()_+~`|}{[]:;?><,./-=';
      let availableChars = '';
  
      if (includeLower) availableChars += lowerChars;
      if (includeUpper) availableChars += upperChars;
      if (includeNumbers) availableChars += numbers;
      if (includeSymbols) availableChars += symbols;
  
      if (!availableChars.length) return '';
  
      let password = '';
      for (let i = 0; i < length; i++) {
        password += availableChars.charAt(Math.floor(Math.random() * availableChars.length));
      }
      return password;
    }
    
    function updatePassword() {
      const password = generatePassword();
      document.getElementById('generatedPassword').innerText = password || 'Please select at least one character type.';
    }
    
    // Update slider tooltip.
    const lengthInput = document.getElementById('lengthInput');
    const lengthTooltip = document.getElementById('lengthTooltip');
    
    function updateLengthTooltip() {
      const val = lengthInput.value;
      lengthTooltip.innerText = val;
      const percent = (val - lengthInput.min) / (lengthInput.max - lengthInput.min);
      const sliderWidth = lengthInput.offsetWidth;
      lengthTooltip.style.left = (percent * sliderWidth) + 'px';
    }
    
    lengthInput.addEventListener('input', () => {
      updateLengthTooltip();
      updatePassword();
    });
    
    document.getElementById('includeLower').addEventListener('change', updatePassword);
    document.getElementById('includeUpper').addEventListener('change', updatePassword);
    document.getElementById('includeNumbers').addEventListener('change', updatePassword);
    document.getElementById('includeSymbols').addEventListener('change', updatePassword);
    
    // Initialize.
    updateLengthTooltip();
    updatePassword();
  </script>
</body>
</html>
