// =============================================================================
// GTS (Go to Success) - Firebase Configuration
// Cấu hình chung cho tất cả các trang frontend
// =============================================================================

const firebaseConfig = {
  apiKey: "AIzaSyAom_YsJkuimVBo5OzXHtiUCrsxKyQY89k",
  authDomain: "gtsv2-a93c5.firebaseapp.com",
  databaseURL: "https://gtsv2-a93c5-default-rtdb.firebaseio.com",
  projectId: "gtsv2-a93c5",
  storageBucket: "gtsv2-a93c5.firebasestorage.app",
  messagingSenderId: "1045981371372",
  appId: "1:1045981371372:web:97d332c92337ecaf103ec9",
  measurementId: "G-YPCKKWNM17"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.database();

// =============================================================================
// API Base URL
// =============================================================================
const API_BASE = 'http://localhost:5000/api';

// =============================================================================
// Utility Functions
// =============================================================================

function showError(message) {
    const toast = document.getElementById('toast') || createToast();
    toast.textContent = message;
    toast.className = 'toast error';
    toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', 4000);
}

function showSuccess(message) {
    const toast = document.getElementById('toast') || createToast();
    toast.textContent = message;
    toast.className = 'toast success';
    toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', 3000);
}

function createToast() {
    const toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = `
        position: fixed; top: 20px; right: 20px; z-index: 9999;
        padding: 15px 25px; border-radius: 5px; font-family: 'JetBrains Mono', monospace;
        font-size: 14px; display: none; max-width: 400px;
    `;
    document.body.appendChild(toast);
    return toast;
}

function showLoading(show) {
    const loader = document.getElementById('loading') || createLoading();
    loader.style.display = show ? 'flex' : 'none';
}

function createLoading() {
    const div = document.createElement('div');
    div.id = 'loading';
    div.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(5, 7, 10, 0.9); z-index: 9998;
        display: none; justify-content: center; align-items: center;
        font-family: 'JetBrains Mono', monospace; color: #00f3ff;
    `;
    div.innerHTML = `
        <div style="text-align: center;">
            <div style="width: 50px; height: 50px; border: 3px solid rgba(0,243,255,0.3);
                border-top-color: #00f3ff; border-radius: 50%; animation: spin 1s infinite; margin: 0 auto 20px;"></div>
            <div>ĐANG XỬ LÝ...</div>
        </div>
        <style>@keyframes spin { to { transform: rotate(360deg); } }</style>
    `;
    document.body.appendChild(div);
    return div;
}

// Toast style injection
const toastStyle = document.createElement('style');
toastStyle.textContent = `
    .toast.error { background: #ff0055; color: white; border: 1px solid #ff3377; box-shadow: 0 0 20px rgba(255,0,85,0.5); }
    .toast.success { background: #00cc66; color: white; border: 1px solid #33ff88; box-shadow: 0 0 20px rgba(0,204,102,0.5); }
`;
document.head.appendChild(toastStyle);
