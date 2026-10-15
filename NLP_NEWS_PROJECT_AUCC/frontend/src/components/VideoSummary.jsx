import { useEffect, useState } from "react";
import { getVideoSummary } from "../api/client.js";
import AnalysisPanel from "./AnalysisPanel.jsx";

export default function VideoSummary({ videoId, language = "th" }) {
  const en = language === "en";
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    setLoading(true);
    setResult(null);
    setError(null);
    getVideoSummary(videoId)
      .then((data) => { if (active) setResult(data); })
      .catch((err) => { if (active) setError(err.response?.data?.detail || "ไม่สามารถสรุปเนื้อหาวิดีโอได้ กรุณาลองใหม่ / Unable to summarize this video."); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [videoId, attempt]);
  return <AnalysisPanel title={en ? "Video content summary" : "สรุปเนื้อหาในคลิป"}
    subtitle={en ? "Key points and the speaker's views, summarized from the video." : "ประเด็นสำคัญและมุมมองของผู้พูด สรุปจากเนื้อหาวิดีโอ"}>
    {loading && <p role="status" className="animate-pulse py-5 text-sm text-slate-500">{en ? "Reading and summarizing the video…" : "กำลังอ่านและสรุปเนื้อหาวิดีโอ…"}</p>}
    {error && <div role="alert" className="rounded-xl bg-amber-50 p-4 text-sm text-amber-900"><p>{error}</p><button type="button" onClick={() => setAttempt((n) => n + 1)} className="mt-3 rounded-lg border border-amber-300 px-3 py-2 font-semibold">{en ? "Try again" : "ลองใหม่"}</button></div>}
    {result && <div className="space-y-5 text-sm leading-7 text-slate-700">
      <p className="whitespace-pre-wrap">{result.overview}</p>
      {result.key_points?.length > 0 && <div><h3 className="mb-2 font-bold text-slate-900">{en ? "Key points" : "ในคลิปพูดถึงอะไรบ้าง"}</h3><ul className="list-disc space-y-1 pl-5">{result.key_points.map((point, index) => <li key={index}>{point}</li>)}</ul></div>}
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-xl bg-indigo-50 p-4"><h3 className="mb-2 font-bold text-indigo-950">{en ? "Team outlook and matchup" : "แนวโน้มของทีมและการพบคู่แข่ง"}</h3><p className="whitespace-pre-wrap">{result.outlook}</p></div>
        <div className="rounded-xl bg-sky-50 p-4"><h3 className="mb-2 font-bold text-sky-950">{en ? "Plans and responses discussed" : "แผนการเล่นและการรับมือที่กล่าวถึง"}</h3><p className="whitespace-pre-wrap">{result.tactics}</p></div>
      </div>
      <a href={`https://www.youtube.com/watch?v=${encodeURIComponent(videoId)}`} target="_blank" rel="noreferrer" className="inline-block text-xs font-medium text-indigo-700 underline">{en ? "Source: watch the original video" : "แหล่งข้อมูล: ดูวิดีโอต้นฉบับ"}</a>
    </div>}
  </AnalysisPanel>;
}
