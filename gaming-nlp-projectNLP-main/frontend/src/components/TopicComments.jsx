import AnalysisPanel, { sentimentLabels } from "./AnalysisPanel.jsx";
import { topicName } from "./TopicChart.jsx";

const styles = {
  positive: "border-emerald-200 bg-emerald-50 text-emerald-800",
  negative: "border-red-200 bg-red-50 text-red-800",
  neutral: "border-slate-200 bg-slate-50 text-slate-700",
};

export default function TopicComments({ comments, selectedTopic, language = "th" }) {
  const en = language === "en";
  const labels = sentimentLabels[en ? "en" : "th"];
  const items = (comments || []).filter((item) => !selectedTopic || item.topics.includes(selectedTopic));
  return <AnalysisPanel
    title={selectedTopic ? `${en ? "Comments: " : "ความคิดเห็น: "}${topicName(selectedTopic, language)}` : (en ? "Analyzed comments" : "ความคิดเห็นที่นำมาวิเคราะห์")}
    subtitle={en ? "Select a topic on the left to view matching comments and their sentiment." : "กดประเด็นด้านซ้ายเพื่อดูความคิดเห็นที่เกี่ยวข้องและความรู้สึก"}
    badge={`${items.length} ${en ? "comments" : "ความคิดเห็น"}`}>
    <div className="mb-4 flex flex-wrap gap-2" aria-label={en ? "Sentiment colors" : "สีแสดงความรู้สึก"}>
      {Object.entries(labels).map(([key, label]) => <span key={key} className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${styles[key]}`}>{label}</span>)}
    </div>
    <p role="status" className="sr-only">{items.length} {en ? "matching comments" : "ความคิดเห็นที่ตรงกับประเด็น"}</p>
    {items.length ? <ol className="max-h-[650px] space-y-3 overflow-y-auto pr-1">{items.map((item) => <li key={item.id} className={`rounded-xl border border-l-4 p-3 ${styles[item.sentiment] || styles.neutral}`}>
      <div className="mb-2 flex items-center justify-between gap-3 text-xs"><span>#{item.id + 1}</span><span className="font-bold">{labels[item.sentiment]}</span></div>
      <p className="whitespace-pre-wrap break-words text-sm leading-6">{item.text}</p>
      <div className="mt-2 flex flex-wrap gap-1.5">{item.topics.map((topic) => <span key={topic} className="rounded-md bg-white/70 px-2 py-1 text-xs text-slate-600">{topicName(topic, language)}</span>)}</div>
    </li>)}</ol> : <p className="py-12 text-center text-sm text-slate-500">{comments === undefined
      ? (en ? "Run the analysis again to see comments by topic." : "กรุณาวิเคราะห์ใหม่เพื่อดูความคิดเห็นแยกตามประเด็น")
      : (en ? "No comments for this topic." : "ไม่มีความคิดเห็นในประเด็นนี้")}</p>}
  </AnalysisPanel>;
}
