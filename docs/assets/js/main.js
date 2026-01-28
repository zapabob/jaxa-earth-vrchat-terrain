// ============================================
// JAXA Earth API → VRChat Terrain Generator
// GitHub Pages - Main JavaScript
// ============================================

// Language data
const translations = {
  ja: {
    // Navigation
    'nav-home': 'ホーム',
    'nav-setup': 'セットアップ',
    'nav-features': '機能',
    'nav-docs': 'ドキュメント',
    
    // Hero
    'hero-title': 'JAXAの衛星データから\nVRChatワールドの地形を自動生成',
    'hero-subtitle': 'JAXA Earth APIの地球観測データを、Blender/Unity/VRChatで使える3D地形に変換するMCPサーバー',
    'hero-cta': '始める',
    'hero-cta-secondary': 'GitHubで見る',
    
    // Features
    'feature-1-title': '🛰️ 衛星データ取得',
    'feature-1-desc': 'JAXAの標高、地表面温度、植生指数など様々なデータにアクセス',
    'feature-2-title': '🎮 VRChat最適化',
    'feature-2-desc': 'ポリゴン数・テクスチャサイズを自動調整してVRChat向けに最適化',
    'feature-3-title': '🎨 Blender/Unity対応',
    'feature-3-desc': 'ワンクリックでエクスポート、すぐに使える形式で出力',
    'feature-4-title': '💬 自然言語操作',
    'feature-4-desc': '「富士山周辺の地形をVRChat用にエクスポートして」と話すだけ',
    'feature-5-title': '🔧 Cursor/Codex対応',
    'feature-5-desc': 'お好みのIDEで利用可能、設定は自動認識',
    'feature-6-title': '📊 統計計算',
    'feature-6-desc': '空間統計・時間統計を自動計算してデータを分析',
    
    // Setup
    'setup-title': 'セットアップガイド',
    'setup-subtitle': '5分で始められる簡単セットアップ',
    'setup-prereq-title': '前提条件',
    'setup-prereq-desc': '以下のソフトウェアがインストールされている必要があります',
    'setup-step-1-title': 'リポジトリをクローン',
    'setup-step-1-desc': 'GitHubからリポジトリをクローンします',
    'setup-step-2-title': '依存関係をインストール',
    'setup-step-2-desc': 'uvまたはpipを使用して必要なパッケージをインストールします',
    'setup-step-3-title': 'IDE設定',
    'setup-step-3-desc': 'CursorまたはCodex IDEでMCPサーバーを設定します',
    'setup-step-4-title': '動作確認',
    'setup-step-4-desc': 'IDEでMCPサーバーが正しく動作するか確認します',
    'setup-method-1': '方法1: uvを使用（推奨）',
    'setup-method-2': '方法2: pipを使用',
    'setup-cursor-title': 'Cursor IDE設定',
    'setup-cursor-desc': 'プロジェクトルートに<code>.cursor/mcp.json</code>ファイルが既に作成されています。Cursor IDEを再起動すると、自動的にMCPサーバーが認識されます。',
    'setup-cursor-manual': '手動設定が必要な場合:',
    'setup-cursor-note': '注意: <code>C:\\path\\to\\jaxa-earth-vrchat-terrain</code> を実際のプロジェクトパスに置き換えてください。',
    'setup-codex-title': 'Codex IDE設定',
    'setup-codex-desc': 'プロジェクトルートに<code>.codex/mcp.json</code>ファイルが既に作成されています。Codex IDEを再起動すると、自動的にMCPサーバーが認識されます。',
    'setup-codex-manual': '手動設定が必要な場合:',
    'setup-verify-1': 'IDEを完全に再起動します',
    'setup-verify-2': 'Agentモードまたはチャット機能を開きます',
    'setup-verify-3': '以下のコマンドを試してください：',
    'setup-verify-success': '正常に動作していれば、コレクションの一覧が表示されます。',
    
    // Usage
    'usage-title': '使用例',
    'usage-basic-title': '基本的な使用例',
    'usage-vrchat-title': 'VRChat向け使用例',
    'usage-search-title': 'コレクション検索',
    'usage-image-title': '画像表示',
    'usage-heightmap-title': '高度マップ生成',
    'usage-blender-title': 'Blender用エクスポート',
    'usage-unity-title': 'Unity用エクスポート',
    'usage-optimize-title': 'VRChat向け最適化',
    
    // Documentation
    'docs-title': 'ドキュメント',
    'docs-readme-title': '📖 README',
    'docs-readme-desc': 'プロジェクトの概要と詳細なドキュメント',
    'docs-quickstart-title': '🚀 クイックスタート',
    'docs-quickstart-desc': '5分で始める簡単ガイド',
    'docs-workflow-title': '🎬 VRChat/Blenderワークフロー',
    'docs-workflow-desc': '詳細なステップバイステップガイド',
    'docs-official-title': '📚 JAXA公式ドキュメント',
    'docs-official-desc': 'JAXA Earth API公式ドキュメント',
    
    // Code blocks
    'code-copy': 'コピー',
    'code-copied': 'コピーしました！',
    
    // Footer
    'footer-text': 'Made with ❤️ for VRChat creators and 3D artists',
    'footer-license': 'MIT License',
    'footer-contribute': '貢献',
  },
  en: {
    // Navigation
    'nav-home': 'Home',
    'nav-setup': 'Setup',
    'nav-features': 'Features',
    'nav-docs': 'Docs',
    
    // Hero
    'hero-title': 'Transform JAXA Satellite Data\ninto VRChat Worlds',
    'hero-subtitle': 'Convert JAXA Earth API observation data into 3D terrain for Blender/Unity/VRChat with an MCP server',
    'hero-cta': 'Get Started',
    'hero-cta-secondary': 'View on GitHub',
    
    // Features
    'feature-1-title': '🛰️ Satellite Data Access',
    'feature-1-desc': 'Access various JAXA data including elevation, land surface temperature, and vegetation index',
    'feature-2-title': '🎮 VRChat Optimization',
    'feature-2-desc': 'Automatically optimize polygon count and texture size for VRChat',
    'feature-3-title': '🎨 Blender/Unity Support',
    'feature-3-desc': 'One-click export in ready-to-use formats',
    'feature-4-title': '💬 Natural Language',
    'feature-4-desc': 'Just say "Export terrain around Mount Fuji for VRChat"',
    'feature-5-title': '🔧 Cursor/Codex Support',
    'feature-5-desc': 'Works with your favorite IDE, auto-detected configuration',
    'feature-6-title': '📊 Statistical Analysis',
    'feature-6-desc': 'Automatically calculate spatial and temporal statistics',
    
    // Setup
    'setup-title': 'Setup Guide',
    'setup-subtitle': 'Get started in 5 minutes',
    'setup-prereq-title': 'Prerequisites',
    'setup-prereq-desc': 'The following software must be installed',
    'setup-step-1-title': 'Clone Repository',
    'setup-step-1-desc': 'Clone the repository from GitHub',
    'setup-step-2-title': 'Install Dependencies',
    'setup-step-2-desc': 'Install required packages using uv or pip',
    'setup-step-3-title': 'IDE Configuration',
    'setup-step-3-desc': 'Configure MCP server in Cursor or Codex IDE',
    'setup-step-4-title': 'Verify Installation',
    'setup-step-4-desc': 'Verify that the MCP server works correctly in your IDE',
    'setup-method-1': 'Method 1: Using uv (Recommended)',
    'setup-method-2': 'Method 2: Using pip',
    'setup-cursor-title': 'Cursor IDE Configuration',
    'setup-cursor-desc': 'The <code>.cursor/mcp.json</code> file has already been created in the project root. Restart Cursor IDE and the MCP server will be automatically recognized.',
    'setup-cursor-manual': 'If manual configuration is needed:',
    'setup-cursor-note': 'Note: Replace <code>C:\\path\\to\\jaxa-earth-vrchat-terrain</code> with your actual project path.',
    'setup-codex-title': 'Codex IDE Configuration',
    'setup-codex-desc': 'The <code>.codex/mcp.json</code> file has already been created in the project root. Restart Codex IDE and the MCP server will be automatically recognized.',
    'setup-codex-manual': 'If manual configuration is needed:',
    'setup-verify-1': 'Completely restart your IDE',
    'setup-verify-2': 'Open Agent mode or chat functionality',
    'setup-verify-3': 'Try the following command:',
    'setup-verify-success': 'If it works correctly, a list of collections will be displayed.',
    
    // Usage
    'usage-title': 'Usage Examples',
    'usage-basic-title': 'Basic Usage Examples',
    'usage-vrchat-title': 'VRChat Usage Examples',
    'usage-search-title': 'Collection Search',
    'usage-image-title': 'Image Display',
    'usage-heightmap-title': 'Heightmap Generation',
    'usage-blender-title': 'Blender Export',
    'usage-unity-title': 'Unity Export',
    'usage-optimize-title': 'VRChat Optimization',
    
    // Documentation
    'docs-title': 'Documentation',
    'docs-readme-title': '📖 README',
    'docs-readme-desc': 'Project overview and detailed documentation',
    'docs-quickstart-title': '🚀 Quick Start',
    'docs-quickstart-desc': 'Get started in 5 minutes',
    'docs-workflow-title': '🎬 VRChat/Blender Workflow',
    'docs-workflow-desc': 'Detailed step-by-step guide',
    'docs-official-title': '📚 JAXA Official Documentation',
    'docs-official-desc': 'JAXA Earth API official documentation',
    
    // Code blocks
    'code-copy': 'Copy',
    'code-copied': 'Copied!',
    
    // Footer
    'footer-text': 'Made with ❤️ for VRChat creators and 3D artists',
    'footer-license': 'MIT License',
    'footer-contribute': 'Contribute',
  }
};

// Current language
let currentLang = localStorage.getItem('lang') || 'ja';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initLanguageToggle();
  initScrollEffects();
  initCodeCopy();
  updateLanguage(currentLang);
});

// Language toggle
function initLanguageToggle() {
  const toggleButtons = document.querySelectorAll('.lang-toggle button');
  toggleButtons.forEach(button => {
    button.addEventListener('click', () => {
      const lang = button.dataset.lang;
      setLanguage(lang);
    });
  });
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('lang', lang);
  updateLanguage(lang);
  
  // Update active button
  document.querySelectorAll('.lang-toggle button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
}

function updateLanguage(lang) {
  document.querySelectorAll('[data-i18n]').forEach(element => {
    const key = element.dataset.i18n;
    if (translations[lang] && translations[lang][key]) {
      const translation = translations[lang][key];
      if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
        element.value = translation;
      } else {
        // Handle <br> tags in translations (replace \n with <br>)
        if (translation.includes('\n')) {
          element.innerHTML = translation.replace(/\n/g, '<br>');
        } else {
          element.textContent = translation;
        }
      }
    }
  });
  
  // Update HTML lang attribute
  document.documentElement.lang = lang;
}

// Scroll effects
function initScrollEffects() {
  const header = document.querySelector('.header');
  let lastScroll = 0;
  
  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
  });
  
  // Fade in on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
      }
    });
  }, observerOptions);
  
  document.querySelectorAll('.card, .feature-card, .step').forEach(el => {
    observer.observe(el);
  });
}

// Code copy functionality
function initCodeCopy() {
  document.querySelectorAll('.code-block-copy').forEach(button => {
    button.addEventListener('click', async () => {
      const codeBlock = button.closest('.code-block').querySelector('pre code');
      const text = codeBlock.textContent;
      
      try {
        await navigator.clipboard.writeText(text);
        const originalText = button.textContent;
        button.textContent = translations[currentLang]['code-copied'] || 'Copied!';
        button.style.color = 'var(--color-success)';
        
        setTimeout(() => {
          button.textContent = originalText;
          button.style.color = '';
        }, 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
      }
    });
  });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});
