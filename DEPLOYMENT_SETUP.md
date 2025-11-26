# Netlify Deployment Setup

This project is configured for automatic deployment to Netlify via GitHub Actions.

## Required GitHub Secrets

You need to add the following secrets to your GitHub repository:

### 1. NETLIFY_AUTH_TOKEN
1. Go to Netlify Dashboard → User Settings → Applications
2. Click "New access token"
3. Copy the token
4. Add to GitHub: Repository → Settings → Secrets and variables → Actions → New repository secret
   - Name: `NETLIFY_AUTH_TOKEN`
   - Value: (paste your token)

### 2. NETLIFY_SITE_ID
1. Go to your Netlify site → Site settings → General
2. Copy the "Site ID" (under Site information)
3. Add to GitHub: Repository → Settings → Secrets and variables → Actions → New repository secret
   - Name: `NETLIFY_SITE_ID`
   - Value: (paste your site ID)

## How It Works

- Every push to `main` branch triggers automatic deployment
- GitHub Actions builds the project (`npm run build`)
- The `dist` folder is deployed to Netlify
- Build logs are visible in GitHub Actions tab

## Manual Deployment (Alternative)

If you prefer manual deployment:

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod --dir=dist
```

## Site URL
Once configured, your site will be available at:
`https://bibliacatolica2.netlify.app` (or your custom domain)
