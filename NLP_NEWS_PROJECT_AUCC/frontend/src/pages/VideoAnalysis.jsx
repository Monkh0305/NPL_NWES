import VideoThumbnail from "../components/VideoThumbnail.jsx";
import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Eye, ThumbsUp, MessageCircle } from "lucide-react";
import { getVideo, runAnalysis } from "../api/client.js";
import SentimentChart from "../components/SentimentChart.jsx";
import EmotionChart from "../components/EmotionChart.jsx";
import TopicChart from "../components/TopicChart.jsx";
import VideoSummary from "../components/VideoSummary.jsx";
import TopicComments from "../components/TopicComments.jsx";
import { ChartSkeleton, ErrorState } from "../components/Skeletons.jsx";

export default function VideoAnalysis({ language = "th" }) {
  const { videoId } = useParams();
  const [video, setVideo] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const text = {
    th: {
      back: "กลับสู่หน้าหลัก",
      analysisError: "วิเคราะห์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง",
      summary: "สรุป",
      generatedFrom: "สร้างจาก",
      comments: "ความคิดเห็น",
    },
    en: {
      back: "Back to Dashboard",
      analysisError: "Analysis failed. Please try again.",
      summary: "Summary",
      generatedFrom: "Generated from",
      comments: "comments",
    },
  }[language] || {
    back: "กลับสู่หน้าหลัก",
    analysisError: "วิเคราะห์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง",
    summary: "สรุป",
    generatedFrom: "สร้างจาก",
    comments: "ความคิดเห็น",
  };

  useEffect(() => {
    setLoading(true);
    setSelectedTopic(null);
    setError(null);
    Promise.all([getVideo(videoId).then((data) => { setVideo(data); return data; }), runAnalysis(videoId)])
      .then(([videoData, analysisData]) => {
        setVideo(videoData);
        setAnalysis(analysisData);
      })
      .catch((requestError) => {
        const detail = requestError.response?.data?.detail;
        const apiError = requestError.response?.data?.youtube_error;
        setError(apiError || detail || text.analysisError);
      })
      .finally(() => setLoading(false));
  }, [videoId, text.analysisError, retryCount]);

  return (
    <div className="space-y-5 sm:space-y-6">
      <Link to="/" className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 transition hover:text-slate-900">
        <ArrowLeft size={16} /> {text.back}
      </Link>

      {video && (
        <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div className="flex flex-col gap-4 p-4 sm:flex-row sm:p-5">
            <VideoThumbnail language={language} sample={video.video_id?.startsWith("mock_")} src={video.thumbnail} alt={video.title} className="aspect-video h-auto w-full rounded-2xl object-cover sm:h-48 sm:w-64" />
            <div className="flex-1 space-y-3">
              <h1 className="text-xl font-bold text-slate-900">{video.title}</h1>
              <p className="text-sm font-medium text-slate-500">{video.channel}</p>
              <div className="flex flex-wrap gap-4 text-sm text-slate-600">
                <span className="inline-flex items-center gap-1.5"><Eye size={14} />{video.views.toLocaleString()}</span>
                <span className="inline-flex items-center gap-1.5"><ThumbsUp size={14} />{video.likes.toLocaleString()}</span>
                <span className="inline-flex items-center gap-1.5"><MessageCircle size={14} />{video.comment_count.toLocaleString()}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {error && (
        <ErrorState
          message={error}
          onRetry={() => setRetryCount((count) => count + 1)}
        />
      )}

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2">
          <ChartSkeleton /><ChartSkeleton /><ChartSkeleton /><ChartSkeleton />
        </div>
      ) : analysis && (
        <>
          <div className="grid gap-4 md:grid-cols-2">
            <SentimentChart data={analysis.sentiment} />
            <EmotionChart data={analysis.emotion} />
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <TopicChart data={analysis.categories} language={language} selectedTopic={selectedTopic} onSelectTopic={setSelectedTopic} />
            <TopicComments comments={analysis.categories?.comments} selectedTopic={selectedTopic} language={language} />
          </div>

        </>
      )}
      <VideoSummary videoId={videoId} language={language} />
    </div>
  );
}
