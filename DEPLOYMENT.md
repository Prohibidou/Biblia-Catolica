# 📖 Biblia Católica - Deployment Guide

## 🚀 Desplegada en Netlify

Tu aplicación de la Biblia Católica está lista para ser desplegada gratuitamente en Netlify.

### Archivos del Build

- **Carpeta de producción**: `dist/`
- **Tamaño total**: ~2.5 MB
- **Contenido**:
  - Aplicación React compilada (~330 KB JS + ~4 KB CSS)
  - Base de datos Navarra SQLite comprimida (~2.4 MB)

### Opción 1: Netlify Drop (Más Rápido) ✨

1. Ve a [https://app.netlify.com/drop](https://app.netlify.com/drop)
2. Arrastra la carpeta `dist` desde tu explorador de archivos
3. ¡Listo! Tu sitio estará en línea en segundos
4. Netlify te dará una URL como: `https://random-name-12345.netlify.app`

### Opción 2: Netlify CLI

```bash
# 1. Instalar Netlify CLI (si no está instalado)
npm install -g netlify-cli

# 2. Login a Netlify
netlify login

# 3. Desplegar el sitio
netlify deploy --prod --dir=dist
```

### Opción 3: Deploy desde GitHub

1. Sube tu código a GitHub
2. Conecta el repositorio con Netlify
3. Configuración de build:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
4. Deploy automático en cada push

## 📊 Especificaciones

- **Framework**: React + Vite
- **Tipo**: Single Page Application (SPA)
- **Hosting compatible**: Netlify, Vercel, GitHub Pages, Cloudflare Pages
- **Peso optimizado**: ~2.5 MB total (incluye toda la Biblia de Navarra)

## 🔧 Comandos útiles

```bash
# Desarrollo local
npm run dev

# Build de producción
npm run build

# Preview del build
npm run preview
```

## 🌐 URL de ejemplo

Una vez desplegado, tu Biblia estará accesible en una URL como:
`https://biblia-catolica-navarra.netlify.app`

¡Puedes personalizarla en la configuración de Netlify!
