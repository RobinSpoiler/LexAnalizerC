import { Routes, Route } from "react-router-dom";
import { Overview, Uploader, Highlighter } from "../pages";

export const AppRoutes = () => {
  const renderRoutes = () => (
    <>
      {/* <Route path="/comparator" element={<Comparator />} /> */}
      <Route path="/highlighter" element={<Highlighter />} />
      <Route path="/upload" element={<Uploader />} />
      <Route path="/overview" element={<Overview />} />
      <Route path="/*" element={<Uploader />} />
    </>
  );

  return (
    <Routes>
      {renderRoutes()}
    </Routes>
  );
};