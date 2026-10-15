import AnalysisPanel, { percent } from "./AnalysisPanel.jsx";
const names = { athlete: ["นักกีฬา", "Athletes"], team: ["ทีม / สโมสร", "Team"], coach_tactics: ["โค้ชและแผนการเล่น", "Coaching & tactics"], referee: ["กรรมการ", "Refereeing"], competition: ["การแข่งขัน", "Competition"], performance: ["ผลงานการเล่น", "Performance"], injury: ["อาการบาดเจ็บ", "Injuries"], ranking: ["อันดับการแข่งขัน", "Rankings"], transfer: ["การย้ายทีม", "Transfers"], venue_tickets: ["สนามและบัตรเข้าชม", "Venue & tickets"], broadcast_fans: ["การถ่ายทอดและแฟนกีฬา", "Broadcast & fans"], other: ["อื่น ๆ", "Other"] };
export default function TopicChart({ data, language = "th", selectedTopic = null, onSelectTopic }) {
  const en = language === "en";
  const items = (data?.categories || []).map((c) => ({ key: c.category, name: names[c.category]?.[en ? 1 : 0] || c.category, value: c.percentage })).sort((a, b) => b.value - a.value);
  return <AnalysisPanel title={en ? "Topics in the conversation" : "ประเด็นที่ผู้ชมพูดถึง"} subtitle={en ? "One comment may cover multiple topics; totals may exceed 100%." : "หนึ่งความคิดเห็นอาจมีหลายประเด็น ผลรวมจึงอาจเกิน 100%"} badge={`${items.length} ${en ? "topics" : "ประเด็น"}`}>
    <button type="button" onClick={() => onSelectTopic(null)} aria-pressed={selectedTopic === null} className={`mb-3 rounded-lg border px-3 py-2 text-sm font-medium text-indigo-700 ${selectedTopic === null ? "border-indigo-300 bg-indigo-50" : "border-slate-200"}`}>{en ? "All comments" : "ความคิดเห็นทั้งหมด"}</button>
    {items.length ? <ul className="space-y-2">{items.map((item) => <li key={item.key}>
      <button type="button" aria-pressed={selectedTopic === item.key} onClick={() => onSelectTopic(item.key)} className={`w-full rounded-xl border p-3 text-left transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-indigo-600 ${selectedTopic === item.key ? "border-indigo-300 bg-indigo-50" : "border-transparent hover:bg-slate-50"}`}>
        <span className="mb-2 flex justify-between gap-3 text-sm"><span>{item.name}</span><span className="font-semibold">{percent(item.value)}</span></span>
        <span className="block h-2 overflow-hidden rounded-full bg-slate-100" aria-hidden="true"><span className="block h-full rounded-full bg-indigo-500" style={{ width: `${Math.min(100, Math.max(0, item.value || 0))}%` }} /></span>
      </button>
    </li>)}</ul> : <p className="py-12 text-center text-sm text-slate-500">{en ? "No topics yet" : "ยังไม่มีข้อมูลประเด็น"}</p>}
  </AnalysisPanel>;
}

export const topicName = (key, language = "th") => names[key]?.[language === "en" ? 1 : 0] || key;
