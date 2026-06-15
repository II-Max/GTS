// =============================================================================
// GTS (Go to Success) - Auth Check Script
// Script này được include ở các trang yêu cầu đăng nhập (problems, solve, etc.)
// Tự động kiểm tra auth state và chuyển hướng nếu chưa đăng nhập
// =============================================================================

(function() {
    // Kiểm tra xem Firebase đã init chưa
    if (typeof firebase === 'undefined') {
        console.error('Firebase not loaded! Make sure firebase-app.js and firebase-auth.js are included first.');
        return;
    }

    // Inject CSS cho user menu
    const css = `
        .neo-navbar {
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 24px; background: rgba(10, 13, 20, 0.95);
            border-bottom: 1px solid rgba(0,243,255,0.1);
            position: sticky; top: 0; z-index: 100;
            backdrop-filter: blur(10px);
        }
        .neo-navbar .brand {
            font-size: 1.2rem; font-weight: 800;
            background: linear-gradient(135deg, #00f3ff, #b300ff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; letter-spacing: 2px; text-decoration: none;
        }
        .neo-navbar .nav-links { display: flex; gap: 20px; align-items: center; }
        .neo-navbar .nav-links a {
            color: #6b7a8f; text-decoration: none; font-size: 0.8rem;
            letter-spacing: 1px; transition: color 0.3s;
        }
        .neo-navbar .nav-links a:hover { color: #00f3ff; }
        
        .neo-user-menu {
            display: flex; align-items: center; gap: 12px; cursor: pointer;
            position: relative; padding: 6px 12px; border-radius: 6px;
            transition: background 0.3s;
        }
        .neo-user-menu:hover { background: rgba(255,255,255,0.05); }
        .neo-user-menu img {
            width: 32px; height: 32px; border-radius: 50%;
            border: 1px solid rgba(0,243,255,0.3);
        }
        .neo-user-menu .name {
            color: #c8d6e5; font-size: 0.8rem; max-width: 120px;
            overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
        }
        .neo-user-menu .dropdown {
            display: none; position: absolute; top: 100%; right: 0;
            background: rgba(10, 13, 20, 0.98); border: 1px solid rgba(0,243,255,0.15);
            border-radius: 8px; min-width: 200px; padding: 8px 0;
            margin-top: 8px; backdrop-filter: blur(10px);
        }
        .neo-user-menu .dropdown.show { display: block; }
        .neo-user-menu .dropdown a {
            display: flex; align-items: center; gap: 10px;
            padding: 10px 16px; color: #c8d6e5; text-decoration: none;
            font-size: 0.8rem; transition: all 0.2s;
        }
        .neo-user-menu .dropdown a:hover {
            background: rgba(0,243,255,0.05); color: #00f3ff;
        }
        .neo-user-menu .dropdown .divider {
            height: 1px; background: rgba(255,255,255,0.05); margin: 4px 0;
        }
        .neo-user-menu .dropdown .logout {
            color: #ff0055;
        }
        .neo-user-menu .dropdown .logout:hover { background: rgba(255,0,85,0.1); color: #ff3377; }
    `;

    const styleEl = document.createElement('style');
    styleEl.textContent = css;
    document.head.appendChild(styleEl);

    // ======================================================================
    // Auth check
    // ======================================================================
    const auth = firebase.auth();
    const currentUser = localStorage.getItem('neo_user');
    
    auth.onAuthStateChanged(user => {
        if (!user) {
            // Chưa đăng nhập - kiểm tra xem có user trong localStorage không
            if (!currentUser) {
                // Redirect đến trang đăng nhập
                const currentPath = window.location.pathname.split('/').pop();
                if (currentPath !== 'login.html' && currentPath !== 'index.html') {
                    window.location.href = 'login.html?redirect=' + encodeURIComponent(currentPath);
                }
            }
        } else {
            // Đã đăng nhập - lưu thông tin
            localStorage.setItem('neo_user', JSON.stringify({
                uid: user.uid,
                email: user.email,
                display_name: user.displayName,
                avatar: user.photoURL,
            }));
        }
    });

    // ======================================================================
    // Hàm inject navbar cho các trang con
    // ======================================================================
    window.NeoNavbar = {
        inject: function() {
            const user = JSON.parse(localStorage.getItem('neo_user') || '{}');
            
            // Kiểm tra xem navbar đã được inject chưa
            if (document.querySelector('.neo-navbar')) return;

            const navbar = document.createElement('div');
            navbar.className = 'neo-navbar';
            navbar.innerHTML = `
                <a href="problems.html" class="brand">GTS</a>
                <div class="nav-links">
                    <a href="problems.html">BÀI TẬP</a>
                    <a href="contest.html">THI ĐẤU</a>
                    <a href="rank.html">XẾP HẠNG</a>
                    <a href="history.html">LỊCH SỬ</a>
                    <div class="neo-user-menu" onclick="NeoNavbar.toggleDropdown(event)">
                        <img src="${user.avatar || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(user.display_name || 'User') + '&background=00f3ff&color=05070a&size=32'}" 
                             alt="avatar" onerror="this.src='https://ui-avatars.com/api/?name=U&background=00f3ff&color=05070a&size=32'">
                        <span class="name">${user.display_name || user.email || 'User'}</span>
                        <div class="dropdown" id="userDropdown">
                            <a href="history.html"><span>📊</span> Lịch sử làm bài</a>
                            <a href="rank.html"><span>🏆</span> Bảng xếp hạng</a>
                            <div class="divider"></div>
                            <a class="logout" onclick="NeoNavbar.logout()"><span>🚪</span> Đăng xuất</a>
                        </div>
                    </div>
                </div>
            `;

            // Thêm vào đầu body
            document.body.insertBefore(navbar, document.body.firstChild);
        },

        toggleDropdown: function(event) {
            event.stopPropagation();
            document.getElementById('userDropdown').classList.toggle('show');
        },

        logout: function() {
            auth.signOut().then(() => {
                localStorage.removeItem('neo_user');
                localStorage.removeItem('neo_token');
                window.location.href = 'login.html';
            });
        }
    };

    // Close dropdown when clicking outside
    document.addEventListener('click', function() {
        const dropdown = document.getElementById('userDropdown');
        if (dropdown) dropdown.classList.remove('show');
    });

    console.log('%c🔐 Auth Check Active', 'color: #00ff88; font-size: 12px;');
})();
