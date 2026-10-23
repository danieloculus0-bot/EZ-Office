# EZ-Office Media • native playback compatibility

## Playback architecture (Pass 03, October 2026)

EZ Media plays local files using the built-in HTML \`<audio>\` and \`<video>\` controls. It creates a temporary \`blob:\` URL for the selected file, streams it through the browser media engine, and revokes the URL when the media is closed or the user switches tools. **No CDN, browser extension, JavaScript codec bundle, FFmpeg executable, online conversion service, or separate desktop player is required by the app.**

The browser/operating system still needs a compatible decoder. There is no practical lightweight way to decode *every* video format on every browser with zero underlying media codecs. EZ-Office detects advertised format support, requests actual metadata, starts playback only after the user presses Play, and displays clear errors when decoding fails.

## Proven native playback

CI generates short actual media files using FFmpeg **only as a test fixture generator, not an EZ-Office application dependency**. Playwright drives the actual browser media elements, checks that the audio/video playback clock advances, and for video verifies that drawing the decoded frame to a Canvas returns nonblank image data.

| Container / encoding | Playwright Chromium (Linux) | Playwright WebKit (Linux) |
| --- | --- | --- |
| WebM VP8 + Opus video | Real playback validated | Real playback validated |
| MP4 H.264 baseline + AAC video | Browser did not advertise support; not claimed | Real playback validated |
| MP3 | Real playback validated | Real playback validated |
| PCM WAV | Real playback validated | Real playback validated |

These describe **CI Linux browser builds**, not all releases of Chrome, Safari, iOS, or venvWin hardware. Format support varies by engine and the container's internal encoding. New CI receipts supersede old ones.

EZ Slides uses the same browser-native playback engine for embedded video and audio (stored inside its \`.ezslides\` file). Its preview now offers a user-initiated **Play / Pause slide media** button, native controls and a visible unsupported-codec message. Automated tests verify embedded playback too.

## Recommended media files

- Video for portable/browser-first use: **WebM (VP8 + Opus)** when available, or **MP4 (H.264 + AAC)** when your target browser advertises and actually supports it.
- Audio: **MP3** for wide compatibility; **PCM WAV** for dependable uncompressed decoding.
- MOV, MKV, FLAC, AC3, DTS, HEVC, AV1 and other formats may or may not play natively, even if the file extension is recognized. Browser support for a container is not a guarantee about all codecs inside that container.
- EZ Media's **Check formats** button shows \`canPlayType()\` estimates and **does not pretend to have verified playback** until the actual file decodes and progresses.
- Large videos are handled as \`blob:\` object URLs without copying whole file bytes into JavaScript. Embedded slide videos are currently size-limited and saved inside a JSON data URL; use EZ Media for normal large videos.

## venvWin deployment reality

WebKitGTK's native multimedia stack uses **GStreamer**. To deliver out-of-the-box playback on a future minimal venvWin install, the chosen browser image/distro must already have the required media framework/decoder coverage. **This pass does not install or bundle Linux codec packages into venvWin** or verify the actual Jetson/vEnvWin machine. The user should not have to install a long list of media tools just to operate EZ-Office; the supported media path should be included in the base system image and checked in an on-device acceptance run.

Target hardware acceptance cases: open MP3 and WAV with audible sound; open MP4 H.264/AAC and WebM VP8/Opus with picture **and** sound; seek and pause; switch tools and check playback stops; reopen a different file; verify downloaded original bytes; watch RAM after long playback. Any unsupported format should display a clear explanation, not masquerade as "Ready."

## Limitations and safety

No codec conversion/transcoding; no DRM bypass; no EME/Widevine installation; no external playback server. The app only consumes explicitly selected local files. Camera/webcam capture and playlists are not implemented. Hardware speaker output and real iPhone Safari are not measurable in cloud CI; tests verify decoding and timelines in browser instances, not physical speakers.
