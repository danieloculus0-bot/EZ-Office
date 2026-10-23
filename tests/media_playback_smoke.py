"""Exercise actual local media decoding and timeline progression, not just <video>/<audio> controls.
CI uses ffmpeg ONLY to create realistic test files. EZ-Office has zero runtime codec/tool dependencies.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
import wave

from playwright.sync_api import sync_playwright, expect, TimeoutError as PlaywrightTimeoutError

ROOT=Path(__file__).resolve().parents[1]
PAGE=(ROOT/"index.html").as_uri()

def run_ffmpeg(*args):
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",*args]
    subprocess.run(cmd,check=True,timeout=40)

def fixtures(folder):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is required to CREATE fixtures for this CI test only; not for app playback")
    mp4=folder/"sample.mp4"
    run_ffmpeg("-f","lavfi","-i","testsrc=size=64x64:rate=8:duration=2",
               "-f","lavfi","-i","sine=frequency=440:sample_rate=16000:duration=2",
               "-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",
               "-profile:v","baseline","-crf","36","-c:a","aac","-b:a","32k",
               "-movflags","+faststart","-shortest",str(mp4))
    webm=folder/"sample.webm"
    run_ffmpeg("-f","lavfi","-i","testsrc=size=64x64:rate=8:duration=2",
               "-f","lavfi","-i","sine=frequency=440:sample_rate=16000:duration=2",
               "-c:v","libvpx","-deadline","realtime","-cpu-used","8","-b:v","65k",
               "-c:a","libopus","-b:a","24k","-shortest",str(webm))
    mp3=folder/"sample.mp3"
    run_ffmpeg("-f","lavfi","-i","sine=frequency=440:sample_rate=16000:duration=2",
               "-c:a","libmp3lame","-q:a","7",str(mp3))
    wav=folder/"sample.wav"
    with wave.open(str(wav),"wb") as sound:
        sound.setnchannels(1);sound.setsampwidth(2);sound.setframerate(16000)
        sound.writeframes(bytes(16000*2*2))
    for file in (mp4,webm,mp3,wav):
        assert file.stat().st_size>250,(file,file.stat().st_size)
    return [("video/webm; codecs=\"vp8, opus\"",webm),
            ("video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"",mp4)], \
           [("audio/mpeg",mp3),("audio/wav",wav)]

def choose_file(page,path):
    with page.expect_file_chooser() as dialog:
        page.get_by_role("button",name="Open media").click()
    dialog.value.set_files(str(path))

def playback(page,file,kind):
    choose_file(page,file)
    element=page.locator(".media-stage "+kind)
    expect(element).to_have_count(1)
    page.wait_for_function("""kind=>{
      const el=document.querySelector('.media-stage '+kind);
      return !!el&&(el.readyState>=1||!!el.error);
    }""",arg=kind,timeout=10000)
    error=element.evaluate("(el)=>el.error?.code ?? 0")
    if error:
        return (False,"media error "+str(error)+": "+page.locator(".media-playback-state").inner_text())
    duration=element.evaluate("el=>el.duration")
    if duration<1.5:
        return (False,"metadata duration wrong "+str(duration))
    if kind=="video":
        dims=element.evaluate("el=>[el.videoWidth,el.videoHeight]")
        if min(dims)<=0:return (False,"video dimensions missing: "+str(dims))
        assert element.evaluate("el=>el.playsInline")
    page.get_by_role("button",name="Play / Pause").click()
    try:
        page.wait_for_function("""kind=>{
          const el=document.querySelector('.media-stage '+kind);
          return el&&el.currentTime>0.3;
        }""",arg=kind,timeout=8000)
    except PlaywrightTimeoutError:
        return (False,"timeline did not progress: "+page.locator(".media-playback-state").inner_text())
    if element.evaluate("el=>el.paused") is False:
        page.get_by_role("button",name="Play / Pause").click()
    assert page.get_by_role("button",name="← 10s").is_enabled()
    assert page.get_by_role("button",name="10s →").is_enabled()
    assert element.evaluate("el=>el.currentTime")>0
    return (True,"decoded and advanced timeline")

def main():
    with tempfile.TemporaryDirectory(prefix="ez-media-real-") as temp:
        video,audio=fixtures(Path(temp))
        with sync_playwright() as playwright:
            for engine in (playwright.chromium,playwright.webkit):
                browser=engine.launch(headless=True)
                page=browser.new_page(viewport={"width":390,"height":844},
                    device_scale_factor=2,is_mobile=True,has_touch=True)
                page.goto(PAGE)
                assert page.evaluate("EZOffice.inspect().current")=="home"
                page.locator('[data-tool="media"]').click()
                expect(page.get_by_role("button",name="Play / Pause")).to_be_disabled()
                page.get_by_role("button",name="Check formats").click()
                expect(page.get_by_role("region",name="Native format support")).to_contain_text("MP4")
                assert page.get_by_role("button",name="Open media").is_visible()
                results={}
                for mime,file in video+audio:
                    kind="video" if mime.startswith("video") else "audio"
                    # Tests only claim format support where the actual browser advertises decoding.
                    claimed=page.evaluate("""args=>document.createElement(args.kind).canPlayType(args.mime)""",
                                          {"kind":kind,"mime":mime})
                    if not claimed:
                        results[file.suffix]=(False,"browser does not advertise "+mime)
                        continue
                    results[file.suffix]=playback(page,file,kind)
                assert results[".wav"][0],(engine.name,results)
                assert any(results[file.suffix][0] for _,file in video),(engine.name,results)
                assert any(results[file.suffix][0] for _,file in audio),(engine.name,results)

                # No hidden decoder was loaded. Native <video>/<audio> owns playback.
                scripts=page.locator("script[src]").evaluate_all(
                    "elements=>elements.map(el=>el.getAttribute('src'))")
                assert all(not s.startswith(("https:","http:")) for s in scripts),scripts
                page.get_by_role("button",name="Close media").click()
                expect(page.locator(".media-stage audio,.media-stage video")).to_have_count(0)
                assert page.get_by_role("button",name="Play / Pause").is_disabled()
                assert "Media released" in page.locator(".media-playback-state").inner_text()
                print("NATIVE_MEDIA_PLAYBACK_PASS",engine.name,results)
                browser.close()

if __name__=="__main__":
    main()
