# 家庭互動模式整理 — GitHub Pages

將 `content/article.md` 轉成可公開閱讀的靜態網頁，部署於 GitHub Pages。

## 本機預覽

```bash
cd c:\gh\dad-page
python build.py
python -m http.server 8080
```

瀏覽器開啟：<http://localhost:8080>

修改 `content/article.md` 後，請重新執行 `python build.py` 再部署。

## 部署到 GitHub Pages（使用另一個 GitHub 帳號）

以下步驟需要在你想使用的 **那個 GitHub 帳號** 下操作。若本機 `git push` 時登入的是別的帳號，請先切換帳號或改用 SSH key / Personal Access Token。

### 1. 在 GitHub 建立新 repository

1. 登入你要用的 GitHub 帳號（瀏覽器請確認右上角頭像是否正確）。
2. 建立新 repo，例如名稱：`dad-page`（可自訂）。
3. 建議設為 **Public**（免費 GitHub Pages 需公開 repo，除非你有 GitHub Pro）。

### 2. 本機推送到該 repo

在專案資料夾執行（將 `YOUR_USER` 換成你的帳號名稱）：

```bash
cd c:\gh\dad-page
git init
git add .
git commit -m "Add GitHub Pages site for family interaction article"
git branch -M main
git remote add origin https://github.com/YOUR_USER/dad-page.git
git push -u origin main
```

**登入說明：** 第一次 `git push` 時，Windows 可能會跳出 GitHub 登入視窗或要求 Personal Access Token。請使用 **要建立 Pages 的那個帳號** 登入，不要用錯帳號。

### 3. 開啟 GitHub Pages

1. 到 repo 頁面 → **Settings** → **Pages**
2. **Build and deployment** → Source 選 **Deploy from a branch**
3. Branch 選 `main`，資料夾選 **`/ (root)`**
4. 儲存後約 1–3 分鐘，網址會出現：

   `https://YOUR_USER.github.io/dad-page/`

## 專案結構

| 路徑 | 說明 |
|------|------|
| `content/article.md` | 文章原始 Markdown |
| `build.py` | 產生 `index.html` |
| `index.html` | 部署用首頁（由 build 產生） |
| `assets/css/main.css` | 版型與重點樣式 |
| `assets/js/main.js` | 目錄捲動高亮 |

## 樣式說明

- 頂部：標題與免責說明區塊
- 左側（桌機）：章節目錄，捲動時自動標示目前段落
- **粗體獨立段落**：金黃色重點框（`key-point`）
- 引用區塊：灰／藍色說明框
- 第一章 10 點特徵：獨立高亮清單
# dad-page
