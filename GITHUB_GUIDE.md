# Publish this portfolio on GitHub Pages (about 10 minutes)

## Option A: website upload (no tools needed)
1. Sign in at github.com (create a free account if needed).
2. Click **+** (top right) > **New repository**.
3. Name it `tithi-singh-portfolio`, set it to **Public**, tick **Add a README file**, click **Create repository**.
4. Click **Add file > Upload files**. Unzip this package and drag in `index.html`, `.nojekyll`, `GITHUB_GUIDE.md` and the `src` folder. (If `.nojekyll` is hidden on your computer, skip it; the site works without it.) Click **Commit changes**. Upload `README.md` too, replacing the default one.
5. Go to **Settings > Pages**. Under **Build and deployment**, set Source to **Deploy from a branch**, Branch **main**, folder **/ (root)**, then **Save**.
6. Wait 1 to 2 minutes and refresh. The site is at `https://YOUR-USERNAME.github.io/tithi-singh-portfolio/`.

## Option B: command line
```bash
cd tithi_site
git init -b main
git add .
git commit -m "Add finance portfolio"
git remote add origin https://github.com/YOUR-USERNAME/tithi-singh-portfolio.git
git push -u origin main
```
Then do step 5 above.

## Make it yours
- Add your email, LinkedIn and GitHub URLs to `src/profile.json`, or send them to Claude to regenerate the page.
- Pin the repository on your GitHub profile and add the link to your resume and LinkedIn Featured section.
- Optional custom domain: Settings > Pages > Custom domain.

## Tips for recruiters
- Put the live link in the first line of your resume and LinkedIn headline.
- In interviews, walk through the DCF sliders: base value, what the price implies (reverse DCF) and what would change your mind.
