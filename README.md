<div align="center">

<a href="https://pixshaft.com"><img src="https://raw.githubusercontent.com/SoxiaLiSA/SoxiaLiSA/main/assets/hero.svg" width="100%" alt="Ikura — I build Shaft: the whole of Pixiv, in your pocket."></a>

<sub>在做 Shaft：一个开源的 Pixiv 第三方安卓客户端，以及它背后的云端服务与官网。</sub>

[![Website](https://img.shields.io/badge/pixshaft.com-7c5cff?style=for-the-badge&logo=googlechrome&logoColor=white)](https://pixshaft.com)
[![Google Play](https://img.shields.io/badge/Google_Play-PixShaft-3ddc84?style=for-the-badge&logo=googleplay&logoColor=white)](https://play.google.com/store/apps/details?id=ceui.pixiv.pshaft)
[![Stars](https://img.shields.io/github/stars/CeuiLiSA/Pixiv-Shaft?style=for-the-badge&logo=github&color=f5c842&label=Pixiv-Shaft)](https://github.com/CeuiLiSA/Pixiv-Shaft)
[![Release](https://img.shields.io/github/v/release/CeuiLiSA/Pixiv-Shaft?style=for-the-badge&logo=android&color=3ddc84&label=latest)](https://github.com/CeuiLiSA/Pixiv-Shaft/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/CeuiLiSA/Pixiv-Shaft/total?style=for-the-badge&color=e74c3c)](https://github.com/CeuiLiSA/Pixiv-Shaft/releases)


</div>

<br>

## 🧩 The Shaft stack

One app, one backend, one website — designed together so each can stay small.<br>
<sub>一个 app、一套后端、一个官网，三件事一起设计，各自才能保持精简。</sub>

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

<table>
<tr>
<td width="33%" valign="top">

### 📱 Pixiv-Shaft
**The client.** Illustrations, manga, novels, rankings, FANBOX and pixiv COMIC in one Android app — Material You, direct connection in mainland China, no ads. Plus on-device AI: super-resolution, smart cut-out, manga translation (OCR + MT) and RIFE ugoira interpolation.

<sub>插画 / 漫画 / 小说 / 排行榜 / FANBOX / pixiv COMIC 全都有；端侧 AI 超分、抠图、漫画翻译、动图补帧。</sub>

`Kotlin` `Java` `Coroutines` `Room` `Retrofit` `Glide` `ONNX Runtime` `C++/JNI`

[Source](https://github.com/CeuiLiSA/Pixiv-Shaft) · [Releases](https://github.com/CeuiLiSA/Pixiv-Shaft/releases/latest) · [Google Play](https://play.google.com/store/apps/details?id=ceui.pixiv.pshaft)

</td>
<td width="33%" valign="top">

### ☁️ pixshaft-api
**The backend behind pixshaft.com.** Cloud sync for settings, mute lists and download config; browse history; remote config and in-app push; plans with automatic Afdian fulfilment; curated Prime tag shelves. HMAC-signed requests, per-route rate limiting, single-process SQLite in WAL mode.

<sub>设置 / 屏蔽名单 / 下载配置的云同步、浏览历史、远程配置与应用内推送、订阅与爱发电自动发货。</sub>

`Node 22` `Hono` `better-sqlite3` `pino` `pm2` `Caddy`

Companion: **shaft-api-v2** — community events + trending API with a React admin console.

🔒 private for now · live at [pixshaft.com](https://pixshaft.com)

</td>
<td width="33%" valign="top">

### 🌐 shaft-web
**The website.** [pixshaft.com](https://pixshaft.com): a motion-heavy landing page (bento features, showcase, pricing, FAQ, guestbook) and a web **discover** page at [/web](https://pixshaft.com/web) with switchable skins and a login flow.

<sub>官网落地页（特性 / 界面 / 订阅 / FAQ / 留言板）＋ 网页端「发现」页，可换皮肤，带登录流程。</sub>

`Next.js 16` `React 19` `TypeScript` `Tailwind v4` `motion` `GSAP` `Lenis`

🔒 private for now · live at [pixshaft.com](https://pixshaft.com)

</td>
</tr>
</table>

<br>

## 🧪 Also on the bench

- [**StackSwipe**](https://github.com/SoxiaLiSA/StackSwipe) — iOS-style app switcher for Jetpack Compose with physics-based animations
- [**pixiv-login**](https://github.com/SoxiaLiSA/pixiv-login) — Android library for Pixiv OAuth 2.0 login (PKCE), one dependency via JitPack
- [**Shaft**](https://github.com/SoxiaLiSA/Shaft) — a SwiftUI prototype of Shaft (discover feed, detail, token refresh); a full iOS client is in progress privately

<br>

## 🛠️ Toolbox

![Kotlin](https://img.shields.io/badge/Kotlin-7f52ff?style=flat-square&logo=kotlin&logoColor=white)
![Android](https://img.shields.io/badge/Android-3ddc84?style=flat-square&logo=android&logoColor=white)
![Jetpack Compose](https://img.shields.io/badge/Jetpack_Compose-4285f4?style=flat-square&logo=jetpackcompose&logoColor=white)
![C++](https://img.shields.io/badge/C%2B%2B-00599c?style=flat-square&logo=cplusplus&logoColor=white)
![ONNX](https://img.shields.io/badge/ONNX_Runtime-005ced?style=flat-square&logo=onnx&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178c6?style=flat-square&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232a?style=flat-square&logo=react&logoColor=61dafb)
![Tailwind](https://img.shields.io/badge/Tailwind-06b6d4?style=flat-square&logo=tailwindcss&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Hono](https://img.shields.io/badge/Hono-e36002?style=flat-square&logo=hono&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003b57?style=flat-square&logo=sqlite&logoColor=white)
![Swift](https://img.shields.io/badge/Swift-f05138?style=flat-square&logo=swift&logoColor=white)

<br>

<div align="center">

<sub>💗 Shaft is free and open source. If it saves you a scroll or two: <a href="https://afdian.com/a/pixshaft">afdian.com/a/pixshaft</a></sub>

</div>
