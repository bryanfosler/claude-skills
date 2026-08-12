---
name: stream-transcript
description: Pull a Teams meeting transcript out of the SharePoint/Stream web player in Chrome, with speaker labels, and land it on disk as a VTT. Use this whenever a Teams transcript is needed but the Microsoft Graph route is unavailable — the M365 connector returns 403 `GraphAccessToTranscriptsDisabled` (a tenant-wide admin policy — common in enterprise tenants), the recording is over the connector's 100 MB fetch cap, the meeting was an ad-hoc call with no calendar event, or the user pastes a `stream.aspx` / Teams recap link and says "grab the transcript", "copy the transcript from the browser", or "pull the VTT". Also the fallback for `/meeting-notes` Phase 1.3 when a transcript fetch fails. Produces a speaker-labeled `<v Name>` VTT without any manual export.
---

# stream-transcript — pull a labeled VTT from the Stream player

Graph transcript access can be closed off while the **SharePoint/Stream REST API stays open**, because it authenticates as the user's browser session rather than as the connector. This skill uses that path.

Everything runs as `fetch()` **inside the page** via `mcp__claude-in-chrome__javascript_tool`. You are not reading rendered text off the screen and not scrolling a virtualized list — you are calling the same API the player calls, and lifting the player's own in-memory turn data.

Use **`claude-in-chrome`**, not the in-app Browser: this needs the user's real logged-in SharePoint session.

## What you need to start

A `stream.aspx` URL for the recording. The user can paste it from the Teams recap ("Copy link" on the recording), or you can find the recording in the organizer's OneDrive `Recordings` folder. The URL's `id=` parameter is the server-relative path to the `.mp4`.

## Why there are two data sources (read this before you start)

The recording exposes the transcript **twice**, and they are not equivalent:

| | `media/transcripts` VTT | Stream player turn data |
|---|---|---|
| Speaker labels | **none** — no `<v>` tags at all | **yes** — `speakerDisplayName` per turn |
| Timing | millisecond | second |
| Granularity | ~1,559 cues (90-min meeting) | ~838 speaker turns |
| Reached by | REST call | React fiber walk |

**Use the turn data.** Speaker attribution is worth far more than millisecond timing for meeting notes, and the text is otherwise the same.

Do **not** try to graft speakers from the turn data onto the ms-precision cues by time-matching. That was tried and it drifts: second-resolution turn starts don't align to cue boundaries, turns merge multiple cues, and boundary cues get misattributed. Verified failure — 5 of 8 sampled turns misaligned. Build the VTT straight from the turns.

## Procedure

### 1. Open the recording

`navigate` to the `stream.aspx` URL, then screenshot to confirm it loaded and you're authenticated. Open the **Transcript** panel if it isn't already open (right-side rail) — the panel must render at least once for step 4 to work, because that's what populates the React state.

### 2. Resolve driveId + itemId

Run in-page, substituting the organizer's personal site path and the `.mp4` server-relative path from the URL's `id=`:

```js
const base='/personal/rtarver_sram_com';
const p='/personal/rtarver_sram_com/Documents/Recordings/<FILE>.mp4';
const d=await fetch(base+'/_api/v2.1/drive',{headers:{accept:'application/json'}}).then(r=>r.json());
const f=await fetch(base+"/_api/web/GetFileByServerRelativePath(decodedurl='"+p.replace(/'/g,"''")+"')?$select=UniqueId,Name,Length",{headers:{accept:'application/json;odata=nometadata'}}).then(r=>r.json());
JSON.stringify({driveId:d.id, file:f})
```

This works **cross-account** — the file does not need to be in the user's own OneDrive. Note `Length`: if it's over ~100 MB, that confirms why the connector's file read would have failed.

### 3. Confirm a transcript exists

```js
const b='/personal/<ORG>/_api/v2.1/drives/<driveId>/items/<itemId>';
window.__b=b;
const r=await fetch(b+'/media/transcripts',{headers:{accept:'application/json'}});
window.__tj=r.ok?await r.json():null;
JSON.stringify({status:r.status, n:window.__tj?.value?.length, ids:window.__tj?.value?.map(v=>({id:v.id,lang:v.languageTag,size:v.size}))})
```

If this 404s or returns an empty `value`, Teams hasn't finalized the transcript yet — for a meeting that just ended, wait and retry rather than concluding none exists.

The unlabeled VTT, if you ever want it, is the entry's **`temporaryDownloadUrl`** (ignore `displayName`, which ends in `.json` but returns VTT), or `/media/transcripts/{id}/content` with `Accept: text/vtt`. The `/streamContent?format=text/vtt` variant returns 400 — don't bother. **For normal use skip this entirely and go to step 4.**

### 4. Lift the speaker-labeled turns from React state

The player holds the full attributed transcript in a component's props. Walk up the fiber tree from a DOM node containing known cue text:

```js
function fk(n){return Object.keys(n).find(k=>k.startsWith('__reactFiber$'))}
const el=[...document.querySelectorAll('div')].find(d=>/<A PHRASE FROM THE FIRST CUE>/.test(d.textContent)&&d.textContent.length<400);
let f=el[fk(el)],ent=null,h=0;
while(f&&h<40){
  for(const bag of[f.memoizedProps,f.memoizedState]){
    if(bag&&typeof bag==='object'){for(const[k,v]of Object.entries(bag)){
      if((k==='entries'||k==='items')&&Array.isArray(v)&&v.length>100&&v[0]?.speakerDisplayName!==undefined)ent=v;
    }}}
  if(ent)break; f=f.return; h++;
}
window.__ent=ent;
const sp={}; ent.forEach(e=>sp[e.speakerDisplayName||'(none)']=(sp[e.speakerDisplayName||'(none)']||0)+1);
JSON.stringify({n:ent.length, speakers:sp, types:[...new Set(ent.map(e=>e.type))], first:ent[0].timestamp, last:ent[ent.length-1].timestamp})
```

Turn shape: `speakerDisplayName`, `speakerId`, `text`, `timestamp`, `endTime`, `type`, `entryId`, `roomDisplayName`, `speakerType`. Timestamps are ISO-8601 durations (`PT1H29M59S`). `type` is `Text` or `StopEvent` — drop `StopEvent` and empty-text turns.

Sanity-check the returned `speakers` map and the first/last timestamps against the meeting's real length before continuing. If `ent` is null, the transcript panel probably never rendered — go back to step 1.

### 5. Build the VTT and save it

`endTime` is sometimes ≤ `timestamp` from rounding (~15% of turns), so clamp: `end = max(endTime, start+1)`, then cap at the next turn's start so cues don't overlap.

Do **not** return the transcript body as tool output — a 90-minute meeting is ~120 KB and would flood context. Write it to disk with a blob + `<a download>` click, then verify from the shell.

```js
const dur=s=>{const m=/^PT(?:(\d+)H)?(?:(\d+)M)?(?:([\d.]+)S)?$/.exec(s||'');return m?(+(m[1]||0))*3600+(+(m[2]||0))*60+(+(m[3]||0)):null};
const T=window.__ent.filter(e=>e.type==='Text'&&e.speakerDisplayName&&e.text?.trim())
  .map(e=>({t:dur(e.timestamp),e:dur(e.endTime),sp:e.speakerDisplayName,txt:e.text.trim().replace(/\s+/g,' ')}));
const fmt=s=>{const h=Math.floor(s/3600),m=Math.floor(s%3600/60),x=Math.floor(s%60);
  return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(x).padStart(2,'0')+'.000'};
const body=T.map((e,i)=>{let end=Math.max(e.e,e.t+1); const nx=T[i+1]?T[i+1].t:null;
  if(nx!==null&&end>nx&&nx>e.t)end=nx;
  return (i+1)+'\n'+fmt(e.t)+' --> '+fmt(end)+'\n<v '+e.sp+'>'+e.txt+'</v>'});
const out='WEBVTT\n\n'+body.join('\n\n')+'\n';
const a=document.createElement('a');
a.href=URL.createObjectURL(new Blob([out],{type:'text/vtt'}));
a.download='<YYYY-MM-DD>-<Slug>.vtt';
document.body.appendChild(a);a.click();a.remove();
JSON.stringify({turns:T.length,len:out.length,sample:out.split('\n\n').slice(1,3)})
```

Then confirm from the shell — never assume the download landed:

```bash
ls -l ~/Downloads/<name>.vtt && grep -o '<v [^>]*>' ~/Downloads/<name>.vtt | sort | uniq -c | sort -rn
```

### 6. Verify coverage before you trust it

Fetch the unlabeled VTT (step 3) and compare normalized word counts against the turn text. They should match within a handful of words — the turn data de-duplicates the occasional stuttered repeat, which is the expected delta. A large gap means the React state held only a partially loaded window, and you should re-open the panel and re-lift.

## Hard-won gotchas

- **The harness output filter blanks any tool result containing query strings or cookie-ish data.** `performance.getEntriesByType('resource')` comes back as `[BLOCKED: Cookie/query string data]`, and so does any result echoing a signed URL. Stash bodies and URLs on `window` and return only sanitized scalars — lengths, counts, ids, short sanitized samples.
- **Network-URL discovery via a `fetch`/XHR monkey-patch does not work here.** By the time you can install the hook the panel data is already cached, and re-opening the panel refetches nothing but telemetry. The fiber walk is the reliable route.
- **Cue-ID prefixes are not speaker ids.** Every cue in the unlabeled VTT shares one GUID prefix with a sequence suffix (`<guid>/9-0`). Don't try to derive speakers from them.
- **Don't click around the Stream chrome to spot-check.** Panel state shifts and stale coordinates land on other controls — a verification click once opened the **Share** dialog. Verify from the extracted data and the shell, not by clicking. If a share/send dialog ever opens, close it immediately and say so; never send.
- Clean up: close any tab you opened with `tabs_close_mcp`.

## Handing off to /meeting-notes

Once the VTT is on disk, `/meeting-notes` Phase 2 takes over unchanged: single segment, no recurring-URI scoring, `target-segment: 0`, no date warning. In the transcript file's blockquote, record that the VTT came from the Stream player (and why Graph wasn't used), and whether speakers are labeled.

If a note was already written from an **unlabeled** VTT, don't just swap the transcript — the summary's attributions were guesses. Re-run a verification pass over the note against the labeled transcript and correct owners and who-argued-what. On 2026-08-06 that pass corrected 12 of 68 attributed claims, including who volunteered for a role and one "decision" that never happened.

## Related

- `~/.claude/skills/meeting-notes/SKILL.md` — the pipeline this feeds
- Memory: `graph-transcripts-disabled-tenant` — the 403 and current tenant state
