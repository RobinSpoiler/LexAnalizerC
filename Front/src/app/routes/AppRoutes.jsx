import { Routes, Route } from "react-router-dom";
import { Comparator } from "../pages";

export const AppRoutes = () => {
  const renderRoutes = () => (
    <>
      <Route path="/comparator" element={<Comparator />} />
      <Route path="/*" element={<Comparator />} />
    </>
  );

  return (
    <Routes>
      {renderRoutes()}
    </Routes>
  );
};