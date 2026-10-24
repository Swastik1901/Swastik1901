<h1 align="center">Swastik Kumar</h1>

<p align="center">
  Full-stack developer &nbsp;·&nbsp; Privacy &nbsp;·&nbsp; Networking &nbsp;·&nbsp; Web
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/swastik-kumar19"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:vardaan1901@gmail.com"><img src="https://img.shields.io/badge/Email-1f2328?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>
</p>

<br>

I'm a B.Tech student in Artificial Intelligence & Machine Learning at Heritage Institute of Technology, Patna. I like building at the intersection of **privacy, networking and the web**, the kind of projects where you have to understand what's happening on the wire, not just in the UI.

<br>

## Currently

| | |
|---|---|
| **Building** | Privacy-enforcing tools and web experiences |
| **Exploring** | TypeScript, 3D on the web (Three.js + Blender), applied AI |
| **Ask me about** | Full-stack development, Node.js, MongoDB, MITM proxies, open source |

<br>

## Featured project

### [Sentin-AL](https://github.com/Swastik1901/sentin-al) — privacy-enforcing proxy platform

> What if websites had to *pay you* for your data?

A privacy-first MITM proxy that intercepts HTTP/HTTPS traffic and runs a custom **Data Lease Negotiation Protocol**: a site must agree on a lease price before it receives data such as your location, device fingerprint or browsing activity.

```mermaid
flowchart LR
    B[Browser] -->|HTTPS request| P{{Sentin-AL Proxy}}
    P -->|lease offer| W[Website]
    W -->|pays rate-card price| P
    P -->|real data| W
    W -.->|refuses| D[Data poisoning]
    D -.->|fake GPS + fingerprint + UA| W
    P --> M[(MongoDB rate cards)]
    P --> L[Live dashboard + wallet]
```

- **Data poisoning:** if a site refuses to pay, synthetic noise (fake GPS, randomized fingerprints, spoofed user agents) keeps your real data private.
- **Rate cards:** MongoDB-backed, per-domain pricing across 20+ major websites.
- **Live dashboard and wallet:** track transactions and claim privacy earnings in real time.
- **On-the-fly TLS:** per-host certificates generated with node-forge to inspect HTTPS traffic.

<p>
  <img src="https://img.shields.io/badge/Node.js-1f2328?style=flat-square&logo=nodedotjs&logoColor=5FA04E" alt="Node.js">
  <img src="https://img.shields.io/badge/Express-1f2328?style=flat-square&logo=express&logoColor=white" alt="Express">
  <img src="https://img.shields.io/badge/MongoDB-1f2328?style=flat-square&logo=mongodb&logoColor=47A248" alt="MongoDB">
  <img src="https://img.shields.io/badge/Socket.io-1f2328?style=flat-square&logo=socketdotio&logoColor=white" alt="Socket.io">
  <img src="https://img.shields.io/badge/node--forge-1f2328?style=flat-square" alt="node-forge">
  <img src="https://img.shields.io/badge/http--mitm--proxy-1f2328?style=flat-square" alt="http-mitm-proxy">
</p>

<br>

## Tech stack

<p>
  <img src="https://img.shields.io/badge/HTML-1f2328?style=flat-square&logo=html5&logoColor=E34F26" alt="HTML">
  <img src="https://img.shields.io/badge/CSS-1f2328?style=flat-square&logo=css3&logoColor=1572B6" alt="CSS">
  <img src="https://img.shields.io/badge/JavaScript-1f2328?style=flat-square&logo=javascript&logoColor=F7DF1E" alt="JavaScript">
  <img src="https://img.shields.io/badge/TypeScript-1f2328?style=flat-square&logo=typescript&logoColor=3178C6" alt="TypeScript">
  <img src="https://img.shields.io/badge/Node.js-1f2328?style=flat-square&logo=nodedotjs&logoColor=5FA04E" alt="Node.js">
  <img src="https://img.shields.io/badge/Express-1f2328?style=flat-square&logo=express&logoColor=white" alt="Express">
  <img src="https://img.shields.io/badge/MongoDB-1f2328?style=flat-square&logo=mongodb&logoColor=47A248" alt="MongoDB">
  <img src="https://img.shields.io/badge/Python-1f2328?style=flat-square&logo=python&logoColor=3776AB" alt="Python">
  <img src="https://img.shields.io/badge/Three.js-1f2328?style=flat-square&logo=threedotjs&logoColor=white" alt="Three.js">
  <img src="https://img.shields.io/badge/Blender-1f2328?style=flat-square&logo=blender&logoColor=E87D0D" alt="Blender">
  <img src="https://img.shields.io/badge/Git-1f2328?style=flat-square&logo=git&logoColor=F05032" alt="Git">
  <img src="https://img.shields.io/badge/Postman-1f2328?style=flat-square&logo=postman&logoColor=FF6C37" alt="Postman">
  <img src="https://img.shields.io/badge/Google%20Cloud-1f2328?style=flat-square&logo=googlecloud&logoColor=4285F4" alt="Google Cloud">
</p>

<br>

## Recognition

| Event | Result |
|---|---|
| Smart Bengal Hackathon 2025 | Finalist, Team Lead |
| Hack n Solve, IGDTUW | Finalist |

<br>

## Open source & community

- **GirlScript Summer of Code 2024:** first open-source experience, contributed to Postman
- **ECSoC 2026:** contributor
- **Google Student Ambassador (2025)**
- **GDG on Campus, Heritage Institute of Technology:** member
- **Pull Shark** achievement on GitHub

<br>

## Certifications

<p>
  <img src="https://img.shields.io/badge/Career%20Essentials%20in%20Generative%20AI-Microsoft%20%26%20LinkedIn-1f2328?style=flat-square" alt="Career Essentials in Generative AI">
  <img src="https://img.shields.io/badge/Postman%20API%20Fundamentals-Student%20Expert-1f2328?style=flat-square" alt="Postman API Fundamentals">
  <img src="https://img.shields.io/badge/AI%20Fluency-Anthropic-1f2328?style=flat-square" alt="AI Fluency">
  <img src="https://img.shields.io/badge/Claude%20101-Anthropic-1f2328?style=flat-square" alt="Claude 101">
</p>

<br>

## Activity

<p align="center">
  <img src="profile-3d-contrib/profile-3d.svg" alt="3D contribution graph" width="100%">
</p>

<p align="center">
  <sub>Open to collaborating on privacy, web and open-source projects.</sub>
</p>
