import { useState } from "react";
import { Trophy } from "lucide-react";

export default function VideoThumbnail({ src, alt, className, language = "th", sample = false }) {
  const [failedSrc, setFailedSrc] = useState(null);
  if (sample || !src || failedSrc === src) {
    const label = sample
      ? (language === "en" ? "Sample sports video" : "วิดีโอกีฬาตัวอย่าง")
      : (language === "en" ? "Image unavailable" : "ไม่สามารถโหลดรูปภาพได้");
    return (
      <div role="img" aria-label={`${label}: ${alt || ""}`} className={`${className} flex flex-col items-center justify-center gap-3 bg-gradient-to-br from-indigo-600 via-violet-600 to-purple-800 text-white`}>
        <Trophy size={56} strokeWidth={1.4} aria-hidden="true" />
        <span className="text-sm font-medium">{label}</span>
      </div>
    );
  }
  return <img src={src} alt={alt} className={className} onError={() => setFailedSrc(src)} />;
}