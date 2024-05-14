import { Routes, Route } from "react-router-dom";
import { Comparator, PlagiarismOverview, Uploader } from "../pages";
import { Highlighter } from "../pages";

export const AppRoutes = () => {
  const renderRoutes = () => (
    <>
      <Route path="/comparator" element={<Comparator />} />
      <Route path="/highlighter" element={<Highlighter />} />
      <Route path="/upload" element={<Uploader />} />
      <Route path="/plagiarismoverview" element={<PlagiarismOverview />} />
      <Route path="/*" element={<Comparator />} />
    </>
  );

  return (
    <Routes>
      {renderRoutes()}
    </Routes>
  );
};