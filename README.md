<!-- Panels are generated: python3 scripts/gen_assets.py (same palette / type / glass as pixshaft.com). -->

<div align="center">

<a href="https://pixshaft.com"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/hero.svg" width="100%" alt="Ikura — I build Shaft: the whole of Pixiv, in your pocket."></a>

[![Stars](https://img.shields.io/github/stars/CeuiLiSA/Pixiv-Shaft?style=for-the-badge&logo=github&color=f5c842&labelColor=07060f&label=Pixiv-Shaft)](https://github.com/CeuiLiSA/Pixiv-Shaft)
[![Release](https://img.shields.io/github/v/release/CeuiLiSA/Pixiv-Shaft?style=for-the-badge&logo=android&color=3ddc84&labelColor=07060f&label=latest)](https://github.com/CeuiLiSA/Pixiv-Shaft/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/CeuiLiSA/Pixiv-Shaft/total?style=for-the-badge&color=7c6cff&labelColor=07060f)](https://github.com/CeuiLiSA/Pixiv-Shaft/releases)
[![Google Play](https://img.shields.io/badge/Google_Play-PixShaft-22d3ee?style=for-the-badge&logo=googleplay&logoColor=white&labelColor=07060f)](https://play.google.com/store/apps/details?id=ceui.pixiv.pshaft)
[![Website](https://img.shields.io/badge/pixshaft.com-f6339a?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=07060f)](https://pixshaft.com)

</div>

<a href="https://pixshaft.com"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/marquee.svg" width="100%" alt="What Shaft does — illustrations, manga, novels, rankings, FANBOX, pixiv COMIC, cloud sync, remote config, in-app push, trending API, web discover…"></a>

<br>

<img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/h-stack.svg" width="100%" alt="The Shaft stack — one app, one backend, one website">

<table>
<tr>
<td width="33.3%"><a href="https://github.com/CeuiLiSA/Pixiv-Shaft"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/card-app.svg" width="100%" alt="Pixiv-Shaft — the Android client"></a></td>
<td width="33.3%"><a href="https://pixshaft.com"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/card-api.svg" width="100%" alt="pixshaft-api — the backend behind pixshaft.com"></a></td>
<td width="33.3%"><a href="https://pixshaft.com/web"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/card-web.svg" width="100%" alt="shaft-web — pixshaft.com and the web discover page"></a></td>
</tr>
</table>

<details>
<summary><b>How the three fit together</b> · 三者怎么配合</summary>
<br>

```mermaid
flowchart LR
    subgraph device["📱 Android"]
        app["<b>Pixiv-Shaft</b><br/>Kotlin · Material You"]
    end
    subgraph cloud["☁️ pixshaft.com"]
        api["<b>pixshaft-api</b><br/>Hono · SQLite<br/>sync · config · plans"]
        events["<b>shaft-api-v2</b><br/>Hono · WebSocket<br/>events · trending"]
        web["<b>shaft-web</b><br/>Next.js · React<br/>landing · web discover"]
    end
    pixiv[("pixiv.net<br/>official API")]

    app -- "signed REST" --> api
    app -- "REST / WS" --> events
    app -- "direct" --> pixiv
    web -. "guestbook" .-> api
```

- **Pixiv-Shaft** talks to pixiv directly for content, and to pixshaft.com only for the things pixiv can't give it: cloud-synced settings, remote config, in-app push, plans.
- **pixshaft-api** is a single Node 22 process (Hono + better-sqlite3 in WAL mode, pm2, behind Caddy). Requests are HMAC-signed by the app; every route is rate-limited. **shaft-api-v2** sits beside it for community events and trending, with a WebSocket channel and a React admin console.
- **shaft-web** is the Next.js 16 site at pixshaft.com — the landing page and the `/web` discover page. Both backends and the site are private repos for now; the running product is the public part.

<sub>Pixiv-Shaft 直连 pixiv 拿内容，只把 pixiv 给不了的事交给 pixshaft.com：设置云同步、远程配置、应用内推送、订阅。pixshaft-api 是单进程 Node 22（Hono + better-sqlite3 WAL，pm2，Caddy 前置），请求由 app 侧 HMAC 签名、逐路由限流；shaft-api-v2 负责社区事件与热榜，带 WebSocket 与 React 管理台。shaft-web 是 pixshaft.com 的 Next.js 16 官网 + `/web` 网页端发现页。后端与官网目前私有，线上产品本身是公开的那部分。</sub>

</details>

<br>

<img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/h-bench.svg" width="100%" alt="Also on the bench">

<table>
<tr>
<td width="33.3%"><a href="https://github.com/SoxiaLiSA/StackSwipe"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/bench-stackswipe.svg" width="100%" alt="StackSwipe — iOS-style app switcher for Jetpack Compose"></a></td>
<td width="33.3%"><a href="https://github.com/SoxiaLiSA/pixiv-login"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/bench-login.svg" width="100%" alt="pixiv-login — Android library for Pixiv OAuth 2.0 (PKCE)"></a></td>
<td width="33.3%"><a href="https://github.com/SoxiaLiSA/Shaft"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/bench-shaft-ios.svg" width="100%" alt="Shaft — SwiftUI prototype"></a></td>
</tr>
</table>

<br>

<img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/h-toolbox.svg" width="100%" alt="Under the hood">

<div align="center">

<a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=kotlin,androidstudio,gradle,cpp,ts,nextjs,react,tailwind,nodejs,sqlite,swift,git&theme=dark&perline=12" alt="Kotlin · Android Studio · Gradle · C++ · TypeScript · Next.js · React · Tailwind · Node.js · SQLite · Swift · Git"></a>

<br><br>

<img src="https://streak-stats.demolab.com?user=SoxiaLiSA&theme=dark&hide_border=true&background=07060F&ring=7C6CFF&fire=22D3EE&currStreakLabel=A78BFA&currStreakNum=FFFFFF&sideNums=FFFFFF&sideLabels=D9D4FF&dates=8B8B9E&stroke=1F1B33&border_radius=16" height="170" alt="Contribution streak">

</div>

<br>

<a href="https://pixshaft.com"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/cta.svg" width="100%" alt="Start browsing Pixiv the Shaft way — Google Play · GitHub Releases · pixshaft.com"></a>

<div align="center">
<sub>
<a href="https://play.google.com/store/apps/details?id=ceui.pixiv.pshaft">Google Play</a> ·
<a href="https://github.com/CeuiLiSA/Pixiv-Shaft/releases/latest">GitHub Releases</a> ·
<a href="https://pixshaft.com">pixshaft.com</a> ·
<a href="https://pixshaft.com/web">Web discover</a> ·
💗 <a href="https://afdian.com/a/pixshaft">afdian.com/a/pixshaft</a>
&nbsp;&nbsp;|&nbsp;&nbsp; 📍 Tokyo · ずっと真夜中でいいのに
</sub>
</div>
